import os
from guardian.core.process import Process

class LinuxCollector:
    def __init__(self):
        try:
            self.page_size = os.sysconf('SC_PAGE_SIZE')
        except (AttributeError, ValueError, OSError):
            self.page_size = 4096
        try:
            self.clock_ticks = os.sysconf('SC_CLK_TCK')
        except (AttributeError, ValueError, OSError):
            self.clock_ticks = 100

    def get_processes(self):
        procs = []
        try:
            pids = [int(p) for p in os.listdir('/proc') if p.isdigit()]
        except OSError:
            return procs

        for pid in pids:
            try:
                stat_path = f'/proc/{pid}/stat'
                status_path = f'/proc/{pid}/status'

                with open(stat_path, 'r') as f:
                    stat_data = f.read()

                start = stat_data.find('(') + 1
                end = stat_data.rfind(')')
                name = stat_data[start:end]
                
                fields = stat_data[end+2:].split()
                utime = int(fields[11])
                stime = int(fields[12])
                cpu_ticks = utime + stime

                mem_bytes = 0
                with open(status_path, 'r') as f:
                    for line in f:
                        if line.startswith('VmRSS:'):
                            mem_kb = int(line.split()[1])
                            mem_bytes = mem_kb * 1024
                            break

                procs.append(Process(pid, name, cpu_ticks, mem_bytes))

            except (OSError, IOError, ValueError, IndexError):
                continue




