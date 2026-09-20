from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from apps.api.core.database import get_db
from apps.api.core.security import get_current_user_id
from apps.api.domain.categories.models import Category
from apps.api.domain.transactions.models import Transaction
from apps.api.domain.categories.schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    type: Optional[str] = Query(None, pattern="^(expense|income)$"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    query = db.query(Category).filter(or_(Category.user_id == user_id, Category.user_id.is_(None)))
    if type: query = query.filter(Category.type == type)
    return query.order_by(Category.name.asc()).all()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_data: CategoryCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    existing = db.query(Category).filter(
        Category.name.ilike(cat_data.name.strip()),
        Category.type == cat_data.type,
        or_(Category.user_id == user_id, Category.user_id.is_(None))
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists.")

    cat = Category(
        user_id=user_id,
        name=cat_data.name.strip(),
        icon=cat_data.icon or "tag",
        color=cat_data.color or "#6366F1",
        type=cat_data.type,
        is_default=False
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.put("/{cat_id}", response_model=CategoryResponse)
def update_category(
    cat_id: int,
    data: CategoryUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    cat = db.query(Category).filter(Category.id == cat_id, Category.user_id == user_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(cat, k, v)
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{cat_id}")
def delete_category(
    cat_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    cat = db.query(Category).filter(Category.id == cat_id, Category.user_id == user_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    db.query(Transaction).filter(Transaction.category_id == cat_id).update({Transaction.category_id: None})
    db.delete(cat)
    db.commit()
    return {"message": "Category deleted."}
