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
			// Invalid opcode
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

	strOutputs := []string{}
	for _, v := range outputs {
		strOutputs = append(strOutputs, strconv.Itoa(v))
	}
	return strings.Join(strOutputs, ",")
}

func arraysEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func findMinimumAForSelfReplicatingProgram(program []int) int {
	B := 0
	C := 0
	// Increase this limit as needed
	minA := 1900000000
	maxA := 10000000000000
	//		801940000
	/*		197780000
		197730000, not a solution yet...
	Checked A = 197740000, not a solution yet...
	Checked A = 197750000, not a solution yet...
	Checked A = 197760000, not a solution yet...
	Checked A = 197770000, not a solution yet...
	  Checked A =  197780000*/
	//Checked A = 1517390000
	//Checked A = 1884780000
	// Pyton code: 164150000
	// Checked up to A ~10000000000 (in blocks of 100000) in main3.go
	// 		~17160000000
	//		  4294967295
	//		  4,294,967,295
	// Checked up to A ~32200000000 (in blocks of 100000) in main3.go

	// Checked up to A ~40630000000 (in blocks of 100000)
	// exit status 0xc000013a
	progStrArr := []string{}
	for _, v := range program {
		progStrArr = append(progStrArr, strconv.Itoa(v))
	}
	targetOutput := strings.Join(progStrArr, ",")

	for A := minA; A <= maxA; A++ {
		out := executeProgram(A, B, C, program)
		if out == targetOutput {
			return A
		}
		if A%10000 == 0 {
			fmt.Printf("Checked A = %d\n", A)
		}
	}
	return -1
}

func main() {
	//program := []int{0, 3, 5, 4, 3, 0}
	program := []int{2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0}
	result := findMinimumAForSelfReplicatingProgram(program)
	if result != -1 {
		fmt.Printf("The lowest positive A that causes the program to output a copy of itself: %d\n", result)
	} else {
		fmt.Println("No solution found within the search limit.")
	}
}
