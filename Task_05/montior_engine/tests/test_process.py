import unittest
from guardian.core.process import Process

class TestProcess(unittest.TestCase):
    
    def test_init_defaults(self):
        p = Process(1, "test")
        self.assertEqual(p.pid, 1)
        self.assertEqual(p.name, "test")
        self.assertEqual(p.cpu_ticks, 0)
        self.assertEqual(p.memory_bytes, 0)
        self.assertEqual(p.cpu_percent, 0.0)
        self.assertEqual(p.memory_percent, 0.0)

    def test_init_custom(self):
        p = Process(42, "python", 1500, 2048000)
        self.assertEqual(p.pid, 42)
        self.assertEqual(p.name, "python")
        self.assertEqual(p.cpu_ticks, 1500)
        self.assertEqual(p.memory_bytes, 2048000)

    def test_repr(self):
        p = Process(99, "chrome")
        self.assertEqual(repr(p), "Process(pid=99, name=chrome)")

    def test_attribute_modification(self):
        p = Process(1, "sys")
        p.cpu_percent = 12.5
        p.memory_percent = 3.4
        self.assertEqual(p.cpu_percent, 12.5)
        self.assertEqual(p.memory_percent, 3.4)

if __name__ == '__main__':
    unittest.main()