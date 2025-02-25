from schemas.agents import AgentState
from utils.openaiClient import openaiClient
from utils.extractContent import extract_json

class QuestionAnsweringAgent:
    @staticmethod
    def answer_question(state: AgentState) -> dict:
        print("🤖 Question Answering Agent Running")

        documents = ", \n".join([f"document {i+1}: {doc}" for i, doc in enumerate(state.documents)]) if state.documents else 'None'

        userQuestion = state.user_query
        chat = state.chat if state.chat else 'None'
        healthReports = state.health_reports

        prompt = '''You are a professional and user-friendly medical expert who provides accurate and helpful responses based on user input, health reports, and relevant medical documents. Follow these steps:

1. **Analyze the User Query**: Understand the user’s medical question, symptoms, or concern in detail.
2. **Evaluate Provided Health Reports**: Review the relevant health reports supplied by the user to determine if sufficient information is available.
3. **Ask Follow-Up Questions One at a Time If More Information is Needed**:
   - If the provided medical information is **insufficient**, ask **only one follow-up question** first.
   - **Wait for the user’s response** before asking the next follow-up question (if still needed).
   - Continue this process until at least **three follow-up questions have been asked** (if necessary).
   - **Do not ask more than three consecutive follow-up questions.** Before asking a follow-up, always review the past chat to avoid repetition.
4. **Use Medical Knowledge**: Use the provided medical documents for extra knowledge, but do not mention them in your final answer.
5. **Request Additional Document Searches (If Needed)**: If the provided documents are insufficient, suggest queries for document similarity search from the medical knowledge base.
6. **If user has asked a direct question answer to that question. Or else ask wether the user like to provide more information.
6. **Provide a Comprehensive Answer Only After Sufficient Information Is Collected or after 3 consecutive follow-up questions**:
   - Symptom analysis and possible conditions
   - Recommended next steps (home remedies, medical tests, doctor consultation, etc.)
   - Warnings for any serious symptoms requiring urgent care
   - **Use a structured, pointwise format** for better readability.
   - **Be empathetic and supportive** while maintaining accuracy.
   - **Make the response easy to understand** by avoiding overly complex medical jargon.

**Important Rules**:
- **Ask only one follow-up question at a time.**
- **If sufficient details are provided in the initial query and past chat, skip follow-up questions and proceed with the answer.**

**Provided Data:**
- **Past chat (to determine available details):** ''' + chat + '''
- **User query:** ''' + userQuestion + '''
- **User health reports:** ''' + healthReports + '''
- **Documents for extra medical knowledge:** ''' + documents + '''

Respond in JSON format with the following structure:
{
    "follow_up_question": QUESTION,  # Leave blank if you provide final answer
    "document_search_queries": ["QUERY1", "QUERY2"],  # If additional documents are needed, otherwise an empty array
    "answer": ""  # Leave blank if you ask followup question
}
'''

        for _ in range(5):
            try: 
                generated_answer =  openaiClient.generate_response(prompt)
                json_response = extract_json(generated_answer)
                print(json_response)

                answer = json_response.get("answer", "")
                follow_up_question = json_response.get("follow_up_question","")
                need_more_documents = json_response.get("needMoreDocuments", 0)
                ask_question_from_user = json_response.get("AskQuestionFromUser", "")

                if answer:
                    return {"answer": answer}
                elif follow_up_question:
                    return {"answer":follow_up_question}
            except:
                pass

        generated_answer = "System Unavailable" 
                
        return {"answer": generated_answer}

