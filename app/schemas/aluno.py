from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class AlunoBase(BaseModel):
    nome: str
    professor_id: int
    percentual_desconto: float

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    percentual_desconto: Optional[float] = None

class AlunoInDB(AlunoBase):
    id: int
    
    class Config:
        from_attributes = True