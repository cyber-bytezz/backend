from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, Cart, Product, OrderItem
from app.schemas import OrderCreate
from app.utils.security import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def place_order(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Places an order from the cart items of the logged-in user."""
    user_id = current_user.id

    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty. Add items before placing an order.")

    total_price = 0
    order_items = []

    # ✅ Create new order first
    new_order = Order(user_id=user_id, total_price=0)  # ✅ Initialize total_price as 0
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")

        order_item = OrderItem(
            order_id=new_order.id,  # ✅ Assign the correct order ID
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)
        total_price += product.price * item.quantity

    # ✅ Update order total price after items are added
    new_order.total_price = total_price
    db.commit()

    # ✅ Clear the user's cart
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": new_order.id,
        "total_price": total_price
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
            "products": products,
            "created_at": order.created_at
        })

    return response
