class Process:
    def __init__(self, pid, name, cpu_ticks=0, memory_bytes=0):
        self.pid = pid
        self.name = name
        self.cpu_ticks = cpu_ticks
        self.memory_bytes = memory_bytes
        self.cpu_percent = 0.0
        self.memory_percent = 0.0

    def __repr__(self):
        return f"Process(pid={self.pid}, name={self.name})"