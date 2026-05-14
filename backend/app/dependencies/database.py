"""
AR: اعتمادية قاعدة البيانات — جلسة لكل طلب ثم إغلاق تلقائي.
EN: Database dependency — one DB session per request, closed automatically.

هذا نفس منطق `get_db` القديم في `database.py` لكن منفصل ليكون أوضح للمبتدئين.
This mirrors the old `get_db` helper but lives under `dependencies/` for clarity.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
