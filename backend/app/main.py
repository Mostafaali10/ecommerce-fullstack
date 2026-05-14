"""
AR: نقطة دخول FastAPI — إنشاء التطبيق وربط المسارات والـ CORS.
EN: FastAPI entrypoint — app factory, routers, and CORS configuration.

تشغيل محلي / Local run (from `backend/` folder):
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import Base, engine

# AR: استيراد النماذج يُسجّل الجداول على `Base.metadata` قبل `create_all`
# EN: Import models so tables are registered on `Base.metadata` before `create_all`
import app.models  # noqa: F401

from app.routers import auth, categories, orders, products, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    AR: يُنفَّذ عند بدء التوقف — هنا ننشئ الجداول تلقائياً (سهل للمبتدئين).
    EN: Runs on startup/shutdown — here we auto-create tables (beginner-friendly).

    في الإنتاج استخدم أداة هجرات مثل Alembic بدلاً من `create_all` فقط.
    In production prefer Alembic migrations instead of only `create_all`.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="E-Commerce API",
    description="REST API: authentication, users, categories, products, and orders.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AR: ترتيب الربط لا يغيّر عناوين URL طالما البادئات مختلفة
# EN: Include order does not change URLs as long as prefixes differ
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
