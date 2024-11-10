from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Enum
import enum
from .base import BaseModel

class StatusAgendamento(str, enum.Enum):
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"

class Agendamento(BaseModel):
    __tablename__ = "agendamentos"

    quadra_id = Column(Integer, ForeignKey("quadras.id"))
    cliente_id = Column(Integer, ForeignKey("users.id"))
    data_hora_inicio = Column(DateTime)
    data_hora_fim = Column(DateTime)
    status = Column(Enum(StatusAgendamento))
    valor = Column(Float)
    observacoes = Column(String, nullable=True)