from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PaymentMethodBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: Optional[str] = "other"

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodResponse(PaymentMethodBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
