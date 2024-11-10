from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.deps import get_current_active_user
from ..database import get_db
from ..models.user import User, UserType
from ..models.aluno import Aluno
from ..models.professor import Professor
from ..schemas.aluno import AlunoCreate, AlunoUpdate, AlunoInDB

router = APIRouter(prefix="/alunos", tags=["alunos"])

@router.post("/", response_model=AlunoInDB)
def create_aluno(
    aluno: AlunoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type not in [UserType.ADMIN, UserType.PROFESSOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Se for professor, só pode adicionar alunos para si mesmo
    if current_user.user_type == UserType.PROFESSOR:
        professor = db.query(Professor).filter(Professor.user_id == current_user.id).first()
        if not professor or professor.id != aluno.professor_id:
            raise HTTPException(status_code=403, detail="Professor can only add students to themselves")
    
    db_aluno = Aluno(**aluno.model_dump())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@router.get("/", response_model=List[AlunoInDB])
def read_alunos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type == UserType.PROFESSOR:
        professor = db.query(Professor).filter(Professor.user_id == current_user.id).first()
        if not professor:
            raise HTTPException(status_code=404, detail="Professor not found")
        return db.query(Aluno).filter(Aluno.professor_id == professor.id).offset(skip).limit(limit).all()
    elif current_user.user_type == UserType.ADMIN:
        return db.query(Aluno).offset(skip).limit(limit).all()
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

@router.put("/{aluno_id}", response_model=AlunoInDB)
def update_aluno(
    aluno_id: int,
    aluno_update: AlunoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type not in [UserType.ADMIN, UserType.PROFESSOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    
    # Se for professor, só pode atualizar seus próprios alunos
    if current_user.user_type == UserType.PROFESSOR:
        professor = db.query(Professor).filter(Professor.user_id == current_user.id).first()
        if not professor or professor.id != db_aluno.professor_id:
            raise HTTPException(status_code=403, detail="Professor can only update their own students")
    
    for field, value in aluno_update.model_dump(exclude_unset=True).items():
        setattr(db_aluno, field, value)
    
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@router.delete("/{aluno_id}")
def delete_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type not in [UserType.ADMIN, UserType.PROFESSOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    
    # Se for professor, só pode deletar seus próprios alunos
    if current_user.user_type == UserType.PROFESSOR:
        professor = db.query(Professor).filter(Professor.user_id == current_user.id).first()
        if not professor or professor.id != db_aluno.professor_id:
            raise HTTPException(status_code=403, detail="Professor can only delete their own students")
    
    db.delete(db_aluno)
    db.commit()
    return {"message": "Aluno deleted successfully"}