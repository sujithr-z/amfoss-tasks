import unittest
from unittest.mock import patch, MagicMock
from guardian.collectors.windows import WindowsCollector

class TestWindowsCollector(unittest.TestCase):
    
    @patch('subprocess.run')
    def test_get_processes_success(self, mock_run):
        mock_output = "1234,python,52428800,1.25\n5678,explorer,104857600,0.5"
        mock_run.return_value = MagicMock(stdout=mock_output, stderr="")
        
        collector = WindowsCollector()
        procs = collector.get_processes()
        
        self.assertEqual(len(procs), 2)
        
        p1 = next(p for p in procs if p.pid == 1234)
        self.assertEqual(p1.name, "python")
        self.assertEqual(p1.memory_bytes, 52428800)
        self.assertEqual(p1.cpu_ticks, int(1.25 * 10000000))
        
        p2 = next(p for p in procs if p.pid == 5678)
        self.assertEqual(p2.name, "explorer")
        self.assertEqual(p2.memory_bytes, 104857600)
        self.assertEqual(p2.cpu_ticks, int(0.5 * 10000000))

    @patch('subprocess.run')
    def test_get_processes_empty(self, mock_run):
        mock_run.return_value = MagicMock(stdout="", stderr="")
        
        collector = WindowsCollector()
        procs = collector.get_processes()
        
        self.assertEqual(len(procs), 0)

    @patch('subprocess.run')
    def test_get_processes_invalid_line(self, mock_run):
        mock_output = "invalid_line\n123,test,1024,0.1"
        mock_run.return_value = MagicMock(stdout=mock_output, stderr="")
        
        collector = WindowsCollector()
        procs = collector.get_processes()
        
        self.assertEqual(len(procs), 1)
        p = procs[0]
        self.assertEqual(p.pid, 123)
        self.assertEqual(p.name, "test")

if __name__ == '__main__':
    unittest.main()