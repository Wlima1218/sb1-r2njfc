from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class ProfessorBase(BaseModel):
    especialidade: str
    percentual_padrao: float

class ProfessorCreate(ProfessorBase):
    user_id: int

class ProfessorUpdate(BaseModel):
    especialidade: Optional[str] = None
    percentual_padrao: Optional[float] = None

class ProfessorInDB(ProfessorBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True