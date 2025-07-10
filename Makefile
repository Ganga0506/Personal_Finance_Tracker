test:
	PYTHONPATH=. python3 tests/test_transactions.py

run-transactions:
	PYTHONPATH=. python3 app/transactions.py

run:
	PYTHONPATH=. uvicorn app.main:app --reload