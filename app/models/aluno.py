from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Aluno(BaseModel):
    __tablename__ = "alunos"

    nome = Column(String)
    professor_id = Column(Integer, ForeignKey("professores.id"))
    percentual_desconto = Column(Float)
    
    professor = relationship("Professor", back_populates="alunos")