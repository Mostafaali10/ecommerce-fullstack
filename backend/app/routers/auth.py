"""
AR: مسارات المصادقة — تسجيل وتسجيل دخول.
EN: Authentication routes — register + login.

المنطق مطابق للنسخة القديمة في `app/routes/auth.py` (bcrypt + توكن JWT).
"""

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    AR: ينشئ مستخدماً جديداً إذا لم يكن الإيميل مستخدماً.
    EN: Creates a new user if the email is not already taken.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # AR: bcrypt مباشرة لتفادي مشاكل توافق passlib في بعض البيئات
    # EN: raw bcrypt to avoid passlib compatibility issues on some setups
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # AR: منطق تجريبي — إيميل فيه "admin" يصبح مديراً
    # EN: demo rule — emails containing "admin" become admin role
    enforced_role = "admin" if "admin" in user.email.lower() else "customer"
    new_user = User(email=user.email, password=hashed_password, role=enforced_role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User created as {enforced_role}"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    AR: يتحقق من الإيميل/كلمة المرور ويعيد JWT.
    EN: Validates credentials and returns a JWT access token.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({"user_id": db_user.id, "role": db_user.role})
    return {"message": "Login success", "token": token}
