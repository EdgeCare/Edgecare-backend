from pydantic import BaseModel
from typing import List, Optional

class AgentState(BaseModel):
    user_query: Optional[str] = None
    keywords: Optional[List[str]] = None
    documents: Optional[List[str]] = None
    answer: Optional[str] = None
    needs_refinement: bool = False

    

