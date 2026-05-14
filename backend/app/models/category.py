"""
AR: نموذج التصنيف — جدول `categories`.
EN: Category ORM model — maps to the `categories` table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # AR: المنتجات المرتبطة (علاقة عكسية من Product.category)
    # EN: Related products (reverse side via `Product.category`)
    products = relationship("Product", back_populates="category")
