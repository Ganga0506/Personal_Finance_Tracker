from sqlalchemy.orm import Session
from app.models import Transaction, CategoryEnum
from datetime import date

def add_transaction(db: Session, name: str, amount: float, category: CategoryEnum, date_: date):
    if not isinstance(category, CategoryEnum):
        raise ValueError("Invalid category.")
    txn = Transaction( name=name, amount=amount, category=category, date=date_)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn

def get_all_transactions(db):
    return db.query(Transaction).all()