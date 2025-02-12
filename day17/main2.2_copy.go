package main

import (
	"fmt"
	"strconv"
	"strings"
)

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
			denom := 1 << operandValue
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
			denom := 1 << operandValue
			if denom == 0 {
				return ""
			}
			B = A / denom
			IP += 2

		case 7: // cdv
			denom := 1 << operandValue
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

func findMinimumAForSelfReplicatingProgramImproved(program []int) int {
	// Target output is the program itself:
	progStrArr := []string{}
	for _, v := range program {
		progStrArr = append(progStrArr, strconv.Itoa(v))
	}
	targetOutput := strings.Join(progStrArr, ",")
	targetLength := len(program)

	B := 0
	C := 0

	// Step 1: Coarse search in large increments
	step := 100
	var lastA int
	foundRange := false

	//		501940000
	for A := 0; A <= 1000000; A += step {
		out := executeProgram(A, B, C, program)
		olen := 0
		if out != "" {
			olen = len(strings.Split(out, ","))
		}

		// If we find the exact match right away:
		if out == targetOutput {
			return A
		}

		// Check output length relationship
		if olen >= targetLength {
			// We've reached or exceeded the length where the output might match
			// Store this position and revert to fine search
			foundRange = true
			lastA = A
			break
		}

		if A%(step*10) == 0 {
			fmt.Printf("Coarse checked A = %d\n", A)
		}
	}

	if !foundRange {
		// Could not find any range where the output length matches or exceeds
		fmt.Println("No range found where output length matches or exceeds target program length.")
		return -1
	}

	// Step 2: Fine search
	// We know at A=lastA output length >= targetLength. Let's go back step to find the exact point.
	startA := lastA - step
	if startA < 1 {
		startA = 1
	}

	for A := startA; A <= lastA; A++ {
		out := executeProgram(A, B, C, program)
		if out == targetOutput {
			return A
		}
	}

	// If not found in that range, maybe the output length was just coincidentally large
	// and not correct. You could refine the logic further if needed.
	fmt.Println("No exact match found in the identified range.")
	return -1
}

func main() {
	// Example usage with given program:
	program := []int{0, 3, 5, 4, 3, 0}
	//program := []int{2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0}
	result := findMinimumAForSelfReplicatingProgramImproved(program)
	if result != -1 {
		fmt.Printf("The lowest positive A that causes the program to output a copy of itself: %d\n", result)
	} else {
		fmt.Println("No solution found.")
	}
}
