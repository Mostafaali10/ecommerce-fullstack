"""
AR: نموذج المنتج — جدول `products`.
EN: Product ORM model — maps to the `products` table.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # AR: المخزون — كان مستخدماً في المسارات لكن العمود ناقص في النسخة القديمة
    # EN: Stock field — required by routes; legacy model file was missing this column
    stock = Column(Integer, nullable=False, default=0, server_default="0")

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    order_items = relationship("OrderItem", back_populates="product")
