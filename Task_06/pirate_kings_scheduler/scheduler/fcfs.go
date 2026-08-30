package scheduler

import (
	"pirate-kings-scheduler/models"
	"sort"
)

// Segment represents a continuous block of execution in the Gantt chart.
type Segment struct {
	PID   string
	Start int
	End   int
}

// SimulationResult holds the simulated processes with computed times and the Gantt timeline.
type SimulationResult struct {
	Processes []models.Process
	Timeline  []Segment
}

// Scheduler defines the standard interface for all CPU scheduling algorithms.
type Scheduler interface {
	Run(processes []models.Process) SimulationResult
}

// FCFS represents the First-Come-First-Serve scheduling algorithm.
type FCFS struct{}

func NewFCFS() *FCFS {
	return &FCFS{}
}

func (f *FCFS) Run(processes []models.Process) SimulationResult {
	return RunFCFS(processes)
}

// RunFCFS executes First-Come-First-Serve scheduling.
func RunFCFS(processes []models.Process) SimulationResult {
	n := len(processes)
	if n == 0 {
		return SimulationResult{Processes: []models.Process{}, Timeline: []Segment{}}
	}

	// Create a copy to prevent mutation of the original slice
	procs := make([]models.Process, n)
	copy(procs, processes)

	// Sort by ArrivalTime, then by ID
	sort.Slice(procs, func(i, j int) bool {
		if procs[i].ArrivalTime == procs[j].ArrivalTime {
			return procs[i].ID < procs[j].ID
		}
		return procs[i].ArrivalTime < procs[j].ArrivalTime
	})

	var timeline []Segment
	currentTime := 0

	for i := 0; i < n; i++ {
		p := &procs[i]
		if currentTime < p.ArrivalTime {
			currentTime = p.ArrivalTime
		}

		p.StartTime = currentTime
		p.CompletionTime = currentTime + p.BurstTime
		p.TurnaroundTime = p.CompletionTime - p.ArrivalTime
		p.WaitingTime = p.TurnaroundTime - p.BurstTime

		timeline = append(timeline, Segment{
			PID:   p.ID,
			Start: p.StartTime,
			End:   p.CompletionTime,
		})

		currentTime = p.CompletionTime
	}

	return SimulationResult{
		Processes: procs,
		Timeline:  timeline,
	}
}