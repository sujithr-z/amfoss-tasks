package input

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var defaultReader = bufio.NewReader(os.Stdin)

// ReadInt prompts for a non-negative integer.
func ReadInt(prompt string) int {
	return ReadIntWithReader(defaultReader, prompt)
}

// ReadIntWithReader prompts for a non-negative integer using the given reader.
func ReadIntWithReader(reader *bufio.Reader, prompt string) int {
	for {
		fmt.Print(prompt)
		input, err := reader.ReadString('\n')
		if err != nil {
			return 0
		}
		input = strings.TrimSpace(input)

		val, err := strconv.Atoi(input)
		if err == nil && val >= 0 {
			return val
		}

		fmt.Println("Invalid input. Please enter a non-negative integer.")
	}
}

// ReadPositiveInt prompts for an integer greater than 0.
func ReadPositiveInt(prompt string) int {
	return ReadPositiveIntWithReader(defaultReader, prompt)
}

// ReadPositiveIntWithReader prompts for an integer greater than 0 using the given reader.
func ReadPositiveIntWithReader(reader *bufio.Reader, prompt string) int {
	for {
		val := ReadIntWithReader(reader, prompt)
		if val > 0 {
			return val
		}
		fmt.Println("Invalid input. Value must be greater than 0.")
	}
}