from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProductCreate(BaseModel):
    name: str
    price: float
    category: str
    stock: int
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    stock: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class CartItem(BaseModel):
    product_id: int
    quantity: int

class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    name: str
    price: float
    quantity: int
    total_price: float

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    user_id: int
    payment_status: str  
