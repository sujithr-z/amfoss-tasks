import unittest
from unittest.mock import MagicMock, patch
from guardian.core.process import Process
from guardian.ui.table import ProcessTable
from guardian.ui.display import Display

class TestUI(unittest.TestCase):
    
    def test_process_table_build(self):
        p1 = Process(pid=100, name="proc1", cpu_ticks=10, memory_bytes=1000)
        p1.cpu_percent = 75.5
        p1.memory_percent = 10.2
        
        p2 = Process(pid=200, name="proc2", cpu_ticks=5, memory_bytes=5000)
        p2.cpu_percent = 12.0
        p2.memory_percent = 60.0
        
        table_gen = ProcessTable([p1, p2], os_type="Windows")
        table = table_gen.build()
        
        self.assertIsNotNone(table)
        self.assertEqual(len(table.rows), 2)

    def test_display_calc_mem_percent(self):
        mock_monitor = MagicMock()
        display = Display(monitor=mock_monitor, os_type="TestOS")
        display.total_mem = 1000000
        
        p = Process(pid=1, name="test", cpu_ticks=0, memory_bytes=500000)
        res = display.calc_mem_percent([p])
        
        self.assertAlmostEqual(res[0].memory_percent, 50.0)

    @patch('builtins.open', unittest.mock.mock_open(read_data="MemTotal:        16384 kB\n"))
    def test_display_get_total_memory_linux(self):
        mock_monitor = MagicMock()
        display = Display(monitor=mock_monitor, os_type="Linux")
        self.assertEqual(display.total_mem, 16384 * 1024)

if __name__ == '__main__':
    unittest.main()
