from typing import Optional
from pydantic import BaseModel

class AnalyticsSummary(BaseModel):
    total_balance: float
    total_income: float
    total_expense: float
    total_savings: float
    monthly_income: float
    monthly_expense: float
    monthly_savings: float
    today_expense: float
    savings_rate: float
    transaction_count: int

class CategoryBreakdownItem(BaseModel):
    category_id: Optional[int]
    category_name: str
    category_icon: str
    category_color: str
    amount: float
    percentage: float

class MonthlyTrendItem(BaseModel):
    month_label: str
    month: int
    year: int
    income: float
    expense: float
    savings: float
