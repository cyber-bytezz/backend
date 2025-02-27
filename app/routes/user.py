from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils.security import get_current_user, get_password_hash, verify_password
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["Users"])

class ProfileUpdate(BaseModel):
    name: str
    email: EmailStr

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    
class AddressUpdate(BaseModel):
    address: str

class UserProfileUpdate(BaseModel):
    name: str
    email: str
    address: str 
    
    
@router.get("/profile")
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch the profile details of the logged-in user"""
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email}

@router.put("/profile")
def update_profile(profile_data: ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update the user's profile information"""
    current_user.name = profile_data.name
    current_user.email = profile_data.email
    db.commit()
    return {"message": "Profile updated successfully"}

@router.put("/change-password")
def change_password(data: ChangePasswordRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Allow users to change their password"""
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    current_user.password_hash = get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.get("/address")
def get_shipping_address(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch the saved shipping address of the logged-in user"""
    return {"address": current_user.address or ""}  # Return empty if no address saved

@router.put("/address")
def update_shipping_address(address_data: AddressUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update the shipping address for the logged-in user"""
    current_user.address = address_data.address
    db.commit()
    return {"message": "Shipping address updated successfully"}

@router.get("/profile")
def get_user_profile(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Retrieve the current user's profile"""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "address": current_user.address  # ✅ Return address
    }

@router.put("/profile")
def update_user_profile(user_data: UserProfileUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Update the current user's profile"""
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.email = user_data.email
    user.address = user_data.address  # ✅ Allow updating address

    db.commit()
    return {"message": "Profile updated successfully"}