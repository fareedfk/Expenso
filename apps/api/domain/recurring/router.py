from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from apps.api.core.database import get_db
from apps.api.core.security import get_current_user_id
from apps.api.domain.recurring.models import RecurringExpense
from apps.api.domain.transactions.models import Transaction
from apps.api.domain.recurring.schemas import (
    RecurringExpenseCreate, RecurringExpenseUpdate, RecurringExpenseResponse
)

router = APIRouter(prefix="/api/recurring", tags=["Recurring Expenses"])

def compute_next_date(cur: date, freq: str) -> date:
    if freq == "daily": return cur + timedelta(days=1)
    if freq == "weekly": return cur + timedelta(days=7)
    if freq == "monthly":
        y = cur.year + (cur.month // 12)
        m = (cur.month % 12) + 1
        return date(y, m, min(cur.day, 28))
    if freq == "yearly":
        return date(cur.year + 1, cur.month, min(cur.day, 28))
    return cur + timedelta(days=30)

@router.get("/", response_model=List[RecurringExpenseResponse])
def get_recurring_expenses(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return db.query(RecurringExpense).options(
        joinedload(RecurringExpense.category)
    ).filter(RecurringExpense.user_id == user_id).order_by(RecurringExpense.next_date.asc()).all()

@router.post("/", response_model=RecurringExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_recurring_expense(data: RecurringExpenseCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    rec = RecurringExpense(
        user_id=user_id, name=data.name.strip(), amount=data.amount,
        category_id=data.category_id, payment_method_id=data.payment_method_id,
        frequency=data.frequency, start_date=data.start_date, end_date=data.end_date,
        next_date=data.start_date, is_active=data.is_active
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return db.query(RecurringExpense).options(joinedload(RecurringExpense.category)).filter(RecurringExpense.id == rec.id).first()

@router.post("/process-due")
def process_due(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    today = date.today()
    due_items = db.query(RecurringExpense).filter(
        RecurringExpense.user_id == user_id, RecurringExpense.is_active == True, RecurringExpense.next_date <= today
    ).all()

    processed = []
    for item in due_items:
        if item.end_date and item.next_date > item.end_date:
            item.is_active = False
            continue
        tx = Transaction(
            user_id=user_id, amount=item.amount, type="expense", description=f"{item.name} (Recurring)",
            category_id=item.category_id, payment_method_id=item.payment_method_id,
            transaction_date=item.next_date, notes=f"Subscription: {item.frequency}"
        )
        db.add(tx)
        processed.append(item.name)
        item.next_date = compute_next_date(item.next_date, item.frequency)

    db.commit()
    return {"processed_count": len(processed), "items": processed}

@router.delete("/{rec_id}")
def delete_recurring(rec_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    rec = db.query(RecurringExpense).filter(RecurringExpense.id == rec_id, RecurringExpense.user_id == user_id).first()
    if not rec: raise HTTPException(status_code=404, detail="Recurring subscription not found.")
    db.delete(rec)
    db.commit()
    return {"message": "Recurring subscription deleted."}
