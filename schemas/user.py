from pydantic import BaseModel
from datetime import datetime

# Base schema for authenticated users
class AuthenticatedUserBase(BaseModel):
    userId: int
    token: str

# User question from a chat
class UserQuestionRequest(AuthenticatedUserBase):
    chatId: int
    content: str
    healthReports: str

class UserQuestionResponce(BaseModel):
    status: str
    content:str

# Mcq questions - only for benchmarking
class McqQuestionRequest(BaseModel):
    id: int
    title: str
    question: str
    options:str

# User persona details
class PersonaRequest(AuthenticatedUserBase):
    details:str
