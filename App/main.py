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
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,})

# 2. Show form to add transaction
@app.post("/add")
def add_form(request: Request):
    categories = transactions.get_categories()
    return templates.TemplateResponse("add_transaction.html", {
        "request": request,
        "categories": categories
    })

# 3. Handle form submission from /add
def submit_form(
    request: Request,
    name: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    date: date = Form(...),
    db: Session = Depends(get_db)
):
    if amount < 0:
        raise HTTPException(status_code=400, detail="Amount cannot be negative")
    
    try:
        transaction_data = TransactionCreate(
            name=name,
            amount=amount,
            category=CategoryEnum(category),
            date=date
        )
        transactions.add_transaction(db, **transaction_data.dict())
        return RedirectResponse(url="/transactions", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# 4. Show all transactions
@app.get("/transactions")
def view_transactions(request: Request, db: Session = Depends(get_db)):
    all_txns = transactions.get_all_transactions(db)
    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "transactions": all_txns
    })

# 5. POST transaction (API, not form)
@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    txn = transactions.add_transaction(db, **transaction.dict())
    return txn

# 6. Get summary (JSON for now)
@app.get("/summary")
def get_summary(budget: float, db: Session = Depends(get_db)):
    return transactions.get_summary(db, budget)

# 7. Get categories (JSON)
@app.get("/categories")
def get_categories():
    return transactions.get_categories()
