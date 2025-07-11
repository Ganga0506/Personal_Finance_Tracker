# Personal Finance Tracker

Hey! This is a simple Personal Finance Tracker web app built with FastAPI, SQLAlchemy, and SQLite. It helps you keep track of your expenses and incomes, view summaries, and get some basic budget insights.

---

## 🚀 Features

- ➕ Add new transactions (with categories like Food, Fun, etc.)
- 💰 Record your income
- 📄 View all past transactions and incomes
- 📂 Filter expenses by category
- 📊 Get summary stats (income, expenses, balance)
- 🥧 Pie chart for category-wise spending
- 📈 Line chart for daily spending
- 📋 Set a budget and get your daily limit + remaining budget
- 🗑️ Delete specific transactions

---

## 🛠 Tech Stack

- **FastAPI** – backend framework  
- **SQLAlchemy** – ORM for database interactions  
- **SQLite** – lightweight local database  
- **Jinja2** – for HTML templates  
- **Matplotlib** – for generating charts  
- **Uvicorn** – to run the app

---

## 🧰 Prerequisites

Before you run the app, make sure you have:

- Python 3.10+ installed  
- `pip` available 

---

## 📦 Setup Instructions

1. **Clone the repo:**

   ```bash
   git clone https://github.com/your-username/finance-tracker.git
   cd finance-tracker
   ```

2. **(Recommended) Set up a virtual environment:** 

     ```bash
     python3 -m venv venv
     source venv/bin/activate      # for macOS/Linux
     venv\Scripts\activate         # for Windows
     ```

3. **Install all dependencies:**

     ```bash
     pip install -r requirements.txt
     ```

4. **Create the database**

     ```bash
     make create-db
     ```

5. **Run the app**

     ```bash
     make run
     ```

---

## ⚠️ Note
`finance.db` is excluded from Git (via .gitignore) so your personal data stays private.

---
## 🧪 Running Tests

You can run the test files with:

```bash
make test-transactions
make test-api
```

## 🧼 Resetting the Database

If you want to clear all your data, just delete the `finance.db` file:

```bash
rm finance.db
```
 And then recreate it with: 
```bash
make create-db
```