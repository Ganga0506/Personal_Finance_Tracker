# delete_income_txns.py
from app.database import SessionLocal
from app.models import Transaction, CategoryEnum

def delete_income_transactions():
    db = SessionLocal()
    try:
        # Delete old transactions with category='INCOME'
        txns = db.query(Transaction).filter(Transaction.category == "INCOME").all()
        print(f"Found {len(txns)} income transactions")

        for txn in txns:
            db.delete(txn)
        db.commit()
        print("Deleted.")
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    delete_income_transactions()

