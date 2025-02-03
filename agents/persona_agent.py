from schemas.agents import AgentState
from langgraph.types import Command
from langgraph.graph import END
from utils.openaiClient import openaiClient

class PersonaAgent:
    @staticmethod
    def talk(state: AgentState):
        print('Persona is running...')
        chat_history = state.chat
        user_message = state.user_query
        prompt_base = f''' You are Lisa, an empathetic and supportive autonomous medical assistant representing the 
EdgeCare Autonomous Health Assistance System. Your role is to provide emotional support, reassurance, 
and clear communication in a professional and compassionate tone. You do not give medical advice or opinions 
of your own. Instead, you focus on delivering medical information provided by the Edgecare autonomous medical 
expert system in a way that is easy to understand, empathetic, and tailored to the user's situation. Always 
acknowledge the user's feelings and concerns, and ensure they feel heard and supported. Here is the 
conversation history so far:{chat_history}
User's latest message: {user_message}
        '''
        prompt_end = '''Lisa, respond empathetically based on the provided information and user context, blending in 
        the medical advice seamlessly if provided above by expert system.'''
        if len(state.keywords)==0:
            # Just a casual reply
            prompt = prompt_base+'''Lisa, For this user message there is no a significant medical advice from expert 
                                  system. Just causally answer '''+prompt_end

        else:
            medical_answer = state.answer
            prompt = prompt_base + f"Expert system suggests: {medical_answer} " + prompt_end

        generated_answer = openaiClient.generate_response(prompt)
        state.answer=generated_answer
        print("\nPersona Process Complete!\n")
        # print("Output:", generated_answer)
        return {"answer": generated_answer}