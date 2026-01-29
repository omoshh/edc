import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.db.logger import job

class TestLogger(unittest.TestCase):

    @patch("backend.db.logger.get_name")
    @patch("backend.db.logger.get_conn")
    @patch("backend.db.logger.utils")
    @patch("backend.db.logger.datetime")
    def test_job_success(self, mock_datetime, mock_utils, mock_get_conn, mock_get_name):
        """Testing correct job() function behavior"""
        # fake system metrics and time
        mock_utils.get_cpu.return_value = 10.0
        mock_utils.get_mem.return_value = 20.0
        mock_utils.get_average.return_value = 0.5
        mock_utils.get_bandwidth.return_value = 1.2
        fixed_now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        
        # mock db setup
        mock_get_name.return_value = "test_table"
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        job()

        # Assertions
        # Checking if SQL query contains correct table name
        execute_args = mock_cursor.execute.call_args[0]
        query = execute_args[0]
        params = execute_args[1]

        self.assertIn("INSERT INTO test_table", query)
        
        # Check if params are given in correct oreder
        expected_params = (10.0, 20.0, 0.5, 1.2, fixed_now)
        self.assertEqual(params, expected_params)

        # Check if data is in db
        mock_conn.commit.assert_called_once()

    @patch("backend.db.logger.get_conn")
    @patch("backend.db.logger.utils")
    def test_job_database_error(self, mock_utils, mock_get_conn):
        """Testing if logger crashes on exeptions"""
        # mock failed db connection
        mock_get_conn.side_effect = Exception("Connection Lost")
        try:
            job()
        except Exception as e:
            self.fail(f"job() raised {type(e).__name__} instead of catching it!")

if __name__ == "__main__":
    unittest.main()