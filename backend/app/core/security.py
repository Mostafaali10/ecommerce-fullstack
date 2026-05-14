"""
AR: إنشاء وفك ترميز JWT + اعتماديات FastAPI للتوكن.
EN: JWT creation/decoding + FastAPI security dependencies.

ملاحظة / Note:
- `try_decode_access_token` يعيد None عند انتهاء الصلاحية (مناسب لـ `/users/me` مع رسالة أوضح)
- `decode_access_token_or_raise` يعيد 401 مباشرة (مناسب لمسارات الإدارة والمنتجات)
"""

from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

# AR: مخطط أمان HTTP Bearer — يظهر زر Authorize في Swagger
# EN: HTTP Bearer security scheme — enables Authorize button in Swagger UI
security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """
    AR: ينشئ JWT يحتوي على `data` + وقت انتهاء (`exp`).
    EN: Creates a JWT containing `data` plus expiration (`exp`).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def try_decode_access_token(token: str) -> dict | None:
    """
    AR: يفك الترميز بهدوء — None إذا كان منتهي أو غير صالح (مثل الكود القديم في users).
    EN: Lenient decode — returns None if expired/invalid (matches legacy users router).
    """
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def decode_access_token_or_raise(token: str) -> dict:
    """
    AR: يفك الترميز أو يرفع 401 — مثل سلوك `auth_dependency` القديم.
    EN: Strict decode or 401 — matches legacy `auth_dependency` behavior.
    """
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    AR: يعتمد على ترويسة Authorization: Bearer <token> ويعيد payload.
    EN: Depends on `Authorization: Bearer <token>` and returns the JWT payload dict.
    """
    return decode_access_token_or_raise(credentials.credentials)


def admin_only(current_user: dict = Depends(get_token_payload)) -> dict:
    """
    AR: يسمح فقط لمستخدم بدور admin — وإلا 403.
    EN: Allows only users with role == admin — otherwise 403.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user
