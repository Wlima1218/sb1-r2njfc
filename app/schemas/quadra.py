from pydantic import BaseModel
from typing import Optional

class QuadraBase(BaseModel):
    nome: str
    descricao: str
    valor_hora: float
    coberta: bool = False
    iluminacao: bool = False

class QuadraCreate(QuadraBase):
    pass

class QuadraUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    valor_hora: Optional[float] = None
    coberta: Optional[bool] = None
    iluminacao: Optional[bool] = None

class QuadraInDB(QuadraBase):
    id: int

    class Config:
        from_attributes = True