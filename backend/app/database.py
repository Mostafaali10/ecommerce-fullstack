"""
AR: اتصال SQLAlchemy بقاعدة البيانات + تعريف `Base` للنماذج.
EN: SQLAlchemy database connection + declarative `Base` for ORM models.

دورة حياة الجلسة / Session lifecycle:
- لا نفتح جلسة عالمية — نستخدم `get_db` في `app/dependencies/database.py` لكل طلب.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# AR: SQLite يحتاج check_same_thread=False مع FastAPI (خيوط متعددة)
# EN: SQLite needs this flag with FastAPI (multi-threaded server)
_connect_args: dict = {}
if settings.database_url.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, connect_args=_connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
