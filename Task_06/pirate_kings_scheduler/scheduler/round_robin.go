package scheduler

import (
	"pirate-kings-scheduler/models"
	"sort"
)

// RoundRobin represents the Round Robin (Preemptive) scheduling algorithm.
type RoundRobin struct {
	Quantum int
}

func NewRoundRobin(quantum int) *RoundRobin {
	return &RoundRobin{Quantum: quantum}
}

func (rr *RoundRobin) Run(processes []models.Process) SimulationResult {
	return RunRR(processes, rr.Quantum)
}

// RunRR executes Round Robin scheduling with a given time quantum.
func RunRR(processes []models.Process, quantum int) SimulationResult {
	n := len(processes)
	if n == 0 {
		return SimulationResult{Processes: []models.Process{}, Timeline: []Segment{}}
	}
	if quantum <= 0 {
		quantum = 1
	}

	procs := make([]models.Process, n)
	copy(procs, processes)

	// Sort initially by ArrivalTime, then ID
	sort.Slice(procs, func(i, j int) bool {
		if procs[i].ArrivalTime == procs[j].ArrivalTime {
			return procs[i].ID < procs[j].ID
		}
		return procs[i].ArrivalTime < procs[j].ArrivalTime
	})

	remainingBurst := make(map[string]int)
	started := make(map[string]bool)
	procMap := make(map[string]*models.Process)

	for i := range procs {
		p := &procs[i]
		remainingBurst[p.ID] = p.BurstTime
		procMap[p.ID] = p
	}

	var timeline []Segment
	var queue []string
	enqueued := make(map[string]bool)

	currentTime := 0
	nextArrivalIdx := 0

	enqueueArrived := func() {
		for nextArrivalIdx < n && procs[nextArrivalIdx].ArrivalTime <= currentTime {
			pid := procs[nextArrivalIdx].ID
			if !enqueued[pid] {
				queue = append(queue, pid)
				enqueued[pid] = true
			}
			nextArrivalIdx++
		}
	}

	if procs[0].ArrivalTime > currentTime {
		currentTime = procs[0].ArrivalTime
	}
	enqueueArrived()

	var completedOrder []models.Process

	for len(queue) > 0 || nextArrivalIdx < n {
		if len(queue) == 0 {
			if nextArrivalIdx < n {
				currentTime = procs[nextArrivalIdx].ArrivalTime
				enqueueArrived()
			}
			continue
		}

		currPID := queue[0]
		queue = queue[1:]

		p := procMap[currPID]

		if !started[currPID] {
			started[currPID] = true
			p.StartTime = currentTime
		}

		execTime := quantum
		if remainingBurst[currPID] < quantum {
			execTime = remainingBurst[currPID]
		}

		start := currentTime
		end := currentTime + execTime
		currentTime = end
		remainingBurst[currPID] -= execTime

		timeline = append(timeline, Segment{
			PID:   currPID,
			Start: start,
			End:   end,
		})

		// Enqueue newly arrived processes during this time slice before re-queuing currPID
		enqueueArrived()

		if remainingBurst[currPID] > 0 {
			queue = append(queue, currPID)
		} else {
			p.CompletionTime = currentTime
			p.TurnaroundTime = p.CompletionTime - p.ArrivalTime
			p.WaitingTime = p.TurnaroundTime - p.BurstTime
			completedOrder = append(completedOrder, *p)
		}
	}

	return SimulationResult{
		Processes: completedOrder,
		Timeline:  timeline,
	}
}