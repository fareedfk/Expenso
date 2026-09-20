from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    currency: Optional[str] = "INR"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    currency: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
