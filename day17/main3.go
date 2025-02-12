package main

import (
	"fmt"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"
)

// executeProgram function as previously defined
func executeProgram(AInit, BInit, CInit int, program []int) string {
	A := AInit
	B := BInit
	C := CInit
	IP := 0
	outputs := []int{}

	operandTypes := map[int]string{
		0: "combo",
		1: "literal",
		2: "combo",
		3: "literal",
		4: "ignored",
		5: "combo",
		6: "combo",
		7: "combo",
	}

	for IP < len(program) {
		if IP+1 >= len(program) {
			break
		}
		opcode := program[IP]
		operand := program[IP+1]
		otype, ok := operandTypes[opcode]
		if !ok {
			break
		}

		var operandValue int
		validOperand := true
		switch otype {
		case "literal":
			operandValue = operand
		case "combo":
			if operand >= 0 && operand <= 3 {
				operandValue = operand
			} else if operand == 4 {
				operandValue = A
			} else if operand == 5 {
				operandValue = B
			} else if operand == 6 {
				operandValue = C
			} else {
				// Invalid operand (7)
				validOperand = false
			}
		case "ignored":
			// operand is ignored
		default:
			validOperand = false
		}

		if !validOperand {
			return ""
		}

		switch opcode {
		case 0: // adv
			denom := 1
			for i := 0; i < operandValue; i++ {
				denom *= 2
			}
			if denom == 0 {
				return ""
			}
			A = A / denom
			IP += 2

		case 1: // bxl
			if otype != "literal" {
				return ""
			}
			B = B ^ operandValue
			IP += 2

		case 2: // bst
			if otype != "combo" {
				return ""
			}
			B = operandValue % 8
			IP += 2

		case 3: // jnz
			if otype != "literal" {
				return ""
			}
			if A != 0 {
				IP = operandValue
			} else {
				IP += 2
			}

		case 4: // bxc
			B = B ^ C
			IP += 2

		case 5: // out
			if otype != "combo" {
				return ""
			}
			outVal := operandValue % 8
			outputs = append(outputs, outVal)
			IP += 2

		case 6: // bdv
			denom := 1
			for i := 0; i < operandValue; i++ {
				denom *= 2
			}
			if denom == 0 {
				return ""
			}
			B = A / denom
			IP += 2

		case 7: // cdv
			denom := 1
			for i := 0; i < operandValue; i++ {
				denom *= 2
			}
			if denom == 0 {
				return ""
			}
			C = A / denom
			IP += 2

		default:
			// Invalid opcode
			return ""
		}
	}

	strOutputs := make([]string, len(outputs))
	for i, v := range outputs {
		strOutputs[i] = strconv.Itoa(v)
	}
	return strings.Join(strOutputs, ",")
}

// Worker function to process a block of A values
func worker(program []int, targetOutput string, startA, blockSize int, results chan<- int, done <-chan struct{}) {
	B := 0
	C := 0
	endA := startA + blockSize - 1
	for A := startA; A <= endA; A++ {
		select {
		case <-done:
			// If a result was found by another goroutine, stop
			return
		default:
			out := executeProgram(A, B, C, program)
			if out == targetOutput {
				results <- A
				return
			}
		}
	}
}

// This function sets up workers that each test blocks of 100,000 A values.
// Once a solution is found, we close the done channel to stop all workers.
func parallelSearch(program []int, startA int) int {
	// Prepare target output
	progStrArr := []string{}
	for _, v := range program {
		progStrArr = append(progStrArr, strconv.Itoa(v))
	}
	targetOutput := strings.Join(progStrArr, ",")

	blockSize := 100000
	numWorkers := runtime.NumCPU()     // Use number of CPU cores as worker count
	jobs := make(chan int, numWorkers) // each job is the starting A of a block
	results := make(chan int, 1)
	done := make(chan struct{})

	var wg sync.WaitGroup

	// Spawn workers
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for startVal := range jobs {
				worker(program, targetOutput, startVal, blockSize, results, done)
			}
		}()
	}

	// A goroutine to close done and jobs if a result is found
	go func() {
		res := <-results
		close(done)
		// Drain jobs if any
		for range jobs {
		}
		fmt.Printf("Solution found at A=%d\n", res)
	}()

	// Start assigning blocks from startA upwards
	// This loop can theoretically go on for a very large number.
	// You can break out or limit as you see fit.
	A := startA
	blockCount := 0
	printInterval := 100 // print progress every 100 blocks
	for {
		select {
		case <-done:
			// Result found
			wg.Wait()
			return -1 // -1 here means we got result via the goroutine
		default:
			// No result yet, assign next block
			jobs <- A
			A += blockSize
			blockCount++
			if blockCount%printInterval == 0 {
				fmt.Printf("Checked up to A ~%d (in blocks of %d)\n", A, blockSize)
			}
		}
		// This could run until max uint, be careful with long running searches.
		// Consider a break condition if needed.
	}
}

func main() {
	// This is the large program that we haven't found a solution for yet.
	//program := []int{2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0}
	program := []int{2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0}

	// We know we've already checked up to ~1,517,390,000
	// Start from there (pick a slightly higher number to ensure no overlap)
	//startFrom := 1517390000
	//startFrom := 1884780000
	//startFrom := 1900000000
	startFrom := 17160000000

	fmt.Printf("Starting parallel search from A=%d, stepping in blocks of 100000.\n", startFrom)

	startTime := time.Now()
	result := parallelSearch(program, startFrom)
	endTime := time.Now()

	if result != -1 {
		fmt.Printf("Lowest positive A: %d\n", result)
	} else {
		fmt.Println("Search terminated or found a solution reported above.")
	}

	fmt.Printf("Search completed in %s\n", endTime.Sub(startTime))
}
