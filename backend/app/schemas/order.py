"""AR: مخططات الطلب / EN: Order request/response schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    """AR/EN: عنصر واحد داخل طلب جديد (معرف المنتج + الكمية)."""

    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    """AR/EN: طلب جديد = قائمة عناصر."""

    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    """AR/EN: سطر داخل الطلب في الاستجابة — `product_name` اختياري للتوافق."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    product_name: Optional[str] = None


class OrderResponse(BaseModel):
    """AR/EN: الطلب كامل مع عناصره."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse]
