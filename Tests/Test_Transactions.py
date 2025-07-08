"""
Unit tests for the Transactions module using an in-memory SQLite database.
"""

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
        Base.metadata.create_all(blind=cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Runs before each test method.
        - Starts a new database session.
        """

        self.db = self.Session()
    
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

        transactions = transactions.get_all_transactions(db=self.db)
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].name, "Starbucks")
        self.assertEqual(transactions[1].name, "Netflix")


if __name__ == '__main__':
    unittest.main()