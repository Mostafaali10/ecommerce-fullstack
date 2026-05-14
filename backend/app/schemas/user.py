"""AR: مخططات Pydantic للمستخدم / EN: Pydantic schemas for users (auth + responses)."""

from pydantic import BaseModel, EmailStr, ConfigDict


class UserRegister(BaseModel):
    """AR/EN: بيانات التسجيل — إيميل + كلمة مرور."""

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """AR/EN: بيانات تسجيل الدخول."""

    email: EmailStr
    password: str


class UserOut(BaseModel):
    """AR/EN: ما نُرجعه للعميل (بدون كلمة المرور)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: str
