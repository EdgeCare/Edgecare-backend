from pydantic import BaseModel
from datetime import datetime

class UserQuestionRequest(BaseModel):
    userId: int
    chatId: int
    token: str
    content: str
    healthReports: str

class UserQuestionResponce(BaseModel):
    status: str
    content:str

class McqQuestionRequest(BaseModel):
    id: int
    title: str
    question: str
    options:str

class PersonaRequest(BaseModel):
    id:int
    details:str
    
# Base schema for user
class UserBase(BaseModel):
    email: str

# Schema for creating a new user
class UserCreate(UserBase):
    email: str
    password: str

# Schema for authentication token
class TokenResponse(BaseModel):
    token: str
    userId: str
    expiresAt: datetime
