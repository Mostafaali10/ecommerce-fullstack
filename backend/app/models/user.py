"""
AR: نموذج المستخدم — جدول `users`.
EN: User ORM model — maps to the `users` table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")

    # AR: علاقة واحد-كثير مع الطلبات — `back_populates` يربط الجانبين بأمان
    # EN: One-to-many with orders — `back_populates` links both sides explicitly
    orders = relationship("Order", back_populates="user")
