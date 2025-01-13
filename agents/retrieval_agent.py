from pydantic import BaseModel
from typing import Optional
from schemas.agents import AgentState

class RetrievalAgent:
    @staticmethod
    def retrieve_documents(state: AgentState) -> dict:
        print("🤖 Retrieval Agent Running")
        retrieved_docs = ["doc1", "doc2", "doc3"]
        
        return {"documents": retrieved_docs}

