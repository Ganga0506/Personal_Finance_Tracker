from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app import transactions 
from app.database import SessionLocal
from app.models import CategoryEnum, Transaction
from pydantic import BaseModel
from datetime import date
import os


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TransactionCreate(BaseModel):
    name: str
    amount: float
    category: CategoryEnum
    date: date

class TransactionResponse(BaseModel):
    id: int
    name: str
    amount: float
    category: CategoryEnum
    date: date

    class Config:
        orm_mode = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ----------------- ROUTES -------------------

# 1. Home Page
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    all_txns = transactions.get_all_transactions(db)
    return templates.TemplateResponse("index.html", {"request": request, "transactions": all_txns})

# 2. Show form on GET to add transaction and also handle POST submission
@app.api_route("/add", methods=["GET", "POST"])
def add_transaction(
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(None),
    amount: float = Form(None),
    category: str = Form(None),
    date: date = Form(None)
):
    if request.method == "GET":
        categories = transactions.get_categories()
        return templates.TemplateResponse("add_transaction.html", {
            "request": request,
            "categories": categories
        })
    
    if amount is not None and amount<0: 
        raise HTTPException(status_code=400, detail="Amount cannot be negative")
    
    try: 
        transaction_data = TransactionCreate(
            name=name,
            amount=amount,
            category=CategoryEnum(category),
            date=date
        )
        data = transaction_data.dict()
        data["date_"] = data.pop("date") 
        transactions.add_transaction(db, **data)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 3. Show all transactions
@app.get("/transactions")
def view_transactions(request: Request, db: Session = Depends(get_db)):
    all_txns = transactions.get_all_transactions(db)
    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "transactions": all_txns
    })

# 4. POST transaction (API, not form)
@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    txn = transactions.add_transaction(db, **transaction.dict())
    return txn

# 5. Get summary (JSON for now)
@app.get("/summary")
def get_summary(budget: float, db: Session = Depends(get_db)):
    return transactions.get_summary(db, budget)

# 6. Get categories (JSON)
@app.get("/categories")
def get_categories():
    return transactions.get_categories()

# 7. Delete transaction
@app.api_route("/delete", methods=["GET", "POST"])
def delete_transaction(
    request: Request,
    db: Session = Depends(get_db),
    id: int = Form(None)
):
    if request.method == "GET":
        all_txns = transactions.get_all_transactions(db)
        return templates.TemplateResponse("delete.html", {
            "request": request,
            "transactions": all_txns
        })

    # Handle POST request (form submission to delete)
    if id is None:
        raise HTTPException(status_code=400, detail="ID is required")

    success = transactions.delete_transaction(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return RedirectResponse(url="/transactions", status_code=303)

# 8. Filter transactions by category
@app.api_route("/category", methods=["GET", "POST"])
def filter_by_category(
    request: Request,
    db: Session = Depends(get_db),
    category: str = Form(None)
):
    if request.method == "GET":
        categories = transactions.get_categories()
        return templates.TemplateResponse("category.html", {
            "request": request,
            "categories": categories
        })
    
    txns = transactions.get_by_category(db, category)
    return templates.TemplateResponse("category.html", {
        "request": request,
        "categories": transactions.get_categories(),
        "transactions": txns,
        "selected_category": category
    })