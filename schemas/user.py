from pydantic import BaseModel
from datetime import datetime

class PostData(BaseModel):
    id: int
    title: str
    content: str
    
# Base schema for user
class UserBase(BaseModel):
    username: str

# Schema for creating a new user
class UserCreate(UserBase):
    username: str
    password: str

# Schema for response with user details
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# Schema for authentication token
class TokenResponse(BaseModel):
    token: str
    expires_at: datetime


class PostData(BaseModel):
    title: str
    content: str
