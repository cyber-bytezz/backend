from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully", "product_id": new_product.id}

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Product.category).distinct().all()
    return [category[0] for category in categories]  # Convert list of tuples to a list

@router.get("/", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    category: str = Query(None, description="Filter by category"),
    min_price: float = Query(None, description="Filter by minimum price"),
    max_price: float = Query(None, description="Filter by maximum price")
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.all()
    return products
