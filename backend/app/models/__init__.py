"""
AR: تجميع النماذج — استيراد هذا الملف يضمن تسجيل الجداول في metadata.
EN: Importing this package ensures all tables are registered on SQLAlchemy metadata.

في `main.py` نستورد: `import app.models` قبل `create_all`.
"""

from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order, OrderItem

__all__ = ["User", "Category", "Product", "Order", "OrderItem"]
