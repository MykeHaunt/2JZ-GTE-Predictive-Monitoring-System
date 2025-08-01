import unittest
from app import app

class PredictTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_prediction_valid_input(self):
        response = self.client.post("/api/predict", json={
            "rpm": 3200,
            "boost": 12,
            "afr": 14.7,
            "oil_temp": 90,
            "coolant_temp": 85,
            "knock": 0.02
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("prediction", response.get_json())

if __name__ == "__main__":
    unittest.main()