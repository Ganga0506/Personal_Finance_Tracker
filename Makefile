test-transactions:
	PYTHONPATH=. python3 tests/test_transactions.py

test-api:
	PYTHONPATH=. python3 tests/test_api.py
	
run-transactions:
	PYTHONPATH=. python3 app/transactions.py

run:
	PYTHONPATH=. uvicorn app.main:app --reload

create-db:
	PYTHONPATH=. python3 app/database.py