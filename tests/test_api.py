from fastapi.testclient import TestClient
from app.main import app
import unittest

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_get_categories(self):
        response = client.get("/categories")
        self.assertEqual(response.status_code, 200)
        self.assertIn("FOOD", response.json())

    def test_create_transaction(self):
        data = {
            "name": "Test Transaction",
            "amount": 10.0,
            "category": "MISC",
            "date": "2025-07-09"
        }
        response = client.post("/transactions", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Transaction")

if __name__ == "__main__":
    unittest.main()
