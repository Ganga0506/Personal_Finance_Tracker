from fastapi import FastAPI, Request, Depends, HTTPException
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # points to app/
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello from FastAPI + Jinja2!"})

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

@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        txn = transactions.add_transaction(
            db=db,
            name=transaction.name,
            amount=transaction.amount,
            category=transaction.category,
            date_=transaction.date
        )
        return txn
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions", response_model=List[TransactionResponse])
def read_transactions(db: Session = Depends(get_db)):
    return transactions.get_all_transactions(db)

@app.get("/summary")
def get_summary(budget: float, db: Session = Depends(get_db)):
    return transactions.get_summary(db, budget)

@app.get("/categories")
def get_categories():
    return transactions.get_categories()
