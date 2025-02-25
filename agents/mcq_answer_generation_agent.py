import ast
from pydantic import BaseModel
from typing import List, Optional
from schemas.agents import AgentState
from utils.openaiClient import openaiClient
from liquid import Template

class McqAnswerGenerationAgent:
    @staticmethod
    def generate_mcq_answer(state: AgentState) -> dict:
        print("🤖 Mcq Answer Generation Agent Running")

        prompt = Template('''
        You are a helpful medical expert, and your task is to answer a multi-choice medical question using the relevant documents. 
        First think step-by-step and then choose the answer from the provided options. Organize your output in a json formatted as 
        Dict{"step_by_step_thinking": (explanation), "answer_choice": (A/B/C)}. 
        Your responses will be used for research purposes only, so have a definite answer.

        Here are the relevant documents:
        {{context}}

        Here is the question:
        {{question}}

        Here are the potential choices:
        {{options}}

        Please think step-by-step and generate your output in json:

        ''')
        
        documents = ", \n".join([f"document {i+1}: {doc}" for i, doc in enumerate(state.documents)]) if state.documents else 'None'
        final_prompt = prompt.render(context=documents, question=state.user_query, options=state.answer_options)
        
        answer = openaiClient.generate_response(final_prompt)

        return {"answer": answer}
