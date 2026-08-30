package simulation

import (
	"fmt"
	"pirate-kings-scheduler/scheduler"
	"strings"
)

// PrintGanttChart displays an ASCII-art Gantt chart for the execution timeline.
func PrintGanttChart(timeline []scheduler.Segment) {
	if len(timeline) == 0 {
		fmt.Println("No execution timeline to display.")
		return
	}

	blockWidth := 8

	// Top border: +--------+--------+
	fmt.Print("+")
	for range timeline {
		fmt.Print(strings.Repeat("-", blockWidth) + "+")
	}
	fmt.Println()

	// Process IDs: |   P1   |   P2   |
	fmt.Print("|")
	for _, seg := range timeline {
		pad := blockWidth - len(seg.PID)
		if pad < 0 {
			pad = 0
		}
		leftPad := pad / 2
		rightPad := pad - leftPad
		fmt.Printf("%s%s%s|", strings.Repeat(" ", leftPad), seg.PID, strings.Repeat(" ", rightPad))
	}
	fmt.Println()

	// Bottom border: +--------+--------+
	fmt.Print("+")
	for range timeline {
		fmt.Print(strings.Repeat("-", blockWidth) + "+")
	}
	fmt.Println()

	// Time markers line: 0       4       9
	// Each slot occupies (blockWidth + 1) characters
	fmt.Printf("%d", timeline[0].Start)
	currentCol := len(fmt.Sprintf("%d", timeline[0].Start))

	for i := 0; i < len(timeline); i++ {
		targetCol := (i + 1) * (blockWidth + 1)
		timeStr := fmt.Sprintf("%d", timeline[i].End)
		spaces := targetCol - currentCol - (len(timeStr) - 1)
		if spaces < 1 {
			spaces = 1
		}
		fmt.Printf("%s%s", strings.Repeat(" ", spaces), timeStr)
		currentCol += spaces + len(timeStr)
	}
	fmt.Println()
}