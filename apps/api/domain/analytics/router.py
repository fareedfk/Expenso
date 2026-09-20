from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from apps.api.core.database import get_db
from apps.api.core.security import get_current_user_id
from apps.api.domain.transactions.models import Transaction
from apps.api.domain.categories.models import Category
from apps.api.domain.analytics.schemas import AnalyticsSummary, CategoryBreakdownItem, MonthlyTrendItem

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/summary", response_model=AnalyticsSummary)
def get_summary(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    today = date.today()
    c_m, c_y = today.month, today.year

    total_inc = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
        Transaction.user_id == user_id, Transaction.type == "income"
    ).scalar() or 0.0

    total_exp = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
        Transaction.user_id == user_id, Transaction.type == "expense"
    ).scalar() or 0.0

    m_inc = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
        Transaction.user_id == user_id, Transaction.type == "income",
        extract("month", Transaction.transaction_date) == c_m, extract("year", Transaction.transaction_date) == c_y
    ).scalar() or 0.0

    m_exp = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
        Transaction.user_id == user_id, Transaction.type == "expense",
        extract("month", Transaction.transaction_date) == c_m, extract("year", Transaction.transaction_date) == c_y
    ).scalar() or 0.0

    t_exp = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
        Transaction.user_id == user_id, Transaction.type == "expense", Transaction.transaction_date == today
    ).scalar() or 0.0

    # Total balance rule: balance only increases when income is added; if 0 income, balance stays 0
    total_bal = round(total_inc - total_exp, 2) if total_inc > 0 else 0.0

    # Monthly savings: only positive savings if income exists
    if m_inc > 0:
        m_sav = round(max(0.0, m_inc - m_exp), 2)
        rate = round((m_sav / m_inc * 100), 1)
    else:
        m_sav = 0.0
        rate = 0.0

    cnt = db.query(Transaction).filter(Transaction.user_id == user_id).count()

    return AnalyticsSummary(
        total_balance=total_bal,
        total_income=round(total_inc, 2),
        total_expense=round(total_exp, 2),
        total_savings=round(max(0.0, total_inc - total_exp) if total_inc > 0 else 0.0, 2),
        monthly_income=round(m_inc, 2),
        monthly_expense=round(m_exp, 2),
        monthly_savings=m_sav,
        today_expense=round(t_exp, 2),
        savings_rate=rate,
        transaction_count=cnt
    )

@router.get("/monthly", response_model=List[MonthlyTrendItem])
def get_monthly_trends(months: int = Query(6, ge=1, le=24), user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    today = date.today()
    results = []
    for i in range(months - 1, -1, -1):
        y = today.year
        m = today.month - i
        while m <= 0: m += 12; y -= 1
        inc = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
            Transaction.user_id == user_id, Transaction.type == "income",
            extract("month", Transaction.transaction_date) == m, extract("year", Transaction.transaction_date) == y
        ).scalar() or 0.0
        exp = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
            Transaction.user_id == user_id, Transaction.type == "expense",
            extract("month", Transaction.transaction_date) == m, extract("year", Transaction.transaction_date) == y
        ).scalar() or 0.0
        results.append(MonthlyTrendItem(
            month_label=datetime(y, m, 1).strftime("%b %Y"), month=m, year=y,
            income=round(inc, 2), expense=round(exp, 2), savings=round(inc - exp, 2)
        ))
    return results

@router.get("/categories", response_model=List[CategoryBreakdownItem])
def get_category_breakdown(
    type: str = Query("expense", pattern="^(expense|income)$"),
    period: str = Query("this_month"),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    today = date.today()
    s_date, e_date = None, today
    if from_date and to_date: s_date, e_date = from_date, to_date
    elif period == "this_week": s_date = today - timedelta(days=today.weekday())
    elif period == "this_month": s_date = date(today.year, today.month, 1)
    elif period == "last_month":
        first_tm = date(today.year, today.month, 1)
        prev_end = first_tm - timedelta(days=1)
        s_date, e_date = date(prev_end.year, prev_end.month, 1), prev_end
    elif period == "3_months": s_date = today - timedelta(days=90)
    elif period == "6_months": s_date = today - timedelta(days=180)

    q = db.query(
        Category.id, Category.name, Category.icon, Category.color,
        func.sum(Transaction.amount).label("total_amt")
    ).join(Transaction, Transaction.category_id == Category.id).filter(
        Transaction.user_id == user_id, Transaction.type == type
    )
    if s_date: q = q.filter(Transaction.transaction_date >= s_date)
    if e_date: q = q.filter(Transaction.transaction_date <= e_date)
    rows = q.group_by(Category.id, Category.name, Category.icon, Category.color).all()
    total_sum = sum(r.total_amt for r in rows) or 0.0

    return [
        CategoryBreakdownItem(
            category_id=r.id, category_name=r.name, category_icon=r.icon or "tag",
            category_color=r.color or "#6366F1", amount=round(float(r.total_amt), 2),
            percentage=round((float(r.total_amt) / total_sum * 100), 1) if total_sum > 0 else 0.0
        ) for r in rows
    ]

@router.get("/calendar")
def get_calendar(month: int = Query(..., ge=1, le=12), year: int = Query(..., ge=2000, le=2100), user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    txs = db.query(Transaction).filter(
        Transaction.user_id == user_id, Transaction.type == "expense",
        extract("month", Transaction.transaction_date) == month, extract("year", Transaction.transaction_date) == year
    ).order_by(Transaction.transaction_date.asc()).all()

    m = {}
    for tx in txs:
        d = tx.transaction_date.strftime("%Y-%m-%d")
        if d not in m: m[d] = {"date": d, "total_expense": 0.0, "count": 0, "items": []}
        m[d]["total_expense"] = round(m[d]["total_expense"] + tx.amount, 2)
        m[d]["count"] += 1
        m[d]["items"].append({
            "id": tx.id, "description": tx.description, "amount": tx.amount,
            "category_name": tx.category.name if tx.category else "Other"
        })
    return m
