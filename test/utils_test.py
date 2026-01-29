import unittest
from unittest.mock import patch, MagicMock
from backend.utils import get_average, get_bandwidth

class TestUtils(unittest.TestCase):

    @patch("os.cpu_count")
    @patch("psutil.getloadavg")
    def test_get_average_calculation(self, mock_load, mock_cpu):
        """Test expected behavior from get_average load calculation"""
        # Setup: Load is 2.0 on a 4-core machine
        mock_load.return_value = (2.0, 1.5, 1.0)
        mock_cpu.return_value = 4
        
        # Expected: (2.0 / 4) * 100 = 50.0
        result = get_average()
        self.assertEqual(result, 50.0)

    @patch("time.sleep")
    @patch("psutil.net_io_counters")
    def test_get_bandwidth_math(self, mock_net, mock_sleep):
        """Test expected behavior from network bandwidth calculation"""
        val_old = MagicMock(bytes_sent=0, bytes_recv=0)
        val_new = MagicMock(bytes_sent=500000, bytes_recv=500000)
        
        mock_net.side_effect = [val_old, val_old, val_new, val_new]
        
        # Expected: (1,000,000 bytes * 8 bits) / 10^6 = 8.0 Mbps
        result = get_bandwidth()
        self.assertEqual(result, 8.0)

    @patch("os.cpu_count")
    @patch("psutil.getloadavg")
    def test_get_average_handles_none(self, mock_load, mock_cpu):
        """Test behavior if cpu_count or getloadavg are None"""
        # Test the fallback logic
        mock_load.return_value = (None, None, None)
        mock_cpu.return_value = None
        self.assertEqual(get_average(), 0)

if __name__ == "__main__":
    unittest.main()