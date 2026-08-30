import os
import sys
import time
from rich.live import Live
from rich.console import Console
from guardian.ui.table import ProcessTable

class Display:
    def __init__(self, monitor, os_type, rate=0.5):
        self.monitor = monitor
        self.os_type = os_type
        self.rate = rate
        self.console = Console()
        self.total_mem = self.get_total_memory()

    def get_total_memory(self):
        if self.os_type == "Linux":
            try:
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if line.startswith('MemTotal:'):
                            return int(line.split()[1]) * 1024
            except Exception:
                pass
        return 1

    def calc_mem_percent(self, processes):
        for p in processes:
            p.memory_percent = (p.memory_bytes / self.total_mem) * 100.0 if self.total_mem > 0 else 0.0
        return processes

    def start(self):
        self.monitor.update()
        time.sleep(self.rate)
        
        try:
            with Live(console=self.console, refresh_per_second=2, screen=True) as live:
                while True:
                    self.monitor.update()
                    procs = self.calc_mem_percent(self.monitor.processes)
                    table = ProcessTable(procs, self.os_type).build()
                    live.update(table)
                    time.sleep(self.rate)
        except KeyboardInterrupt:
            self.monitor.stop()
            self.console.print("\n[yellow]Monitor Engine shutting down...[/yellow]")
            sys.exit(0)