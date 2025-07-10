from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from app import transactions 
from app.database import SessionLocal
from app.models import CategoryEnum, Income
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
    all_income = db.query(Income).order_by(Income.date.desc()).all()
    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "transactions": all_txns,
        "incomes": all_income
    })

# 4. POST transaction (API, not form)
@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    txn = transactions.add_transaction(db, **transaction.dict())
    return txn

# 5. Get summary 
@app.get("/summary", response_class=HTMLResponse)
def get_summary(request: Request, db: Session = Depends(get_db)):
    data = transactions.get_summary(db)
    summary_data = transactions.get_summary(db)
    pie_img = transactions.get_spending_pie_chart(db)
    line_img = transactions.get_daily_spending_chart(db)

    return templates.TemplateResponse("summary.html", {
        "request": request,
        "summary": data,
        "pie_chart": pie_img,
        "line_chart": line_img,
    })

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

# 9. Budget Summary 
@app.api_route("/budget_summary", methods=["GET", "POST"])
def budget_summary(
    request: Request,
    db: Session = Depends(get_db),
    total_budget: float = Form(None),
    end_date: date = Form(None)
):
    daily = None
    remaining = None
    if total_budget is not None and total_budget < 0:
        raise HTTPException(status_code=400, detail="Total budget cannot be negative")
    
    if request.method == "POST" and total_budget and end_date:
        daily = transactions.get_daily_budget(db, total_budget, date.today(), end_date)
        remaining = transactions.get_remaining_budget(db, total_budget)

    return templates.TemplateResponse("budget_summary.html", {
        "request": request,
        "daily_budget": daily,
        "remaining_budget": remaining,
        "total_budget": total_budget,
        "end_date": end_date
    })

#10. Add Income
@app.api_route("/add_income", methods=["GET", "POST"])
def add_income(
    request: Request,
    db: Session = Depends(get_db),
    amount: float = Form(None),
    date_: date = Form(None)
):
    if request.method == "GET":
        return templates.TemplateResponse("add_income.html", {"request": request})

    if amount is not None and amount < 0:
        return templates.TemplateResponse("add_income.html", {
            "request": request,
            "error": "Please enter a valid positive amount."
        })
    
    income_record = Income(amount=amount, date=date_)
    db.add(income_record)
    db.commit()
    db.refresh(income_record)

    return RedirectResponse(url="/", status_code=303)
    