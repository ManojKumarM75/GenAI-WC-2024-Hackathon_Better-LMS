import streamlit as st
import sqlite3
import random

def get_questions():
    conn = sqlite3.connect('quiz_database.db')
    cursor = conn.cursor()
    
    questions = {
        'Blanks': cursor.execute("SELECT * FROM blanks").fetchall(),
        'Match': cursor.execute("SELECT * FROM match_questions").fetchall(),
        'MCQ': cursor.execute("SELECT * FROM mcq").fetchall(),
        'True/False': cursor.execute("SELECT * FROM true_false").fetchall()
    }
    
    conn.close()
    return questions

def get_match_options(question_id):
    conn = sqlite3.connect('quiz_database.db')
    cursor = conn.cursor()
    options = cursor.execute("SELECT term, option FROM match_options WHERE question_id=?", (question_id,)).fetchall()
    conn.close()
    return options

def get_mcq_options(question_id):
    conn = sqlite3.connect('quiz_database.db')
    cursor = conn.cursor()
    options = cursor.execute("SELECT option FROM mcq_options WHERE question_id=?", (question_id,)).fetchall()
    conn.close()
    return [option[0] for option in options]

def read_data():
    output = []
    try:
        conn = sqlite3.connect('quiz_database.db')
        cursor = conn.cursor()

        output.append("Blanks Questions:")
        try:
            cursor.execute("SELECT * FROM blanks")
            for row in cursor.fetchall():
                output.append(f"Question: {row[1]}\nAnswer: {row[2]}\n")
        except sqlite3.Error as e:
            output.append(f"Error reading blanks questions: {e}")

        output.append("\nMatch Questions:")
        try:
            cursor.execute("SELECT * FROM match_questions")
            for row in cursor.fetchall():
                output.append(f"Question: {row[1]}")
                try:
                    cursor.execute("SELECT * FROM match_options WHERE question_id=?", (row[0],))
                    output.append("Options:")
                    for option in cursor.fetchall():
                        output.append(f"  {option[2]}: {option[3]}")
                except sqlite3.Error as e:
                    output.append(f"Error reading match options: {e}")
                
                try:
                    cursor.execute("SELECT * FROM match_answers WHERE question_id=?", (row[0],))
                    output.append("Answers:")
                    for answer in cursor.fetchall():
                        output.append(f"  {answer[2]}: {answer[3]}")
                except sqlite3.Error as e:
                    output.append(f"Error reading match answers: {e}")
                output.append("")
        except sqlite3.Error as e:
            output.append(f"Error reading match questions: {e}")

        output.append("\nMCQ Questions:")
        try:
            cursor.execute("SELECT * FROM mcq")
            for row in cursor.fetchall():
                output.append(f"Question: {row[1]}")
                output.append(f"Correct Answer: {row[2]}")
                try:
                    cursor.execute("SELECT * FROM mcq_options WHERE question_id=?", (row[0],))
                    output.append("Options:")
                    for option in cursor.fetchall():
                        output.append(f"  - {option[2]}")
                except sqlite3.Error as e:
                    output.append(f"Error reading MCQ options: {e}")
                output.append("")
        except sqlite3.Error as e:
            output.append(f"Error reading MCQ questions: {e}")

        output.append("\nTrue/False Questions:")
        try:
            cursor.execute("SELECT * FROM true_false")
            for row in cursor.fetchall():
                output.append(f"Question: {row[1]}\nAnswer: {row[2]}\n")
        except sqlite3.Error as e:
            output.append(f"Error reading true/false questions: {e}")

    except sqlite3.Error as e:
        output.append(f"Error connecting to the database: {e}")
    finally:
        if conn:
            conn.close()
    
    return "\n".join(output)

