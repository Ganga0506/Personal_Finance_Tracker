from fastapi.testclient import TestClient
from app.main import app
import unittest

client = TestClient(app)

class TestAPI(unittest.TestCase):
    """
    Unit tests for FastAPI endpoints using TestClient.
    """
    def test_get_categories(self):
        """
        Test that the /categories endpoint returns 200 and includes 'FOOD' in the response.
        """
        response = client.get("/categories")
        self.assertEqual(response.status_code, 200)
        self.assertIn("FOOD", response.json())

    def test_create_transaction(self):
        """
        Test that a transaction can be submitted via the /add form (POST) without errors.
        """
        data = {
            "name": "Test Transaction",
            "amount": 10.0,
            "category": "Misc",
            "date": "2025-07-09"
        }
        response = client.post("/add", data=data, allow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
