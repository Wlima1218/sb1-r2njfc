from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class StatusComanda(str, enum.Enum):
    ABERTA = "aberta"
    FECHADA = "fechada"
    PAGA = "paga"

class Comanda(BaseModel):
    __tablename__ = "comandas"

    cliente_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(StatusComanda))
    valor_total = Column(Float, default=0.0)
    forma_pagamento = Column(String, nullable=True)
    
    itens = relationship("ItemComanda", back_populates="comanda")

class ItemComanda(BaseModel):
    __tablename__ = "itens_comanda"

    comanda_id = Column(Integer, ForeignKey("comandas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    valor_unitario = Column(Float)
    
    comanda = relationship("Comanda", back_populates="itens")
    produto = relationship("Produto")