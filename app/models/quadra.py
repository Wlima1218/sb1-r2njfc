from sqlalchemy import Column, String, Float, Boolean
from .base import BaseModel

class Quadra(BaseModel):
    __tablename__ = "quadras"

    nome = Column(String, index=True)
    descricao = Column(String)
    valor_hora = Column(Float)
    coberta = Column(Boolean, default=False)
    iluminacao = Column(Boolean, default=False)