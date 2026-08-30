package models

type Process struct {
	ID             string
	ArrivalTime    int
	BurstTime      int
	StartTime      int
	CompletionTime int
	WaitingTime    int
	TurnaroundTime int
}