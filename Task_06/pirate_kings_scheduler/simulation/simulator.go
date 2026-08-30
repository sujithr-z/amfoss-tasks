package simulation

import (
	"pirate-kings-scheduler/models"
	"pirate-kings-scheduler/scheduler"
)

type Simulator struct {
	Scheduler scheduler.Scheduler
}

func New(s scheduler.Scheduler) *Simulator {
	return &Simulator{Scheduler: s}
}

func (sim *Simulator) Run(processes []models.Process) scheduler.SimulationResult {
	return sim.Scheduler.Run(processes)
}