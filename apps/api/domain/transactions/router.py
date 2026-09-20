from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from apps.api.core.database import get_db
from apps.api.core.security import get_current_user_id
from apps.api.domain.transactions.models import Transaction
from apps.api.domain.categories.models import Category
from apps.api.domain.payment_methods.models import PaymentMethod
from apps.api.domain.transactions.schemas import (
    TransactionCreate, TransactionUpdate, TransactionResponse, TransactionListResponse
)

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.get("/", response_model=TransactionListResponse)
def list_transactions(
    type: Optional[str] = Query(None, pattern="^(expense|income)$"),
    category_id: Optional[int] = Query(None),
    payment_method_id: Optional[int] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    min_amount: Optional[float] = Query(None, ge=0),
    max_amount: Optional[float] = Query(None, ge=0),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=500),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if type: query = query.filter(Transaction.type == type)
    if category_id: query = query.filter(Transaction.category_id == category_id)
    if payment_method_id: query = query.filter(Transaction.payment_method_id == payment_method_id)
    if from_date: query = query.filter(Transaction.transaction_date >= from_date)
    if to_date: query = query.filter(Transaction.transaction_date <= to_date)
    if min_amount is not None: query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None: query = query.filter(Transaction.amount <= max_amount)
    if search:
        s = f"%{search.strip()}%"
        query = query.filter(or_(Transaction.description.ilike(s), Transaction.notes.ilike(s)))

    total = query.count()
    txs = (
        query.options(joinedload(Transaction.category), joinedload(Transaction.payment_method))
        .order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return TransactionListResponse(total=total, page=page, limit=limit, transactions=txs)

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if data.category_id and not db.query(Category).filter(
        Category.id == data.category_id, or_(Category.user_id == user_id, Category.user_id.is_(None))
    ).first():
        raise HTTPException(status_code=400, detail="Invalid category.")

    if data.payment_method_id and not db.query(PaymentMethod).filter(
        PaymentMethod.id == data.payment_method_id, or_(PaymentMethod.user_id == user_id, PaymentMethod.user_id.is_(None))
    ).first():
        raise HTTPException(status_code=400, detail="Invalid payment method.")

    tx = Transaction(
        user_id=user_id,
        amount=data.amount,
        type=data.type,
        description=data.description.strip(),
        category_id=data.category_id,
        payment_method_id=data.payment_method_id,
        transaction_date=data.transaction_date,
        notes=data.notes.strip() if data.notes else None
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return db.query(Transaction).options(
        joinedload(Transaction.category), joinedload(Transaction.payment_method)
    ).filter(Transaction.id == tx.id).first()

@router.get("/{tx_id}", response_model=TransactionResponse)
def get_transaction(tx_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    tx = db.query(Transaction).options(
        joinedload(Transaction.category), joinedload(Transaction.payment_method)
    ).filter(Transaction.id == tx_id, Transaction.user_id == user_id).first()
    if not tx: raise HTTPException(status_code=404, detail="Transaction not found.")
    return tx

@router.put("/{tx_id}", response_model=TransactionResponse)
def update_transaction(
    tx_id: int,
    data: TransactionUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    tx = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == user_id).first()
    if not tx: raise HTTPException(status_code=404, detail="Transaction not found.")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(tx, k, v)
    db.commit()
    db.refresh(tx)
    return db.query(Transaction).options(
        joinedload(Transaction.category), joinedload(Transaction.payment_method)
    ).filter(Transaction.id == tx.id).first()

@router.delete("/{tx_id}")
def delete_transaction(tx_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == user_id).first()
    if not tx: raise HTTPException(status_code=404, detail="Transaction not found.")
    backup = {
        "amount": tx.amount, "type": tx.type, "description": tx.description,
        "category_id": tx.category_id, "payment_method_id": tx.payment_method_id,
        "transaction_date": str(tx.transaction_date), "notes": tx.notes
    }
    db.delete(tx)
    db.commit()
    return {"message": "Transaction deleted.", "deleted_data": backup}
