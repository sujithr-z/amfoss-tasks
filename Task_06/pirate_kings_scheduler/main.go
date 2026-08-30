package main

import (
	"fmt"
	"pirate-kings-scheduler/input"
	"pirate-kings-scheduler/metrics"
	"pirate-kings-scheduler/models"
	"pirate-kings-scheduler/scheduler"
	"pirate-kings-scheduler/simulation"
	"strings"
)

func main() {
	fmt.Println("=====================================")
	fmt.Println("      PIRATE KING'S SCHEDULER")
	fmt.Println("=====================================")
	fmt.Println()

	// 1. Get number of processes
	numProcs := input.ReadPositiveInt("Enter number of processes: ")
	processes := make([]models.Process, numProcs)

	// 2. Read process details
	for i := 0; i < numProcs; i++ {
		fmt.Printf("\n--- Process %d ---\n", i+1)
		pid := fmt.Sprintf("P%d", i+1)
		at := input.ReadInt("Arrival Time: ")
		bt := input.ReadPositiveInt("Burst Time: ")

		processes[i] = models.Process{
			ID:          pid,
			ArrivalTime: at,
			BurstTime:   bt,
		}
	}

	// 3. Choose algorithm
	fmt.Println("\nSelect Algorithm:")
	fmt.Println("1. FCFS (First Come First Serve)")
	fmt.Println("2. SJF (Shortest Job First - Non-Preemptive)")
	fmt.Println("3. RR (Round Robin)")

	choice := input.ReadPositiveInt("\nChoice (1-3): ")

	var sched scheduler.Scheduler

	switch choice {
	case 1:
		sched = scheduler.NewFCFS()
	case 2:
		sched = scheduler.NewSJF()
	case 3:
		quantum := input.ReadPositiveInt("Enter Time Quantum: ")
		sched = scheduler.NewRoundRobin(quantum)
	default:
		fmt.Println("Invalid choice. Defaulting to FCFS.")
		sched = scheduler.NewFCFS()
	}

	// 4. Run Simulation
	sim := simulation.New(sched)
	result := sim.Run(processes)

	// 5. Print Gantt Chart
	fmt.Println("\n=====================================")
	fmt.Println("           GANTT CHART")
	fmt.Println("=====================================")
	simulation.PrintGanttChart(result.Timeline)

	// 6. Print Process Table
	fmt.Println("\n=====================================")
	fmt.Println("        PROCESS RESULTS")
	fmt.Println("=====================================")
	printProcessTable(result.Processes)

	// 7. Print Metrics
	fmt.Println("\n=====================================")
	fmt.Println("           METRICS")
	fmt.Println("=====================================")
	metrics.Print(result.Processes)
}

func printProcessTable(processes []models.Process) {
	fmt.Printf("%-5s | %-5s | %-5s | %-5s | %-5s | %-5s\n", "PID", "AT", "BT", "CT", "WT", "TAT")
	fmt.Println(strings.Repeat("-", 42))
	for _, p := range processes {
		fmt.Printf("%-5s | %-5d | %-5d | %-5d | %-5d | %-5d\n",
			p.ID, p.ArrivalTime, p.BurstTime, p.CompletionTime, p.WaitingTime, p.TurnaroundTime)
	}
}