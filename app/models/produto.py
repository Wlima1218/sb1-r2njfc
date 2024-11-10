from sqlalchemy import Column, String, Float, Integer
from .base import BaseModel

class Produto(BaseModel):
    __tablename__ = "produtos"

    nome = Column(String)
    descricao = Column(String)
    preco = Column(Float)
    estoque = Column(Integer)
    categoria = Column(String)