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

        prompt = '''
You are an expert medical knowledge assistant. Your task is to provide answers to medical questions. You can chat with the patient to assist them as a medical professional.

Your responsibilities include:
1. Answering the question using only relevant medical documents to provide accurate responses.
2. If the provided documents are not relevant or you cannot determine the exact answer, requesting additional data.
3. Asking the user a follow-up question to gather more details (as a doctor would do to clarify symptoms or obtain more context).

You must choose the most appropriate option based on the provided information.

Details:
- Past chat: ''' + chat + '''
- User query: ''' + userQuestion + '''
- Medical documents: ''' + documents + '''

Respond in JSON format, ensuring only one of the following three options is included:
{
    "answer": "YOUR ANSWER",  # Use this if you can confidently answer the query based on the given documents.
    "needMoreDocuments": 0 or 1,  # Use 1 if additional documents are required, otherwise 0.
    "AskQuestionFromUser": "YOUR QUESTION"  # Use this if more context or clarification is needed.
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
        
        return {"answer": generated_answer, "needs_refinement": False}

