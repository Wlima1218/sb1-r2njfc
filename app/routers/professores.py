from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.deps import get_current_active_user
from ..database import get_db
from ..models.user import User, UserType
from ..models.professor import Professor
from ..schemas.professor import ProfessorCreate, ProfessorUpdate, ProfessorInDB

router = APIRouter(prefix="/professores", tags=["professores"])

@router.post("/", response_model=ProfessorInDB)
def create_professor(
    professor: ProfessorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Verificar se o usuário existe e é do tipo professor
    user = db.query(User).filter(User.id == professor.user_id).first()
    if not user or user.user_type != UserType.PROFESSOR:
        raise HTTPException(status_code=400, detail="Invalid user_id or user is not a professor")
    
    # Verificar se o professor já existe
    db_professor = db.query(Professor).filter(Professor.user_id == professor.user_id).first()
    if db_professor:
        raise HTTPException(status_code=400, detail="Professor already exists")
    
    db_professor = Professor(**professor.model_dump())
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@router.get("/me", response_model=ProfessorInDB)
def read_professor_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type != UserType.PROFESSOR:
        raise HTTPException(status_code=403, detail="User is not a professor")
    
    professor = db.query(Professor).filter(Professor.user_id == current_user.id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

@router.put("/me", response_model=ProfessorInDB)
def update_professor_me(
    professor_update: ProfessorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type != UserType.PROFESSOR:
        raise HTTPException(status_code=403, detail="User is not a professor")
    
    professor = db.query(Professor).filter(Professor.user_id == current_user.id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    for field, value in professor_update.model_dump(exclude_unset=True).items():
        setattr(professor, field, value)
    
    db.commit()
    db.refresh(professor)
    return professor

@router.get("/ganhos", response_model=dict)
def calculate_earnings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type != UserType.PROFESSOR:
        raise HTTPException(status_code=403, detail="User is not a professor")
    
    professor = db.query(Professor).filter(Professor.user_id == current_user.id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    # Aqui você pode implementar a lógica de cálculo dos ganhos
    # Por exemplo, baseado nos alunos ativos e seus percentuais
    return {
        "ganhos_potenciais": 0.0,  # Implementar cálculo real
        "alunos_ativos": 0  # Implementar contagem real
    }