from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.utils.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user with a hashed password."""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)  # ✅ Correct hashing function
    new_user = User(name=user.name, email=user.email, password_hash=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # ✅ Ensures consistency after commit

    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),  # ✅ FIXED: FastAPI expects `username`
    db: Session = Depends(get_db)
):
    """Authenticates a user and returns a JWT token."""
    db_user = db.query(User).filter(User.email == form_data.username).first()  # ✅ `username` = email

    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token (30 min expiration)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=timedelta(minutes=30))
    
    return {"access_token": access_token, "token_type": "bearer"}
