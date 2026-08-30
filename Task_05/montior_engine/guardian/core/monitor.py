import time

class Monitor:
    def __init__(self, collector, rate=0.5):
        self.collector = collector
        self.rate = rate
        self.processes = []
        self.prev_ticks = {}
        self.prev_time = time.time()
        self.running = False

    def calc_cpu(self, procs):
        curr_time = time.time()
        dt = curr_time - self.prev_time
        clock_ticks = getattr(self.collector, 'clock_ticks', 100)
        
        for p in procs:
            if p.pid in self.prev_ticks:
                delta = p.cpu_ticks - self.prev_ticks[p.pid]
                if dt > 0 and clock_ticks > 0:
                    p.cpu_percent = (delta / clock_ticks / dt) * 100.0
                else:
                    p.cpu_percent = 0.0
            else:
                p.cpu_percent = 0.0
            self.prev_ticks[p.pid] = p.cpu_ticks
            
        self.prev_time = curr_time
        return procs

    def update(self):
        raw = self.collector.get_processes()
        self.processes = self.calc_cpu(raw)

    def start(self):
        self.running = True
        self.update()
        time.sleep(self.rate)
        while self.running:
            self.update()
            time.sleep(self.rate)

    def stop(self):
        self.running = False