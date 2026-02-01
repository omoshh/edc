import unittest
from unittest.mock import patch
import os
from fastapi.testclient import TestClient

# env variable for testing
os.environ["TESTING"] = "1"

from backend.api import app


class TestAPIValidation(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_range_missing_parameters(self):
        """Test that missing query parameters return 422 Unprocessable Entity"""
        # Missing 'end' parameter
        response = self.client.get("/metrics/range?start=2024-01-01T00:00:00")
        self.assertEqual(response.status_code, 422)

        # Missing 'start' parameter
        response = self.client.get("/metrics/range?end=2024-01-01T00:00:00")
        self.assertEqual(response.status_code, 422)

    @patch("backend.api.get_conn")
    def test_range_invalid_date_format(self, mock_get_conn):
        """Test how the API handles non-date strings"""  # mock db
        params = {"start": "not-a-date", "end": "something-else"}
        response = self.client.get("/metrics/range", params=params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

    def test_metrics_post_not_allowed(self):
        """Test that sending a POST request to a GET endpoint returns 405 Method Not Allowed"""
        response = self.client.post("/metrics")
        self.assertEqual(response.status_code, 405)

    def test_cors_headers(self):
        """Test that CORS headers are present for frontend requests"""
        response = self.client.options(
            "/metrics",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("access-control-allow-origin"), "*")

    def test_not_found_route(self):
        """Test that accessing an undefined route returns a 404"""
        response = self.client.get("/this/route/does/not/exist")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Not Found")


if __name__ == "__main__":
    unittest.main()
