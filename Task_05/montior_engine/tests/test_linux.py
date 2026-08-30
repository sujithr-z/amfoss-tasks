import unittest
from unittest.mock import patch, mock_open
from guardian.collectors.linux import LinuxCollector

class TestLinuxCollector(unittest.TestCase):
    
    @patch('os.sysconf', create=True)
    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_processes(self, mock_file, mock_listdir, mock_sysconf):
        mock_sysconf.return_value = 4096
        mock_listdir.return_value = ['1', 'meminfo', '2']
        
        stat_data_1 = "1 (systemd) S 0 1 1 0 -1 4194560 123 456 0 0 100 50 0 0 20 0 1 0 10 12345678 1000"
        status_data_1 = "Name:\tsystemd\nVmRSS:\t1000 kB\n"
        
        stat_data_2 = "2 (kthreadd) S 0 0 0 0 -1 2129984 0 0 0 0 0 0 0 0 20 0 1 0 10 0 0 0"
        status_data_2 = "Name:\tkthreadd\nVmRSS:\t0 kB\n"
        
        def open_side_effect(file_path, *args, **kwargs):
            if file_path == '/proc/1/stat':
                return mock_open(read_data=stat_data_1).return_value
            elif file_path == '/proc/1/status':
                return mock_open(read_data=status_data_1).return_value
            elif file_path == '/proc/2/stat':
                return mock_open(read_data=stat_data_2).return_value
            elif file_path == '/proc/2/status':
                return mock_open(read_data=status_data_2).return_value
            raise FileNotFoundError

        mock_file.side_effect = open_side_effect
        
        collector = LinuxCollector()
        procs = collector.get_processes()
        
        self.assertEqual(len(procs), 2)
        
        p1 = next(p for p in procs if p.pid == 1)
        self.assertEqual(p1.name, "systemd")
        self.assertEqual(p1.cpu_ticks, 150)
        self.assertEqual(p1.memory_bytes, 1000 * 1024)
        
        p2 = next(p for p in procs if p.pid == 2)
        self.assertEqual(p2.name, "kthreadd")
        self.assertEqual(p2.cpu_ticks, 0)
        self.assertEqual(p2.memory_bytes, 0)

if __name__ == '__main__':
    unittest.main()