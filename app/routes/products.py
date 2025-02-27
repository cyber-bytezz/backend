from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse
from typing import List, Optional

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """API to create a new product"""
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully", "product_id": new_product.id}

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """API to get unique product categories"""
    categories = db.query(Product.category).distinct().all()
    return [category[0] for category in categories]  # Convert list of tuples to a list

@router.get("/", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by product name"),
    sort_by: Optional[str] = Query(None, description="Sort by price (asc/desc)")
):
    """API to fetch products with search, sorting, and category filtering"""
    
    print(f"Received filters: category={category}, search={search}, sort_by={sort_by}")  # ✅ Debug log

    query = db.query(Product)

    # ✅ Filter by category (only apply if category is given)
    if category:
        query = query.filter(Product.category == category)

    # ✅ Search by product name (case-insensitive)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # ✅ Sorting (asc/desc)
    if sort_by == "asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "desc":
        query = query.order_by(Product.price.desc())

    products = query.all()
    print(f"Returning {len(products)} products")  # ✅ Debug log
    return products


@router.put("/{product_id}")
def update_product(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    """Admin can update a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return {"message": "Product updated successfully"}

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Admin can delete a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
