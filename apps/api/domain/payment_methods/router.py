from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from apps.api.core.database import get_db
from apps.api.core.security import get_current_user_id
from apps.api.domain.payment_methods.models import PaymentMethod
from apps.api.domain.transactions.models import Transaction
from apps.api.domain.payment_methods.schemas import PaymentMethodCreate, PaymentMethodResponse

router = APIRouter(prefix="/api/payment-methods", tags=["Payment Methods"])

@router.get("/", response_model=List[PaymentMethodResponse])
def get_payment_methods(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return db.query(PaymentMethod).filter(
        or_(PaymentMethod.user_id == user_id, PaymentMethod.user_id.is_(None))
    ).order_by(PaymentMethod.name.asc()).all()

@router.post("/", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment_method(
    pm_data: PaymentMethodCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    existing = db.query(PaymentMethod).filter(
        PaymentMethod.name.ilike(pm_data.name.strip()),
        or_(PaymentMethod.user_id == user_id, PaymentMethod.user_id.is_(None))
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payment method already exists.")

    pm = PaymentMethod(user_id=user_id, name=pm_data.name.strip(), type=pm_data.type or "other")
    db.add(pm)
    db.commit()
    db.refresh(pm)
    return pm

@router.delete("/{pm_id}")
def delete_payment_method(pm_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    pm = db.query(PaymentMethod).filter(PaymentMethod.id == pm_id, PaymentMethod.user_id == user_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Payment method not found.")
    db.query(Transaction).filter(Transaction.payment_method_id == pm_id).update({Transaction.payment_method_id: None})
    db.delete(pm)
    db.commit()
    return {"message": "Payment method deleted."}
