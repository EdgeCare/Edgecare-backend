
from pydantic import BaseModel
from datetime import datetime

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
