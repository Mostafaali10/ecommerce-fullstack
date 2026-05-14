"""
AR: مسارات المستخدم الحالي — `/users/me`.
EN: Current-user routes — `/users/me`.

يستخدم اعتمادية `get_current_user_entity` التي تعيد كائن ORM `User`.
Uses `get_current_user_entity` which returns the persisted `User` ORM object.
"""

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user_entity
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user_entity)):
    """AR/EN: يعيد بيانات المستخدم المسجل حسب التوكن."""
    return current_user
