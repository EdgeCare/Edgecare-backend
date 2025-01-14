from pydantic import BaseModel
from typing import List, Optional

class AgentState(BaseModel):
    chat: Optional[str] = None
    user_query: Optional[str] = None
    keywords: Optional[List[str]] = None
    documents: Optional[List[str]] = None
    needs_refinement: bool = False
    answer: Optional[str] = None

    

