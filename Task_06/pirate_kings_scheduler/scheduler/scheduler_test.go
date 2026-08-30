package scheduler

import (
	"pirate-kings-scheduler/models"
	"testing"
)

func TestFCFS(t *testing.T) {
	procs := []models.Process{
		{ID: "P1", ArrivalTime: 0, BurstTime: 4},
		{ID: "P2", ArrivalTime: 1, BurstTime: 3},
		{ID: "P3", ArrivalTime: 2, BurstTime: 1},
	}

	result := RunFCFS(procs)

	if len(result.Processes) != 3 {
		t.Fatalf("expected 3 processes, got %d", len(result.Processes))
	}

	// P1: Start 0, CT 4, TAT 4, WT 0
	// P2: Start 4, CT 7, TAT 6, WT 3
	// P3: Start 7, CT 8, TAT 6, WT 5
	p1 := result.Processes[0]
	p2 := result.Processes[1]
	p3 := result.Processes[2]

	if p1.CompletionTime != 4 || p1.WaitingTime != 0 || p1.TurnaroundTime != 4 {
		t.Errorf("P1 mismatch: got CT=%d WT=%d TAT=%d", p1.CompletionTime, p1.WaitingTime, p1.TurnaroundTime)
	}
	if p2.CompletionTime != 7 || p2.WaitingTime != 3 || p2.TurnaroundTime != 6 {
		t.Errorf("P2 mismatch: got CT=%d WT=%d TAT=%d", p2.CompletionTime, p2.WaitingTime, p2.TurnaroundTime)
	}
	if p3.CompletionTime != 8 || p3.WaitingTime != 5 || p3.TurnaroundTime != 6 {
		t.Errorf("P3 mismatch: got CT=%d WT=%d TAT=%d", p3.CompletionTime, p3.WaitingTime, p3.TurnaroundTime)
	}
}

func TestSJF(t *testing.T) {
	procs := []models.Process{
		{ID: "P1", ArrivalTime: 0, BurstTime: 7},
		{ID: "P2", ArrivalTime: 2, BurstTime: 4},
		{ID: "P3", ArrivalTime: 4, BurstTime: 1},
		{ID: "P4", ArrivalTime: 5, BurstTime: 4},
	}

	result := RunSJF(procs)

	// Timeline:
	// P1: runs 0 to 7 (CT=7, WT=0, TAT=7)
	// At t=7: P2 (BT=4), P3 (BT=1), P4 (BT=4) are available.
	// P3 chosen: runs 7 to 8 (CT=8, WT=8-4-1=3, TAT=8-4=4)
	// At t=8: P2 and P4 available. P2 arrived first: runs 8 to 12 (CT=12, WT=12-2-4=6, TAT=12-2=10)
	// At t=12: P4 runs 12 to 16 (CT=16, WT=16-5-4=7, TAT=16-5=11)
	if len(result.Processes) != 4 {
		t.Fatalf("expected 4 processes, got %d", len(result.Processes))
	}

	pMap := make(map[string]models.Process)
	for _, p := range result.Processes {
		pMap[p.ID] = p
	}

	if pMap["P1"].CompletionTime != 7 || pMap["P1"].WaitingTime != 0 {
		t.Errorf("P1 mismatch: %+v", pMap["P1"])
	}
	if pMap["P3"].CompletionTime != 8 || pMap["P3"].WaitingTime != 3 {
		t.Errorf("P3 mismatch: %+v", pMap["P3"])
	}
	if pMap["P2"].CompletionTime != 12 || pMap["P2"].WaitingTime != 6 {
		t.Errorf("P2 mismatch: %+v", pMap["P2"])
	}
	if pMap["P4"].CompletionTime != 16 || pMap["P4"].WaitingTime != 7 {
		t.Errorf("P4 mismatch: %+v", pMap["P4"])
	}
}

func TestRoundRobin(t *testing.T) {
	procs := []models.Process{
		{ID: "P1", ArrivalTime: 0, BurstTime: 5},
		{ID: "P2", ArrivalTime: 1, BurstTime: 4},
		{ID: "P3", ArrivalTime: 2, BurstTime: 2},
		{ID: "P4", ArrivalTime: 4, BurstTime: 1},
	}

	result := RunRR(procs, 2)

	pMap := make(map[string]models.Process)
	for _, p := range result.Processes {
		pMap[p.ID] = p
	}

	// Execution:
	// t=0: P1 (rem 5) runs [0,2] -> rem 3. Arrived at t=1: P2, t=2: P3. Queue: [P2, P3, P1]
	// t=2: P2 (rem 4) runs [2,4] -> rem 2. Arrived at t=4: P4. Queue: [P3, P1, P4, P2]
	// t=4: P3 (rem 2) runs [4,6] -> rem 0 (Finished CT=6, TAT=6-2=4, WT=4-2=2). Queue: [P1, P4, P2]
	// t=6: P1 (rem 3) runs [6,8] -> rem 1. Queue: [P4, P2, P1]
	// t=8: P4 (rem 1) runs [8,9] -> rem 0 (Finished CT=9, TAT=9-4=5, WT=5-1=4). Queue: [P2, P1]
	// t=9: P2 (rem 2) runs [9,11] -> rem 0 (Finished CT=11, TAT=11-1=10, WT=10-4=6). Queue: [P1]
	// t=11: P1 (rem 1) runs [11,12] -> rem 0 (Finished CT=12, TAT=12-0=12, WT=12-5=7). Queue: []

	if pMap["P3"].CompletionTime != 6 || pMap["P3"].WaitingTime != 2 {
		t.Errorf("P3 mismatch: got CT=%d WT=%d", pMap["P3"].CompletionTime, pMap["P3"].WaitingTime)
	}
	if pMap["P4"].CompletionTime != 9 || pMap["P4"].WaitingTime != 4 {
		t.Errorf("P4 mismatch: got CT=%d WT=%d", pMap["P4"].CompletionTime, pMap["P4"].WaitingTime)
	}
	if pMap["P2"].CompletionTime != 11 || pMap["P2"].WaitingTime != 6 {
		t.Errorf("P2 mismatch: got CT=%d WT=%d", pMap["P2"].CompletionTime, pMap["P2"].WaitingTime)
	}
	if pMap["P1"].CompletionTime != 12 || pMap["P1"].WaitingTime != 7 {
		t.Errorf("P1 mismatch: got CT=%d WT=%d", pMap["P1"].CompletionTime, pMap["P1"].WaitingTime)
	}
}
