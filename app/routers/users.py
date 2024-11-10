from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.deps import get_current_active_user, get_current_user
from ..core.security import get_password_hash
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserInDB, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserInDB)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserInDB)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if user_update.email:
        current_user.email = user_update.email
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user