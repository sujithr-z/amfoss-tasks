import subprocess
from guardian.core.process import Process

class WindowsCollector:
    def __init__(self):
        self.clock_ticks = 10000000
        self.cmd = [
            "powershell", "-Command",
            "Get-Process | ForEach-Object { \"$($_.Id),$($_.ProcessName),$($_.WorkingSet64),$($_.CPU)\" }"
        ]

    def get_processes(self):
        procs = []
        try:
            res = subprocess.run(self.cmd, capture_output=True, text=True, timeout=5)
            for line in res.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                parts = line.split(',', 3)
                if len(parts) >= 4:
                    pid = int(parts[0])
                    name = parts[1]
                    mem = int(parts[2])
                    cpu = float(parts[3]) if parts[3] else 0.0
                    ticks = int(cpu * 10000000)
                    procs.append(Process(pid, name, ticks, mem))
        except Exception:
            pass
        return procs