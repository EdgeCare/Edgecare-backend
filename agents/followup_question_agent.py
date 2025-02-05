from schemas.agents import AgentState
from utils.openaiClient import openaiClient
from utils.extractContent import extract_json
from langgraph.graph import END

class FollowupQuestionsAgent:
    @staticmethod
    def answer_question(state: AgentState) -> dict:
        print("🤖 Question Answering Agent Running")

        documents = "\n".join(state.documents) if state.documents else 'None'
        userQuestion = state.user_query
        chat = state.chat if state.chat else 'None'

        prompt = '''"You are a highly knowledgeable and empathetic medical expert. Your role is to assist the user by providing medical advice or relevant information based on the details they provide.

If the user has provided clear and sufficient details about their concern, respond with precise, actionable, and easy-to-understand medical insights or recommendations. Avoid using overly complex medical jargon unless necessary.

If the user's input lacks sufficient details, identify the missing information and ask polite, clear, and relevant follow-up questions to gather more context. Ensure your questions focus on obtaining information necessary for an informed response, such as symptoms, duration, medical history, or specific concerns.

Always maintain a professional and empathetic tone, ensuring the user feels comfortable and supported."

**Provided Data:**
- **Past chat:** ''' + chat + '''
- **User query:** ''' + userQuestion + '''
- **Medical documents:** ''' + documents + '''

Respond in JSON format with the following structure:
{
      "answer": "YOUR ANSWER"  # A well-structured, professional, and user-friendly response
}
'''
        generated_answer =  openaiClient.generate_response(prompt)
        json_responce = extract_json(generated_answer)

        answer = json_responce.get("answer", "")

        if answer:
            return {"answer": answer}

        generated_answer = "This is the answer." 
        
        return {"answer": generated_answer}

