import unittest
import time
from unittest.mock import MagicMock
from guardian.core.monitor import Monitor
from guardian.core.process import Process

class TestMonitor(unittest.TestCase):
    
    def test_monitor_init(self):
        mock_collector = MagicMock()
        monitor = Monitor(collector=mock_collector, rate=0.5)
        self.assertEqual(monitor.collector, mock_collector)
        self.assertEqual(monitor.rate, 0.5)
        self.assertEqual(monitor.processes, [])
        self.assertFalse(monitor.running)

    def test_calc_cpu_scaling(self):
        mock_collector = MagicMock()
        mock_collector.clock_ticks = 100
        monitor = Monitor(collector=mock_collector)
        
        # Initial state
        monitor.prev_time = time.time() - 1.0  # 1 second ago
        monitor.prev_ticks = {1: 100}
        
        # Process used 50 ticks over 1.0 second (50 / 100 / 1.0 * 100 = 50%)
        p = Process(pid=1, name="test_proc", cpu_ticks=150, memory_bytes=1024)
        updated = monitor.calc_cpu([p])
        
        self.assertAlmostEqual(updated[0].cpu_percent, 50.0, places=1)
        self.assertEqual(monitor.prev_ticks[1], 150)

    def test_calc_cpu_new_process(self):
        mock_collector = MagicMock()
        mock_collector.clock_ticks = 100
        monitor = Monitor(collector=mock_collector)
        
        p = Process(pid=99, name="new_proc", cpu_ticks=300)
        updated = monitor.calc_cpu([p])
        
        # First sample has 0.0% CPU because no previous ticks
        self.assertEqual(updated[0].cpu_percent, 0.0)
        self.assertEqual(monitor.prev_ticks[99], 300)

    def test_update(self):
        mock_collector = MagicMock()
        mock_collector.clock_ticks = 100
        p = Process(pid=1, name="test", cpu_ticks=10)
        mock_collector.get_processes.return_value = [p]
        
        monitor = Monitor(collector=mock_collector)
        monitor.update()
        
        self.assertEqual(len(monitor.processes), 1)
        self.assertEqual(monitor.processes[0].name, "test")

if __name__ == '__main__':
    unittest.main()
