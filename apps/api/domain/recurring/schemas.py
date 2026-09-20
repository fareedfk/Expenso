from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field
from apps.api.domain.categories.schemas import CategoryResponse

class RecurringExpenseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    frequency: str = Field(..., pattern="^(daily|weekly|monthly|yearly)$")
    start_date: date = Field(default_factory=date.today)
    end_date: Optional[date] = None
    is_active: bool = True

class RecurringExpenseCreate(RecurringExpenseBase):
    pass

class RecurringExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None

class RecurringExpenseResponse(RecurringExpenseBase):
    id: int
    user_id: int
    next_date: date
    category: Optional[CategoryResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
