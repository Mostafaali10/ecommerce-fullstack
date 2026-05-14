"""
AR: مسارات المنتجات — CRUD + تصفية بسيطة + ترقيم صفحات.
EN: Product routes — CRUD + simple filters + pagination.

المسارات تبقى `/products` كما في النسخة القديمة (ملف `product.py`).
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import admin_only, get_token_payload
from app.dependencies.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(tags=["Products"])


@router.post("/products", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    _admin: dict = Depends(admin_only),
):
    if product.stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    new_product = Product(
        name=product.name,
        category_id=product.category_id,
        stock=product.stock,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/products", response_model=List[ProductResponse])
def get_products(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_token_payload),
):
    query = db.query(Product)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()


@router.get("/products/{id}", response_model=ProductResponse)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_token_payload),
):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{id}", response_model=ProductResponse)
def update_product(
    id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    _admin: dict = Depends(admin_only),
):
    if product.stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    existing = db.query(Product).filter(Product.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    existing.name = product.name
    existing.category_id = product.category_id
    existing.stock = product.stock
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/products/{id}", status_code=200)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    _admin: dict = Depends(admin_only),
):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Deleted successfully"}
