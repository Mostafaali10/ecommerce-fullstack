"""
AR: اعتماديات الهوية — ربط مسارات `/users/me` بنموذج المستخدم في DB.
EN: Identity dependencies — bridge `/users/me` to the persisted `User` model.

لماذا ملف منفصل عن `core/security.py`؟
- `core/security.py` = أدوات JWT عامة
- `dependencies/auth.py` = اعتماديات تستخدم ORM (تحتاج `get_db`)
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import security, try_decode_access_token
from app.dependencies.database import get_db
from app.models.user import User


def get_current_user_entity(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    AR: يتحقق من التوكن ثم يجلب صف المستخدم من الجدول (ليس فقط payload).
    EN: Validates JWT then loads the `User` row (not only the token payload).
    """
    payload = try_decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
