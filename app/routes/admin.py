from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, Order
from app.utils.security import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

def verify_admin(current_user):
    """Ensures only admin users can access the route."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only!")
    return current_user

@router.get("/dashboard")
def admin_dashboard(current_user=Depends(get_current_user)):
    verify_admin(current_user)
    return {"message": "Welcome to Admin Panel"}

@router.get("/products")
def admin_get_products(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Admin can view all products."""
    verify_admin(current_user)
    return db.query(Product).all()

@router.get("/orders")
def admin_get_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Admin can view all orders."""
    verify_admin(current_user)
    return db.query(Order).all()

@router.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Admin can update order status."""
    verify_admin(current_user)
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    
    return {"message": "Order status updated successfully"}
