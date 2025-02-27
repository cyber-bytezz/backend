from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, OrderItem, Product, Cart, User
from app.utils.security import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["Orders"])

class OrderCreate(BaseModel):
    payment_method: str  # ✅ Expect `payment_method` in request
    shipping_address: str  # ✅ Expect `shipping_address` in request

@router.post("/")
def place_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Places an order from the cart items of the logged-in user."""
    user_id = current_user.id

    # ✅ Ensure cart items are fetched properly
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty. Add items before placing an order.")

    total_price = sum(
        item.quantity * db.query(Product).filter(Product.id == item.product_id).first().price
        for item in cart_items
    )

    # ✅ Ensure valid payment method
    if order_data.payment_method not in ["Credit Card", "UPI", "Net Banking", "Cash on Delivery"]:
        raise HTTPException(status_code=400, detail="Invalid payment method")

    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        payment_status=order_data.payment_method,
        shipping_address=order_data.shipping_address,  # ✅ Store shipping address
        status="Pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # ✅ Add Order Items & Clear Cart
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(order_id=new_order.id, product_id=product.id, quantity=item.quantity, price=product.price)
        db.add(order_item)

    db.commit()

    # ✅ Clear the cart after order placement
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": new_order.id,
        "payment_status": new_order.payment_status,
        "shipping_address": new_order.shipping_address
    }

@router.get("/")
def get_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Retrieve all orders for the logged-in user with product details."""
    user_id = current_user.id
    orders = db.query(Order).filter(Order.user_id == user_id).all()

    if not orders:
        return {"message": "No orders found"}

    response = []
    for order in orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        products = [
            {
                "product_id": item.product_id,
                "name": db.query(Product).filter(Product.id == item.product_id).first().name,
                "quantity": item.quantity,
                "price": item.price,
                "total_price": item.price * item.quantity
            }
            for item in order_items
        ]

        response.append({
            "order_id": order.id,
            "total_price": order.total_price,
            "payment_status": order.payment_status,
            "status": order.status,
            "shipping_address": order.shipping_address,
            "products": products,
            "created_at": order.created_at
        })

    return response

@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Update order status (e.g., Pending → Shipped → Delivered)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only!")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    return {"message": f"Order status updated to {status}"}
