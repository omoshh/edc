import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
import os

# 1. Set the env variable BEFORE the import to ensure lifespan logic sees it
os.environ["TESTING"] = "1"

import backend.api as api_module 

class TestMetricsAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(api_module.app)
        self.mock_row = {
            "timestamp": datetime(2024, 1, 1, 12, 0, 0),
            "cpu_usage": 25.5,
            "ram_usage": 60.2,
            "load_average": 1.5,
            "network_bandwidth": 100.0
        }

    @patch("backend.api.get_conn")
    @patch("backend.api.get_name")
    def test_get_metrics_success(self, mock_get_name, mock_get_conn):
        mock_get_name.return_value = "metrics_table"
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        mock_cursor.fetchone.return_value = self.mock_row

        response = self.client.get("/metrics")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["cpu_usage"], 25.5)

    @patch("backend.api.get_conn")
    def test_get_metrics_not_found(self, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        response = self.client.get("/metrics")
        # Matches your current try/except block behavior (500)
        self.assertEqual(response.status_code, 500)

    @patch("backend.api.get_conn")
    @patch("backend.api.get_name")
    def test_get_metrics_range_success(self, mock_get_name, mock_get_conn):
        mock_get_name.return_value = "metrics_table"
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [self.mock_row]

        params = {"start": "2024-01-01", "end": "2024-01-02"}
        response = self.client.get("/metrics/range", params=params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)

    @patch("backend.api.get_conn")
    def test_get_metrics_range_db_error(self, mock_get_conn):
        mock_get_conn.side_effect = Exception("DB Fail")

        params = {"start": "2024-01-01", "end": "2024-01-02"}
        response = self.client.get("/metrics/range", params=params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

if __name__ == "__main__":
    unittest.main()