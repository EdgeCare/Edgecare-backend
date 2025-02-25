from pydantic import BaseModel
from typing import List, Optional

class AgentState(BaseModel):
    chat: Optional[str] = ""
    user_query: Optional[str] = ""
    health_reports : Optional[str] = None
    keywords: Optional[List[str]] = None
    documents: Optional[List[str]] = None
    # needs_refinement: bool = False
    answer_options: Optional[str] = None
    answer: Optional[str] = None

    

