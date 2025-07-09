import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Transaction, CategoryEnum
from datetime import date
from app import transactions

class TestTransactions(unittest.TestCase):
    """
    Test case for transaction-related operations in the Transactions module.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment once for all tests.
        - Creates an in-memory SQLite database.
        - Binds a sessionmaker to it.
        """
        
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Runs before each test method.
        - Starts a new database session.
        """
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = self.__class__.Session()
    
    def tearDown(self): 
        """
        Runs after each test method.
        - Closes the database session.
        """

        self.db.close()

    def test_add_transaction(self):
        """
        Tests if a transaction can be successfully added to the database.

        Calls:
            Transactions.add_transaction(db, name, amount, category, date_)

        Asserts:
            - The returned transaction has a valid ID.
            - Name, amount, and category match expected values.
        """

        txn = transactions.add_transaction(
            db=self.db,
            name="Amazon",
            amount=50.00,
            category=CategoryEnum.FUN,
            date_=date(2025, 7, 8)          
        )
        self.assertIsNotNone(txn.id)
        self.assertEqual(txn.name, "Amazon")
        self.assertEqual(txn.amount, 50.00)
        self.assertEqual(txn.category, CategoryEnum.FUN)

    def test_get_all_transactions(self):
        """
        Tests whether all transactions are correctly retrieved from the database.

        Steps:
            - Adds two transactions to the test database.
            - Calls get_all_transactions(db) to get all entries.
    
        Asserts:
            - The total number of transactions returned is 2.
            - The names of the transactions match the ones added ("Starbucks" and "Netflix").
        """
        
        transactions.add_transaction(
            db=self.db,
            name="Starbucks",
            amount=5.75,
            category=CategoryEnum.FOOD,
            date_=date(2025, 7, 8)
        )
        
        transactions.add_transaction(
            db=self.db,
            name="Netflix",
            amount=15.99,
            category=CategoryEnum.FUN,
            date_=date(2025, 7, 8)
        )

        all_txns = transactions.get_all_transactions(db=self.db)
        self.assertEqual(len(all_txns), 2)
        self.assertEqual(all_txns[0].name, "Starbucks")
        self.assertEqual(all_txns[1].name, "Netflix")

    
    def test_get_summary(self):
        """
        Tests summary logic:
        - Total spent
        - Remaining budget

        - Adds two transactions (15 + 12).
        - Checks if summary["total_spent"] = 27.00.
        - Checks if summary["remaining"] = 73.00 (budget was 100.00).
        """
       
        budget = 100.00

        transactions.add_transaction(self.db, "Lunch", 15.00, CategoryEnum.FOOD, date(2025, 7, 8))
        transactions.add_transaction(self.db, "Movie", 12.00, CategoryEnum.FUN, date(2025, 7, 8))

        summary = transactions.get_summary(self.db, budget)

        self.assertEqual(summary["total_spent"], 27.00)
        self.assertEqual(summary["remaining"], 73.00)
    
    def test_get_by_category(self):
        """
        Tests filtering transactions by category.

        - Adds 3 transactions (2 FOOD, 1 TRANSPORT).
        - Checks if only FOOD transactions are returned.
        - Verifies names and count of returned items.
        """

        transactions.add_transaction(self.db, "Dinner", 20.00, CategoryEnum.FOOD, date(2025, 7, 8))
        transactions.add_transaction(self.db, "Subway", 2.75, CategoryEnum.TRANSPORT, date(2025, 7, 8))
        transactions.add_transaction(self.db, "Snacks", 5.00, CategoryEnum.FOOD, date(2025, 7, 8))

        food_txns = transactions.get_by_category(self.db, CategoryEnum.FOOD)

        self.assertEqual(len(food_txns), 2)
        self.assertEqual(food_txns[0].name, "Dinner")
        self.assertEqual(food_txns[1].name, "Snacks")

    def test_daily_budget(self):
        """
        Tests daily budget calculation based on remaining budget and days left.

        - Budget = 90.00; spent 30.00.
        - Days left = 3 (including today).
        - Remaining = 60.00 → daily = 20.00.
        """

        budget = 90.00
        today = date(2025, 7, 8)
        end_date = date(2025, 7, 10)  # 3 days including today

        transactions.add_transaction(self.db, "Gym", 30.00, CategoryEnum.HEALTH, today)
        daily = transactions.get_daily_budget(self.db, budget, today, end_date)
        self.assertAlmostEqual(daily, 20.00, places=2)

    def test_get_categories(self):
        """
        Tests get_categories() returns all category names as strings.
        Asserts that "FOOD" and "INCOME" are in the returned list.
        """

        cats = transactions.get_categories()
        self.assertIn("FOOD", cats)
        self.assertIn("INCOME", cats)

    def test_get_remaining_budget(self):
        """
        Tests get_remaining_budget() returns correct remaining budget.
        Adds a $5 FOOD transaction to a $100 budget and checks if remaining is $95.
        """

        budget = 100
        transactions.add_transaction(self.db, "Coffee", 5, CategoryEnum.FOOD, date(2025,7,8))
        remaining = transactions.get_remaining_budget(self.db, budget)
        self.assertEqual(remaining, 95)

    def test_delete_transaction(self):
        """
        Tests delete_transaction() removes a transaction by ID.
        Adds a transaction, deletes it, and verifies it no longer exists.
        """
        
        txn = transactions.add_transaction(self.db, "Snack", 3, CategoryEnum.FOOD, date(2025,7,8))
        result = transactions.delete_transaction(self.db, txn.id)
        self.assertTrue(result)
        self.assertIsNone(self.db.query(Transaction).filter(Transaction.id==txn.id).first())

    def test_add_income(self):
        """
        Tests add_income() correctly adds an income transaction with category INCOME.
        Verifies the returned transaction's category is INCOME.
        """

        income = transactions.add_income(self.db, "Salary", 1000, date(2025,7,8))
        self.assertEqual(income.category, CategoryEnum.INCOME)

if __name__ == '__main__':
    unittest.main()