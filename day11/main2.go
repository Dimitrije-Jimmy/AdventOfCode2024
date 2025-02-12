package main

import (
	"fmt"
	"strconv"
)

func makeStep(num int) (int, *int) {
	s := strconv.Itoa(num)
	// Rule 1
	if num == 0 {
		return 1, nil
	}
	// Rule 2
	if len(s)%2 == 0 {
		half := len(s) / 2
		leftPart, _ := strconv.Atoi(s[:half])
		rightPart, _ := strconv.Atoi(s[half:])
		return leftPart, &rightPart
	}
	// Rule 3
	res := num * 2024
	return res, nil
}

func stepThrough(stones []int, blinks int) []int {
	for i := 0; i < blinks; i++ {
		newStones := make([]int, 0, len(stones)*2) // Guessing a bigger capacity
		for _, num := range stones {
			step, newNum := makeStep(num)
			newStones = append(newStones, step)
			if newNum != nil {
				newStones = append(newStones, *newNum)
			}
		}
		stones = newStones
		// Optionally print progress
		fmt.Printf("After %d blinks: %d stones\n", i+1, len(stones))
	}
	return stones
}

func main() {
	// Example initial configuration - adjust as needed.
	// For a real puzzle input, read from file or standard input.
	//stones := []int{0, 1, 10, 99, 999} // just an example
	stones := []int{64554, 35, 906, 6, 6960985, 5755, 975820, 0} // just an example
	blinks := 75

	// Run the process
	finalStones := stepThrough(stones, blinks)

	fmt.Println("Final number of stones:", len(finalStones))
}
