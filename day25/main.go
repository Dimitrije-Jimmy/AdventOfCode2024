package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

// readInput reads a file, removes blank lines, and returns a slice of strings.
func readInput(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			lines = append(lines, line)
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
}

func main() {
	filePath := "input2.txt"
	lines, err := readInput(filePath)
	if err != nil {
		log.Fatal("Error reading file: ", err)
	}

	// For demonstration, just print them:
	for i, ln := range lines {
		fmt.Printf("%d: %s\n", i, ln)
	}
}
