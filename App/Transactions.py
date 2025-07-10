from sqlalchemy.orm import Session
from app.models import Transaction, CategoryEnum
from datetime import date

def get_categories():
    """
    Returns a list of all category names as strings.
    Returns:
        List of category names (str) from CategoryEnum.
    """

    return [category.name for category in CategoryEnum]

def add_transaction(db: Session, name: str, amount: float, category: CategoryEnum, date_: date):
    """
    Adds a new transaction to the database.
    Args:
        db: SQLAlchemy Session object
        name: Transaction name or description
        amount: Transaction amount (float)
        category: CategoryEnum value for the transaction
        date_: Date of the transaction
    Raises:
        ValueError: If category is not a valid CategoryEnum member.
    Returns:
        The created Transaction object.
    """
    if not isinstance(category, CategoryEnum):
        raise ValueError("Invalid category.")
    txn = Transaction( name=name, amount=amount, category=category, date=date_)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn

def get_all_transactions(db):
    """
    Fetches all transactions from the database.
    Args:
        db: SQLAlchemy Session object
    Returns:
        List of all Transaction objects.
    """
    return db.query(Transaction).all()

def get_summary(db: Session, budget: float):
    """
    Calculate total spent and remaining budget.
    Args:
        db: SQLAlchemy Session object
        budget: Total budget amount (float)
    Returns:
        dict with keys "total_spent" and "remaining", rounded to 2 decimals
    """

    transactions = db.query(Transaction).all()
    total_spent = sum(txn.amount for txn in transactions)
    remaining = budget - total_spent
    return {
        "total_spent": round(total_spent, 2),
        "remaining": round(remaining, 2)
    }

def get_by_category(db: Session, category: CategoryEnum):
    """
    Get all transactions for a specific category.
    Args:
        db: SQLAlchemy Session object
        category: CategoryEnum value to filter transactions
    Returns:
        List of Transaction objects in the given category
    """

    return db.query(Transaction).filter(Transaction.category == category).all()

def get_daily_budget(db: Session, budget: float, today: date, end_date: date):
    """
    Calculate daily budget based on remaining budget and days left.
    Args:
        db: SQLAlchemy Session object
        budget: Total budget amount (float)
        today: Current date
        end_date: End date for budgeting period
    Returns:
        Float representing the daily allowed spend, 0 if no days left
    """

    days_left = (end_date - today).days + 1  # include today
    transactions = db.query(Transaction).all()
    incomes = db.query(Income).all()
    
    total_spent = sum(txn.amount for txn in transactions)
    total_income = sum(inc.amount for inc in incomes)

    remaining = total_income - total_spent
    if days_left <= 0:
        return 0.0
    if remaining <= 0:
        return 0.0
    return round(remaining / days_left, 2)

def get_remaining_budget(db: Session, budget: float):
    """
    Calculate remaining budget after spending.
    Args:
        db: SQLAlchemy Session object
        budget: Total budget amount (float)
    Returns:
        Remaining budget as a float rounded to 2 decimals
    """

    total_spent = sum(txn.amount for txn in db.query(Transaction).all())
    total_income = sum(inc.amount for inc in db.query(Income).all())
    remaining = total_income - total_spent
    return round(remaining, 2)

def delete_transaction(db: Session, transaction_id: int):
    """
    Delete a transaction by its ID.
    Args:
        db: SQLAlchemy Session object
        transaction_id: ID of the transaction to delete
    Returns:
        True if deletion succeeded, False if transaction not found
    """

    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if txn:
        db.delete(txn)
        db.commit()
        return True
    return False

def add_income(db: Session, name: str, amount: float, date_: date):
    """
    Add an income transaction.
    Args:
        db: SQLAlchemy Session object
        name: Name/description of income
        amount: Income amount
        date_: Date of income
    Returns:
        The created Transaction object with category INCOME
    """

    return add_transaction(db, name, amount, CategoryEnum.INCOME, date_)