from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cart, Product, User
from app.schemas import CartItem
from app.utils.security import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# ✅ Add product to cart
@router.post("/")
def add_to_cart(
    cart_item: CartItem,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Adds a product to the logged-in user's cart."""
    user_id = current_user.id  

    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart_entry = db.query(Cart).filter(
        Cart.user_id == user_id, Cart.product_id == cart_item.product_id
    ).first()

    if cart_entry:
        cart_entry.quantity += cart_item.quantity  
    else:
        cart_entry = Cart(user_id=user_id, product_id=cart_item.product_id, quantity=cart_item.quantity)
        db.add(cart_entry)

    db.commit()
    db.refresh(cart_entry)

    return {
        "message": "Product added to cart successfully",
        "cart_item": {
            "id": cart_entry.id,
            "user_id": cart_entry.user_id,
            "product_id": cart_entry.product_id,
            "quantity": cart_entry.quantity,
            "total_price": product.price * cart_entry.quantity
        }
    }

# ✅ View all cart items
@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves the user's cart items with product details."""
    user_id = current_user.id
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    response = []
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        response.append({
            "id": item.id,
            "user_id": user_id,
            "product_id": item.product_id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
            "total_price": product.price * item.quantity
        })

    return response

# ✅ Decrease product quantity in cart
@router.put("/{product_id}/decrease")
def decrease_cart_item_quantity(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Decreases the quantity of a product in the cart."""
    user_id = current_user.id
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id, Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        db.commit()
        return {"message": "Product quantity decreased", "new_quantity": cart_item.quantity}
    else:
        db.delete(cart_item)  # Remove item if quantity is 1
        db.commit()
        return {"message": "Product removed from cart"}

# ✅ Remove a product from cart
@router.delete("/{product_id}")
def remove_cart_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Removes an item from the cart"""
    user_id = current_user.id
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id, Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "Product removed from cart"}
