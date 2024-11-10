from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class UserType(str, enum.Enum):
    ADMIN = "admin"
    PROFESSOR = "professor"
    CLIENTE = "cliente"

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    user_type = Column(Enum(UserType))
    is_active = Column(Boolean, default=True)
    
    professor_profile = relationship("Professor", back_populates="user", uselist=False)