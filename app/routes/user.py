from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    return {"id": user.id, "name": user.name, "email": user.email}

@router.put("/{user_id}")
def update_user_profile(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    
    user.name = user_data.name
    user.email = user_data.email
    db.commit()
    return {"message": "User profile updated successfully"}
