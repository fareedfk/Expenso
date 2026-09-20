from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from apps.api.domain.categories.schemas import CategoryResponse

class BudgetBase(BaseModel):
    category_id: int
    amount: float = Field(..., gt=0)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    amount: float = Field(..., gt=0)

class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    category: Optional[CategoryResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True

class BudgetProgressResponse(BudgetResponse):
    spent: float
    remaining: float
    percentage: float
    status: str
