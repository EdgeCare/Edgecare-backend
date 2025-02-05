from schemas.agents import AgentState
from utils.openaiClient import openaiClient
from utils.extractContent import extract_json

class QuestionAnsweringAgent:
    @staticmethod
    def answer_question(state: AgentState) -> dict:
        print("🤖 Question Answering Agent Running")

        documents = "\n".join(state.documents) if state.documents else 'None'
        userQuestion = state.user_query
        chat = state.chat if state.chat else 'None'

        prompt = '''You are a professional and user-friendly medical expert who provides accurate and helpful responses based on user input and relevant medical documents. Follow these steps:

1. **Analyze the User Query**: Understand the user’s medical question, symptoms, or concern in detail.
2. **Evaluate Provided Documents**: Review the relevant medical documents supplied by the user to find useful information.
3. **Ask Follow-Up Questions (If Needed)**: If more details are required, ask follow-up questions to clarify symptoms, medical history, or context.
4. **Request Additional Document Searches (If Needed)**: If the provided documents are insufficient, suggest queries for document similarity search.
5. **Provide a Comprehensive Answer**: Once enough information is available, provide a structured response including:
   - Symptom analysis and possible conditions
   - Recommended next steps (home remedies, medical tests, doctor consultation, etc.)
   - Warnings for any serious symptoms requiring urgent care
   - Relevant insights from the medical documents

**Provided Data:**
- **Past chat:** ''' + chat + '''
- **User query:** ''' + userQuestion + '''
- **Medical documents:** ''' + documents + '''

Respond in JSON format with the following structure:
{
    "follow_up_questions": ["QUESTION1", "QUESTION2"],  # If more details are needed, otherwise an empty array
    "document_search_queries": ["QUERY1", "QUERY2"],  # If additional documents are needed, otherwise an empty array
    "answer": "YOUR ANSWER"  # A well-structured, professional, and user-friendly response
}
'''
        generated_answer =  openaiClient.generate_response(prompt)
        json_responce = extract_json(generated_answer)

        answer = json_responce.get("answer", "")
        need_more_documents = json_responce.get("needMoreDocuments", 0)
        ask_question_from_user = json_responce.get("AskQuestionFromUser", "")

        if answer:
            return {"answer": answer}

        generated_answer = "This is the answer." 
        
        return {"answer": generated_answer}

