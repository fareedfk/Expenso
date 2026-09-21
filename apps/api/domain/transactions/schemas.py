from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
from apps.api.domain.categories.schemas import CategoryResponse
from apps.api.domain.payment_methods.schemas import PaymentMethodResponse

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: str = Field(..., pattern="^(expense|income)$")
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    transaction_date: date = Field(default_factory=date.today)
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[str] = Field(None, pattern="^(expense|income)$")
    description: Optional[str] = None
    category_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    transaction_date: Optional[date] = None
    notes: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    category: Optional[CategoryResponse] = None
    payment_method: Optional[PaymentMethodResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    total: int
    page: int
    limit: int
    transactions: List[TransactionResponse]
