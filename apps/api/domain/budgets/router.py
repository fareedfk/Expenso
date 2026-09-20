from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import extract, func

from apps.api.core.database import get_db
from apps.api.core.security import get_current_user_id
from apps.api.domain.budgets.models import Budget
from apps.api.domain.categories.models import Category
from apps.api.domain.transactions.models import Transaction
from apps.api.domain.budgets.schemas import BudgetCreate, BudgetUpdate, BudgetProgressResponse, BudgetResponse

router = APIRouter(prefix="/api/budgets", tags=["Budgets"])

@router.get("/", response_model=List[BudgetProgressResponse])
def get_budgets(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000, le=2100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    today = date.today()
    t_month = month or today.month
    t_year = year or today.year

    budgets = db.query(Budget).options(joinedload(Budget.category)).filter(
        Budget.user_id == user_id, Budget.month == t_month, Budget.year == t_year
    ).all()

    results = []
    for b in budgets:
        spent = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
            Transaction.user_id == user_id,
            Transaction.category_id == b.category_id,
            Transaction.type == "expense",
            extract("month", Transaction.transaction_date) == t_month,
            extract("year", Transaction.transaction_date) == t_year
        ).scalar() or 0.0

        remaining = max(0.0, b.amount - spent)
        pct = round((spent / b.amount) * 100, 1) if b.amount > 0 else 0.0
        status_str = "exceeded" if pct > 100 else ("warning" if pct >= 80 else "normal")

        results.append(BudgetProgressResponse(
            id=b.id, user_id=b.user_id, category_id=b.category_id, amount=b.amount,
            month=b.month, year=b.year, created_at=b.created_at, category=b.category,
            spent=round(spent, 2), remaining=round(remaining, 2), percentage=pct, status=status_str
        ))
    return results

@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(data: BudgetCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise HTTPException(status_code=400, detail="Invalid category.")

    existing = db.query(Budget).filter(
        Budget.user_id == user_id, Budget.category_id == data.category_id,
        Budget.month == data.month, Budget.year == data.year
    ).first()
    if existing:
        existing.amount = data.amount
        db.commit()
        db.refresh(existing)
        return existing

    budget = Budget(user_id=user_id, category_id=data.category_id, amount=data.amount, month=data.month, year=data.year)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).first()
    if not budget: raise HTTPException(status_code=404, detail="Budget not found.")
    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted."}
