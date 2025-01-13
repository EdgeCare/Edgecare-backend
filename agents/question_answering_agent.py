from pydantic import BaseModel
from typing import List, Optional
from schemas.agents import AgentState

class QuestionAnsweringAgent:
    @staticmethod
    def answer_question(state: AgentState) -> dict:
        print("🤖 Keyword Extraction Agent Running", state)
        generated_answer = "This is the answer." 
        
        return {"answer": generated_answer, "needs_refinement": False}

