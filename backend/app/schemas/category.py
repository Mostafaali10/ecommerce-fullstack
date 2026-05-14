"""AR: مخططات التصنيف / EN: Category request/response schemas."""

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    """AR/EN: إنشاء/تحديث تصنيف."""

    name: str


class CategoryResponse(BaseModel):
    """AR/EN: شكل التصنيف في الاستجابة."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
