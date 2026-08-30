# Pirate King's Scheduler 🏴‍☠️

A modular CPU Scheduling Simulator written in Go supporting multiple scheduling algorithms, Gantt chart visualization, and turnaround / waiting time metrics calculation.

## Architecture

```
pirate-kings-scheduler/
│
├── main.go               # CLI entrypoint and orchestrator
├── go.mod                # Go module definition
├── README.md             # Project documentation
│
├── models/
│   └── process.go        # Process struct definition
│
├── scheduler/
│   ├── fcfs.go           # First-Come-First-Serve (FCFS) algorithm & interfaces
│   ├── sjf.go            # Shortest Job First (SJF Non-Preemptive) algorithm
│   └── round_robin.go    # Round Robin (RR Preemptive) algorithm
│
├── simulation/
│   ├── simulator.go      # Simulation runner and pipeline
│   └── gantt.go          # ASCII Gantt chart visualizer
│
├── metrics/
│   └── metrics.go        # Average Waiting Time & Turnaround Time metrics
│
└── input/
    └── parser.go         # Terminal input parser and validators
```

## Features

- **FCFS (First-Come-First-Serve)**: Non-preemptive scheduling in order of arrival.
- **SJF (Shortest Job First)**: Non-preemptive scheduling prioritizing shortest burst time among arrived processes.
- **Round Robin (RR)**: Preemptive scheduling with a customizable time quantum.
- **ASCII Gantt Chart**: Visual execution timeline with start and completion timestamps.
- **Detailed Process Table & Metrics**: Arrival Time (AT), Burst Time (BT), Completion Time (CT), Waiting Time (WT), and Turnaround Time (TAT) alongside averages.

## Getting Started

### Prerequisites
- [Go 1.22+](https://golang.org/dl/)

### Running the Simulator
```bash
go run .
```

### Building the Binary
```bash
go build -o pirate-kings-scheduler.exe .
```
