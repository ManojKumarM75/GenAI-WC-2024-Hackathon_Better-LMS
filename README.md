# GenAI_WC_202410
Gen AI world Cup - Hackathon 20241031

Dharmendra Pratap Singh, Praveen Kumar Gupta, Manoj Kumar Manmathan

The Project: BETTER LMS

In many organizations, the Learning Management Systems (LMS) primarily rely on static content such as PDFs and videos for training and development. This approach often leads to passive learning experiences that do not effectively engage learners or assess their understanding.



To address this limitation, there is a need for an innovative solution that leverages Generative AI to create dynamic, interactive content. By generating a variety of question-answer pairs, including multiple-choice questions (MCQs), fill-in-the-blanks, and true/false questions, match the followings, we can transform the traditional learning experience into an engaging and customizable journey. 



Our project uses Gemini API to create diverse QA pairs form chunks. PDF proprocessing and chunking ensures only reading content is send for QAG. The QA pairs are then stored in db. User interacts with Streamlit GUI for quizzes.

PDF input-> Preprocess -> Question Answer Generation with Gemini API [MCQs, Fill in the blanks, True/False, Match the following] -> to database -> GUI for user.


![image](https://github.com/user-attachments/assets/ba155cec-a581-478b-92a4-918fb7b196bd)
![image](https://github.com/user-attachments/assets/22e655bb-b27a-4ae9-b9af-1eecf8344569)
![image](https://github.com/user-attachments/assets/91d9616c-2e1d-4e6d-bf8b-e942524fee7f)
![image](https://github.com/user-attachments/assets/56559859-2ed1-4cfe-83ca-9c5255616f42)
![image](https://github.com/user-attachments/assets/822aab78-55cd-49d5-8e44-e91089c91cbb)



