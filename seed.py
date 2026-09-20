from datetime import date, timedelta
from sqlalchemy.orm import Session

from apps.api.core.database import SessionLocal, init_database, Base
from apps.api.core.security import hash_password
from apps.api.domain.auth.models import User
from apps.api.domain.categories.models import Category
from apps.api.domain.payment_methods.models import PaymentMethod
from apps.api.domain.transactions.models import Transaction
from apps.api.domain.budgets.models import Budget
from apps.api.domain.recurring.models import RecurringExpense
from apps.api.domain.auth.router import seed_defaults

def seed_demo_data():
    init_database()
    Base.metadata.create_all(bind=SessionLocal().get_bind())
    db: Session = SessionLocal()

    demo_email = "demo@expenso.com"
    existing_user = db.query(User).filter(User.email == demo_email).first()
    if existing_user:
        print(f"Demo user already exists: {demo_email}")
        db.close()
        return

    print("Creating demo user...")
    user = User(
        name="Sameer",
        email=demo_email,
        password_hash=hash_password("demo123"),
        currency="INR"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    seed_defaults(db, user.id)

    cats = db.query(Category).filter(Category.user_id == user.id).all()
    cat_map = {c.name: c.id for c in cats}
    pms = db.query(PaymentMethod).filter(PaymentMethod.user_id == user.id).all()
    pm_map = {p.name: p.id for p in pms}

    today = date.today()
    sample_records = [
        {"desc": "Monthly Salary", "amount": 65000, "type": "income", "cat": "Salary", "pm": "Bank Transfer", "days_ago": 18},
        {"desc": "Freelance Web Project", "amount": 18500, "type": "income", "cat": "Freelancing", "pm": "UPI", "days_ago": 10},
        {"desc": "Previous Month Salary", "amount": 65000, "type": "income", "cat": "Salary", "pm": "Bank Transfer", "days_ago": 48},
        {"desc": "Stock Dividend", "amount": 3200, "type": "income", "cat": "Investments", "pm": "Bank Transfer", "days_ago": 25},
        {"desc": "Apartment Rent", "amount": 16000, "type": "expense", "cat": "Rent", "pm": "Bank Transfer", "days_ago": 18},
        {"desc": "Electricity & Water Bill", "amount": 2450, "type": "expense", "cat": "Bills", "pm": "UPI", "days_ago": 12},
        {"desc": "High Speed Fiber Internet", "amount": 999, "type": "expense", "cat": "Bills", "pm": "UPI", "days_ago": 14},
        {"desc": "Dinner at Barbeque Nation", "amount": 1450, "type": "expense", "cat": "Food", "pm": "Credit Card", "days_ago": 1},
        {"desc": "Grocery & Vegetables", "amount": 1850, "type": "expense", "cat": "Shopping", "pm": "UPI", "days_ago": 2},
        {"desc": "Uber to Airport", "amount": 680, "type": "expense", "cat": "Transport", "pm": "UPI", "days_ago": 3},
        {"desc": "Weekend Movie Tickets", "amount": 800, "type": "expense", "cat": "Entertainment", "pm": "Debit Card", "days_ago": 6},
        {"desc": "Pharmacy & Vitamins", "amount": 650, "type": "expense", "cat": "Health", "pm": "UPI", "days_ago": 7},
        {"desc": "Petrol for Car", "amount": 2500, "type": "expense", "cat": "Transport", "pm": "Credit Card", "days_ago": 8},
        {"desc": "Swiggy Lunch Order", "amount": 320, "type": "expense", "cat": "Food", "pm": "UPI", "days_ago": 0},
    ]

    for item in sample_records:
        db.add(Transaction(
            user_id=user.id, amount=item["amount"], type=item["type"], description=item["desc"],
            category_id=cat_map.get(item["cat"]), payment_method_id=pm_map.get(item["pm"]),
            transaction_date=today - timedelta(days=item["days_ago"]), notes="Demo transaction"
        ))

    budgets = [
        {"cat": "Food", "amount": 8000}, {"cat": "Rent", "amount": 16000},
        {"cat": "Bills", "amount": 4000}, {"cat": "Shopping", "amount": 7000},
        {"cat": "Transport", "amount": 4500}, {"cat": "Entertainment", "amount": 3000},
    ]
    for b in budgets:
        if b["cat"] in cat_map:
            db.add(Budget(user_id=user.id, category_id=cat_map[b["cat"]], amount=b["amount"], month=today.month, year=today.year))

    recurring = [
        {"name": "Netflix Premium", "amount": 649, "cat": "Entertainment", "freq": "monthly"},
        {"name": "Spotify Family", "amount": 179, "cat": "Entertainment", "freq": "monthly"},
        {"name": "Gym Membership", "amount": 2000, "cat": "Health", "freq": "monthly"},
    ]
    for r in recurring:
        db.add(RecurringExpense(
            user_id=user.id, name=r["name"], amount=r["amount"], category_id=cat_map.get(r["cat"]),
            payment_method_id=pm_map.get("Credit Card"), frequency=r["freq"],
            start_date=today, next_date=today + timedelta(days=10), is_active=True
        ))

    db.commit()
    db.close()
    print("[OK] Demo seed completed successfully!")
    print("  Login: demo@expenso.com | Password: demo123")

if __name__ == "__main__":
    seed_demo_data()