def main():
    st.title("Quiz App")
    
    if 'questions' not in st.session_state:
        st.session_state.questions = get_questions()
    
    # Ask user for the number of questions
    if 'quiz_started' not in st.session_state:
        st.session_state.num_questions = st.number_input("How many questions would you like in the quiz?", 
                                                         min_value=1, 
                                                         max_value=sum(len(q) for q in st.session_state.questions.values()), 
                                                         value=5)
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.total_questions = st.session_state.num_questions
            st.session_state.questions_list = []
            st.session_state.history = []
            st.session_state.last_answer = None
            for q_type, q_list in st.session_state.questions.items():
                st.session_state.questions_list.extend([(q_type, q) for q in q_list])
            random.shuffle(st.session_state.questions_list)
            st.session_state.questions_list = st.session_state.questions_list[:st.session_state.num_questions]
            st.rerun()
    
    # Quiz logic
    if 'quiz_started' in st.session_state and st.session_state.quiz_started:
        if st.session_state.current_question < st.session_state.total_questions:
            q_type, question = st.session_state.questions_list[st.session_state.current_question]
            
            st.write(f"Question {st.session_state.current_question + 1} of {st.session_state.total_questions}")
            st.write(question[1])  # Display the actual question text
            
            if q_type == 'Blanks':
                user_answer = st.text_input("Your answer:", key=f"blank_{st.session_state.current_question}")
                submit_button = st.button("Submit")
                
                if submit_button:
                    if user_answer.lower() == question[2].lower():
                        st.success("Correct!")
                        st.session_state.score += 1
                        st.session_state.history.append((question[1], user_answer, "Correct", question[2]))
                    else:
                        st.error(f"Incorrect. The correct answer is: {question[2]}")
                        st.session_state.history.append((question[1], user_answer, "Incorrect", question[2]))
                    st.session_state.current_question += 1
                    st.session_state.last_answer = None
                    st.rerun()
            
            elif q_type == 'Match':
                options = get_match_options(question[0])
                user_answers = {}
                for term, _ in options:
                    user_answers[term] = st.selectbox(f"Match for {term}", [opt[1] for opt in options], key=f"match_{term}_{st.session_state.current_question}")
                if st.button("Submit"):
                    correct_answers = dict(options)
                    if user_answers == correct_answers:
                        st.success("Correct!")
                        st.session_state.score += 1
                        st.session_state.history.append((question[1], "All matches correct", "Correct", str(correct_answers)))
                    else:
                        st.error("Incorrect. The correct matches are:")
                        for term, answer in correct_answers.items():
                            st.write(f"{term}: {answer}")
                        st.session_state.history.append((question[1], str(user_answers), "Incorrect", str(correct_answers)))
                    st.session_state.current_question += 1
                    st.rerun()
            
            elif q_type == 'MCQ':
                options = get_mcq_options(question[0])
                user_answer = st.radio("Choose the correct option:", options, key=f"mcq_{st.session_state.current_question}")
                if st.button("Submit"):
                    if user_answer == question[2]:
                        st.success("Correct!")
                        st.session_state.score += 1
                        st.session_state.history.append((question[1], user_answer, "Correct", question[2]))
                    else:
                        st.error(f"Incorrect. The correct answer is: {question[2]}")
                        st.session_state.history.append((question[1], user_answer, "Incorrect", question[2]))
                    st.session_state.current_question += 1
                    st.rerun()
            
            elif q_type == 'True/False':
                user_answer = st.radio("Your answer:", ["True", "False"], key=f"tf_{st.session_state.current_question}")
                if st.button("Submit"):
                    if user_answer == question[2]:
                        st.success("Correct!")
                        st.session_state.score += 1
                        st.session_state.history.append((question[1], user_answer, "Correct", question[2]))
                    else:
                        st.error(f"Incorrect. The correct answer is: {question[2]}")
                        st.session_state.history.append((question[1], user_answer, "Incorrect", question[2]))
                    st.session_state.current_question += 1
                    st.rerun()
        
        else:
            st.write("Quiz completed!")
            st.markdown(
                f"""
                <div style="
                    background-color: #f0f2f6;
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid #4CAF50;
                    text-align: center;
                ">
                    <h2 style="color: #4CAF50;">Your Final Score</h2>
                    <h1 style="color: #1E88E5;">{st.session_state.score} out of {st.session_state.total_questions}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        
        # Add a border line after the quiz
        st.markdown("---")
        
        # Display history
        if st.session_state.history:
            st.markdown("<hr style='border: 2px solid #0000FF;'>", unsafe_allow_html=True)
            st.markdown("## Quiz History")
            st.markdown("<hr style='border: 2px solid #0000FF;'>", unsafe_allow_html=True)
            
            for i, (question, user_answer, result, correct_answer) in enumerate(reversed(st.session_state.history), 1):
                question_number = len(st.session_state.history) - i + 1
                st.write(f"{question_number}. Question: {question}")
                st.write(f"   Your answer: {user_answer}")
                st.write(f"   Correct answer: {correct_answer}")
                if result == "Correct":
                    st.markdown(f"   Result: <span style='color: green;'>{result}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"   Result: <span style='color: red;'>{result}</span>", unsafe_allow_html=True)
                st.write("---")
        
        if st.button("Restart Quiz"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Add a password-protected button to display database contents
        st.markdown("---")
        st.markdown("## Admin Section")
        
        # Create a container for admin controls
        admin_container = st.container()
        
        # Add password input and button in the container
        with admin_container:
            admin_password = st.text_input("Enter admin password:", type="password")
            show_db = st.button("Show DB Contents")
        
        if show_db:
            if admin_password == 'p':
                st.markdown("### Database Contents")
                st.text_area("", value=read_data(), height=500, max_chars=None, key="db_contents")
            else:
                st.error("Incorrect password. Access denied.")

if __name__ == "__main__":
    main()
