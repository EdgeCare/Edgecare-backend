from pydantic import BaseModel
from typing import List, Optional
from schemas.agents import AgentState

class KeywordExtractionAgent:
    @staticmethod
    def extract_keywords(state: AgentState) -> dict:
        print("Keyword Extraction Agent Running", state)
        extracted_keywords = ["keyword1", "keyword2"]
        state.keywords = extracted_keywords
        return state
