import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload

from apps.api.core.database import get_db
from apps.api.core.security import get_current_user_id
from apps.api.domain.transactions.models import Transaction

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.get("/csv")
def export_csv(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    txs = db.query(Transaction).options(
        joinedload(Transaction.category), joinedload(Transaction.payment_method)
    ).filter(Transaction.user_id == user_id).order_by(Transaction.transaction_date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Date", "Description", "Category", "Payment Method", "Type", "Amount", "Notes"])

    for tx in txs:
        writer.writerow([
            tx.id, tx.transaction_date.strftime("%Y-%m-%d"), tx.description,
            tx.category.name if tx.category else "Uncategorized",
            tx.payment_method.name if tx.payment_method else "N/A",
            tx.type.capitalize(), f"{tx.amount:.2f}", tx.notes or ""
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenso_transactions.csv"}
    )
