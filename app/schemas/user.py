from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserType(str, Enum):
    ADMIN = "admin"
    PROFESSOR = "professor"
    CLIENTE = "cliente"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    user_type: UserType

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None