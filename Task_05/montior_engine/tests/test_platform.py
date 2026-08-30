import unittest
from unittest.mock import patch
from guardian.system.platform import detect_os

class TestPlatform(unittest.TestCase):
    
    @patch('platform.system', return_value='Linux')
    def test_detect_linux(self, mock_system):
        self.assertEqual(detect_os(), 'Linux')

    @patch('platform.system', return_value='Windows')
    def test_detect_windows(self, mock_system):
        self.assertEqual(detect_os(), 'Windows')

    @patch('platform.system', return_value='Darwin')
    def test_detect_macos(self, mock_system):
        self.assertEqual(detect_os(), 'macOS')

    @patch('platform.system', return_value='FreeBSD')
    def test_detect_unknown(self, mock_system):
        self.assertEqual(detect_os(), 'Unknown')

if __name__ == '__main__':
    unittest.main()
