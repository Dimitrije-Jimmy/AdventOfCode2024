package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// KeypadAdjacency represents the movement adjacency for a keypad
type KeypadAdjacency map[string]map[string]string

// State represents the current button and the index in the target string
type State struct {
	button string
	index  int
}

// BFS finds the minimal number of button presses to type the target string on the given keypad
func BFS(start string, target string, adjacency KeypadAdjacency) int {
	queue := []State{{button: start, index: 0}}
	steps := 0

	visited := make(map[string]bool)
	startKey := fmt.Sprintf("%s,%d", start, 0)
	visited[startKey] = true

	for len(queue) > 0 {
		levelSize := len(queue)
		for i := 0; i < levelSize; i++ {
			current := queue[0]
			queue = queue[1:]

			// If we've typed the entire target string
			if current.index == len(target) {
				return steps
			}

			// Explore all possible move commands: '^', 'v', '<', '>'
			for moveCmd, neighbor := range adjacency[current.button] {
				if neighbor == "" || neighbor == "None" {
					continue
				}

				nextState := State{button: neighbor, index: current.index}
				key := fmt.Sprintf("%s,%d", nextState.button, nextState.index)
				if !visited[key] {
					visited[key] = true
					queue = append(queue, nextState)
				}
			}

			// Attempt to press 'A' if the current button matches the next character to type
			if current.index < len(target) && current.button == string(target[current.index]) {
				nextState := State{button: current.button, index: current.index + 1}
				key := fmt.Sprintf("%s,%d", nextState.button, nextState.index)
				if !visited[key] {
					visited[key] = true
					queue = append(queue, nextState)
				}
			}
		}
		steps++
	}

	// If the target string cannot be typed
	return -1
}

// ReadCodes reads codes from a file, each code on a separate line
func ReadCodes(filePath string) ([]string, error) {
	var codes []string

	file, err := os.Open(filePath)
	if err != nil {
		return codes, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		code := strings.TrimSpace(scanner.Text())
		if code != "" {
			codes = append(codes, code)
		}
	}

	if err := scanner.Err(); err != nil {
		return codes, err
	}

	return codes, nil
}

func main() {
	// Define the numeric keypad adjacency
	numericKeypadAdjacency := KeypadAdjacency{
		"7": {"^": "None", "v": "4", "<": "None", ">": "8"},
		"8": {"^": "None", "v": "5", "<": "7", ">": "9"},
		"9": {"^": "None", "v": "6", "<": "8", ">": "None"},
		"4": {"^": "7", "v": "1", "<": "None", ">": "5"},
		"5": {"^": "8", "v": "2", "<": "4", ">": "6"},
		"6": {"^": "9", "v": "3", "<": "5", ">": "None"},
		"1": {"^": "4", "v": "None", "<": "None", ">": "2"},
		"2": {"^": "5", "v": "None", "<": "1", ">": "3"},
		"3": {"^": "6", "v": "A", "<": "2", ">": "None"},
		"0": {"^": "2", "v": "None", "<": "None", ">": "A"},
		"A": {"^": "3", "v": "None", "<": "0", ">": "None"},
	}

	// Define the directional keypad adjacency
	directionalKeypadAdjacency := KeypadAdjacency{
		"^": {"^": "None", "v": "v", "<": "None", ">": "A"},
		"v": {"^": "^", "v": "None", "<": "<", ">": ">"},
		"<": {"^": "None", "v": "None", "<": "None", ">": "v"},
		">": {"^": "A", "v": "None", "<": "v", ">": "None"},
		"A": {"^": "None", "v": ">", "<": "^", ">": "None"},
	}

	// Read codes from input.txt
	codes, err := ReadCodes("C:\\Programming\\Personal Projects\\AdventOfCode2024\\day21\\input2.txt")
	if err != nil {
		fmt.Println("Error reading input:", err)
		return
	}

	fmt.Println("Codes to type:", codes)
	fmt.Println()

	totalComplexity := 0

	for _, code := range codes {
		fmt.Printf("Processing Code: %s\n", code)

		// Extract the numeric part of the code (remove leading zeros and the trailing 'A')
		numericStr := strings.TrimLeft(code[:len(code)-1], "0")
		if numericStr == "" {
			numericStr = "0"
		}
		numericPart, err := strconv.Atoi(numericStr)
		if err != nil {
			fmt.Printf("  Invalid numeric part in code: %s\n", code)
			continue
		}

		// Step 1: Find minimal steps to type the code on the numeric keypad (L1)
		L1_steps := BFS("A", code, numericKeypadAdjacency)
		if L1_steps == -1 {
			fmt.Printf("  No valid L1 sequence found for code: %s\n", code)
			continue
		}
		// fmt.Printf("  L1 steps: %d\n", L1_steps)

		// Convert the code to L1 sequence for L2
		L1_sequence := code

		// Step 2: Find minimal steps to type the L1 sequence on the first directional keypad (L2)
		L2_steps := BFS("A", L1_sequence, directionalKeypadAdjacency)
		if L2_steps == -1 {
			fmt.Printf("  No valid L2 sequence found for code: %s\n", code)
			continue
		}
		// fmt.Printf("  L2 steps: %d\n", L2_steps)

		// Convert the L1 sequence to L2 sequence for L3
		L2_sequence := L1_sequence

		// Step 3: Find minimal steps to type the L2 sequence on the second directional keypad (L3)
		L3_steps := BFS("A", L2_sequence, directionalKeypadAdjacency)
		if L3_steps == -1 {
			fmt.Printf("  No valid L3 sequence found for code: %s\n", code)
			continue
		}
		// fmt.Printf("  L3 steps: %d\n", L3_steps)

		// Step 4: Calculate complexity
		complexity := L3_steps * numericPart
		totalComplexity += complexity

		fmt.Printf("  Minimal L3 length = %d, Complexity = %d\n", L3_steps, complexity)
		fmt.Println()
	}

	fmt.Printf("Total complexity = %d\n", totalComplexity)
}
