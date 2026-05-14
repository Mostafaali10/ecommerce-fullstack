"""AR: مخططات المنتج / EN: Product request/response schemas."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """AR/EN: إنشاء/تحديث منتج — الاسم، التصنيف، المخزون."""

    name: str
    category_id: int
    stock: int = Field(..., ge=0)


class ProductResponse(BaseModel):
    """AR/EN: شكل المنتج في الاستجابة JSON."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category_id: Optional[int] = None
    stock: int
