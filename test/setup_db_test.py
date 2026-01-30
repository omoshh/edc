import unittest
from unittest.mock import patch, MagicMock
import psycopg
from backend.db.setup_db import init_db

class TestSetupDB(unittest.TestCase):

    @patch("backend.db.setup_db.get_conn")
    @patch("backend.db.setup_db.get_name")
    def test_init_db_success_first_try(self, mock_get_name, mock_get_conn):
        """Teset succesful connection from first attempt"""
        mock_get_name.return_value = "metrics_table"
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        init_db()

        args, _ = mock_cursor.execute.call_args
        self.assertIn("CREATE TABLE IF NOT EXISTS metrics_table", args[0])
        self.assertEqual(mock_get_conn.call_count, 1)

    @patch("backend.db.setup_db.time.sleep") # Мокаем sleep, чтобы тест не шел 20 секунд!
    @patch("backend.db.setup_db.get_conn")
    @patch("backend.db.setup_db.get_name")
    def test_init_db_retry_logic(self, mock_get_name, mock_get_conn, mock_sleep):
        """Check that function retries after unsuccesful connections"""
        mock_get_name.return_value = "metrics_table"
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.side_effect = [
            psycopg.OperationalError("DB not ready"),
            psycopg.OperationalError("DB not ready"),
            mock_conn
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        init_db()
        self.assertEqual(mock_get_conn.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        self.assertTrue(mock_cursor.execute.called)

    @patch("backend.db.setup_db.time.sleep")
    @patch("backend.db.setup_db.get_conn")
    @patch("backend.db.setup_db.get_name")
    def test_init_db_fails_after_10_attempts(self, mock_get_name, mock_get_conn, mock_sleep):
        """Check behavior after 10 unsuccesful attemps"""
        mock_get_name.return_value = "metrics_table"
        mock_get_conn.return_value.__enter__.side_effect = psycopg.OperationalError("Dead")

        init_db()
        self.assertEqual(mock_get_conn.call_count, 10)
        self.assertEqual(mock_sleep.call_count, 10)

if __name__ == "__main__":
    unittest.main()