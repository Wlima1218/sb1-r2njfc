from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class Categoria(str, enum.Enum):
    INICIANTE = "iniciante"
    INTERMEDIARIO = "intermediario"
    AVANCADO = "avancado"

class TipoRanking(str, enum.Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    MISTO = "misto"

class Ranking(BaseModel):
    __tablename__ = "rankings"

    nome = Column(String)
    categoria = Column(Enum(Categoria))
    tipo = Column(Enum(TipoRanking))
    
    participantes = relationship("ParticipanteRanking", back_populates="ranking")

class ParticipanteRanking(BaseModel):
    __tablename__ = "participantes_ranking"

    ranking_id = Column(Integer, ForeignKey("rankings.id"))
    jogador_id = Column(Integer, ForeignKey("users.id"))
    pontos = Column(Integer, default=0)
    
    ranking = relationship("Ranking", back_populates="participantes")
    jogador = relationship("User")