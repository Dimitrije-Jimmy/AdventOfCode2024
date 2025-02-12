package main

import (
	"fmt"
	"os"
	"strconv"
	"unicode"
)

func calculateMulSum(inputString string) int {
	totalSum := 0
	isEnabled := true
	i := 0
	length := len(inputString)

	for i < length {
		// Check for 'do()'
		if i+4 <= length && inputString[i:i+4] == "do()" {
			isEnabled = true
			fmt.Println("do() encountered: mul instructions enabled")
			i += 4
		} else if i+7 <= length && inputString[i:i+7] == "don't()" {
			isEnabled = false
			fmt.Println("don't() encountered: mul instructions disabled")
			i += 7
		} else if i+4 <= length && inputString[i:i+4] == "mul(" {
			i += 4 // Move past 'mul('
			// Extract first number
			num1 := ""
			for i < length && unicode.IsDigit(rune(inputString[i])) {
				num1 += string(inputString[i])
				i++
			}
			// Check for ','
			if i < length && inputString[i] == ',' {
				i++ // Move past ','
			} else {
				continue // Invalid format, skip
			}
			// Extract second number
			num2 := ""
			for i < length && unicode.IsDigit(rune(inputString[i])) {
				num2 += string(inputString[i])
				i++
			}
			// Check for ')'
			if i < length && inputString[i] == ')' {
				i++ // Move past ')'
			} else {
				continue // Invalid format, skip
			}
			// Process the mul instruction
			if num1 != "" && num2 != "" {
				x, err1 := strconv.Atoi(num1)
				y, err2 := strconv.Atoi(num2)
				if err1 == nil && err2 == nil {
					product := x * y
					if isEnabled {
						totalSum += product
						fmt.Printf("mul(%d,%d) = %d (Enabled)\n", x, y, product)
					} else {
						fmt.Printf("mul(%d,%d) = %d (Disabled)\n", x, y, product)
					}
				}
			}
		} else {
			i++ // Move to the next character
		}
	}

	fmt.Printf("\nTotal Sum: %d\n", totalSum)
	return totalSum
}

/*func main() {
	inputString := "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
	calculateMulSum(inputString)
}*/

func main() {
	// Read the input string from 'input.txt'
	inputData, err := os.ReadFile("input.txt")
	if err != nil {
		fmt.Println("Error: Unable to open input.txt")
		os.Exit(1)
	}
	inputString := string(inputData)

	calculateMulSum(inputString)
}
