from pydantic import BaseModel
from typing import List, Optional
from schemas.agents import AgentState

class RetrievalAgent:
    @staticmethod
    def retrieve_documents(state: AgentState) -> dict:
        print("Retrieval Agent Running", state)
        retrieved_docs = ["doc1", "doc2"]
        state.documents = retrieved_docs
        return state

