from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Professor(BaseModel):
    __tablename__ = "professores"

    user_id = Column(Integer, ForeignKey("users.id"))
    especialidade = Column(String)
    percentual_padrao = Column(Float)
    
    user = relationship("User", back_populates="professor_profile")
    alunos = relationship("Aluno", back_populates="professor")