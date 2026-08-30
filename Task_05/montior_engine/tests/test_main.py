import unittest
from unittest.mock import patch, MagicMock
import main

class TestMain(unittest.TestCase):
    
    def test_get_collector_linux(self):
        collector = main.get_collector("Linux")
        self.assertIsInstance(collector, main.LinuxCollector)

    def test_get_collector_windows(self):
        collector = main.get_collector("Windows")
        self.assertIsInstance(collector, main.WindowsCollector)

    def test_get_collector_unsupported(self):
        collector = main.get_collector("macOS")
        self.assertIsNone(collector)

    @patch('main.detect_os', return_value='Windows')
    @patch('main.Display')
    @patch('main.Monitor')
    @patch('time.sleep')
    def test_main_run(self, mock_sleep, mock_monitor, mock_display, mock_detect_os):
        mock_display_inst = MagicMock()
        mock_display.return_value = mock_display_inst
        
        main.main()
        
        mock_monitor.assert_called_once()
        mock_display.assert_called_once()
        mock_display_inst.start.assert_called_once()

if __name__ == '__main__':
    unittest.main()
