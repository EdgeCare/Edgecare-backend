from pydantic import BaseModel

class PostData(BaseModel):
    id: int
    title: str
    content: str
    