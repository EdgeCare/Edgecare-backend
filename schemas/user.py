from pydantic import BaseModel
from datetime import datetime

class UserQuestionRequest(BaseModel):
    userId: int
    token: str
    content: str

class UserQuestionResponce(BaseModel):
    status: str
    content:str

class PostMcqData(BaseModel):
    id: int
    title: str
    question: str
    options:str
    
# Base schema for user
class UserBase(BaseModel):
    email: str

# Schema for creating a new user
class UserCreate(UserBase):
    email: str
    password: str

# Schema for response with user details
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# Schema for authentication token
class TokenResponse(BaseModel):
    token: str
    userId: str
    expiresAt: datetime
