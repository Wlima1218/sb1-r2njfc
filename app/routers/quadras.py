from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.deps import get_current_active_user
from ..database import get_db
from ..models.user import User, UserType
from ..models.quadra import Quadra
from ..schemas.quadra import QuadraCreate, QuadraUpdate, QuadraInDB

router = APIRouter(prefix="/quadras", tags=["quadras"])

@router.post("/", response_model=QuadraInDB)
def create_quadra(
    quadra: QuadraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_quadra = Quadra(**quadra.model_dump())
    db.add(db_quadra)
    db.commit()
    db.refresh(db_quadra)
    return db_quadra

@router.get("/", response_model=List[QuadraInDB])
def read_quadras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(Quadra).offset(skip).limit(limit).all()

@router.get("/{quadra_id}", response_model=QuadraInDB)
def read_quadra(
    quadra_id: int,
    db: Session = Depends(get_db)
):
    db_quadra = db.query(Quadra).filter(Quadra.id == quadra_id).first()
    if not db_quadra:
        raise HTTPException(status_code=404, detail="Quadra not found")
    return db_quadra

@router.put("/{quadra_id}", response_model=QuadraInDB)
def update_quadra(
    quadra_id: int,
    quadra_update: QuadraUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_quadra = db.query(Quadra).filter(Quadra.id == quadra_id).first()
    if not db_quadra:
        raise HTTPException(status_code=404, detail="Quadra not found")
    
    for field, value in quadra_update.model_dump(exclude_unset=True).items():
        setattr(db_quadra, field, value)
    
    db.commit()
    db.refresh(db_quadra)
    return db_quadra

@router.delete("/{quadra_id}")
def delete_quadra(
    quadra_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_quadra = db.query(Quadra).filter(Quadra.id == quadra_id).first()
    if not db_quadra:
        raise HTTPException(status_code=404, detail="Quadra not found")
    
    db.delete(db_quadra)
    db.commit()
    return {"message": "Quadra deleted successfully"}