from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.core.database import get_db
from apps.api.core.security import hash_password, verify_password, create_access_token, get_current_user_id
from apps.api.domain.auth.models import User
from apps.api.domain.categories.models import Category
from apps.api.domain.payment_methods.models import PaymentMethod
from apps.api.domain.auth.schemas import (
    UserRegister, UserLogin, UserPasswordChange, UserProfileUpdate, UserResponse, Token
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

DEFAULT_EXPENSE_CATS = [
    ("Food", "utensils", "#EF4444"), ("Transport", "car", "#F59E0B"),
    ("Shopping", "shopping-bag", "#EC4899"), ("Rent", "home", "#8B5CF6"),
    ("Bills", "zap", "#3B82F6"), ("Entertainment", "film", "#10B981"),
    ("Health", "activity", "#14B8A6"), ("Education", "book-open", "#6366F1"),
    ("Travel", "plane", "#06B6D4"), ("Work", "briefcase", "#64748B"),
    ("Others", "package", "#71717A"),
]

DEFAULT_INCOME_CATS = [
    ("Salary", "wallet", "#10B981"), ("Freelancing", "laptop", "#3B82F6"),
    ("Allowance", "gift", "#F59E0B"), ("Business", "trending-up", "#8B5CF6"),
    ("Investments", "pie-chart", "#EC4899"), ("Other Income", "plus-circle", "#14B8A6"),
]

DEFAULT_PMS = [
    ("UPI", "upi"), ("Cash", "cash"), ("Debit Card", "card"),
    ("Credit Card", "card"), ("Bank Transfer", "bank")
]

def seed_defaults(db: Session, user_id: int):
    for name, icon, color in DEFAULT_EXPENSE_CATS:
        db.add(Category(user_id=user_id, name=name, icon=icon, color=color, type="expense", is_default=True))
    for name, icon, color in DEFAULT_INCOME_CATS:
        db.add(Category(user_id=user_id, name=name, icon=icon, color=color, type="income", is_default=True))
    for name, p_type in DEFAULT_PMS:
        db.add(PaymentMethod(user_id=user_id, name=name, type=p_type))
    db.commit()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email.lower()).first():
        raise HTTPException(status_code=400, detail="Email already registered.")

    user = User(
        name=user_data.name.strip(),
        email=user_data.email.lower().strip(),
        password_hash=hash_password(user_data.password),
        currency=user_data.currency or "INR"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    seed_defaults(db, user.id)
    token = create_access_token(user.id)
    return Token(access_token=token, token_type="bearer", user=user)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email.lower().strip()).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    token = create_access_token(user.id)
    return Token(access_token=token, token_type="bearer", user=user)

@router.get("/me", response_model=UserResponse)
def get_me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.put("/profile", response_model=UserResponse)
def update_profile(data: UserProfileUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if data.name: user.name = data.name.strip()
    if data.currency: user.currency = data.currency.strip()
    db.commit()
    db.refresh(user)
    return user

@router.post("/change-password")
def change_password(data: UserPasswordChange, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password incorrect.")
    user.password_hash = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully."}
