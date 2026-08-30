package metrics

import (
	"fmt"
	"pirate-kings-scheduler/models"
)

// Summary holds the calculated performance metrics.
type Summary struct {
	AvgWaitingTime    float64
	AvgTurnaroundTime float64
}

// Calculate computes average waiting time and turnaround time for a slice of completed processes.
func Calculate(processes []models.Process) Summary {
	if len(processes) == 0 {
		return Summary{}
	}

	totalWT := 0
	totalTAT := 0

	for _, p := range processes {
		totalWT += p.WaitingTime
		totalTAT += p.TurnaroundTime
	}

	n := float64(len(processes))
	return Summary{
		AvgWaitingTime:    float64(totalWT) / n,
		AvgTurnaroundTime: float64(totalTAT) / n,
	}
}

// Print displays the calculated metrics in formatted output.
func Print(processes []models.Process) {
	summary := Calculate(processes)
	fmt.Printf("Average Waiting Time:      %.2f\n", summary.AvgWaitingTime)
	fmt.Printf("Average Turnaround Time:   %.2f\n", summary.AvgTurnaroundTime)
}