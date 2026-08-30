from rich.table import Table

class ProcessTable:
    def __init__(self, processes, os_type):
        self.processes = processes
        self.os_type = os_type

    def build(self):
        table = Table(title=f"Monitor Engine | OS: {self.os_type} | Active: {len(self.processes)}")
        
        table.add_column("PID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Process", style="white")
        table.add_column("CPU %", justify="right", style="green")
        table.add_column("Memory %", justify="right", style="yellow")

        for p in sorted(self.processes, key=lambda x: x.cpu_percent, reverse=True):
            cpu_style = "red" if p.cpu_percent > 50.0 else "green"
            mem_style = "red" if p.memory_percent > 50.0 else "yellow"
            
            table.add_row(
                str(p.pid),
                p.name[:25],
                f"[{cpu_style}]{p.cpu_percent:.1f}[/{cpu_style}]",
                f"[{mem_style}]{p.memory_percent:.1f}[/{mem_style}]"
            )

        return table