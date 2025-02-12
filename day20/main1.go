package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"log"
	"math"
	"os"
)

type Cell struct {
	X, Y int
}

type State struct {
	Cost       int
	X, Y       int
	CheatUsed  bool
	CheatEnded bool
	CSX, CSY   *int
	CEX, CEY   *int
}

type PriorityQueue []*State

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].Cost < pq[j].Cost
}
func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}
func (pq *PriorityQueue) Push(x interface{}) {
	*pq = append(*pq, x.(*State))
}
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	*pq = old[0 : n-1]
	return item
}

func readGrid(filePath string) ([][]rune, Cell, Cell) {
	file, err := os.Open(filePath)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var grid [][]rune
	var start, end Cell
	y := 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		row := []rune(line)
		grid = append(grid, row)
		for x, ch := range row {
			if ch == 'S' {
				start = Cell{x, y}
			} else if ch == 'E' {
				end = Cell{x, y}
			}
		}
		y++
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return grid, start, end
}

func bfsNoCheat(grid [][]rune, start, end Cell) int {
	width := len(grid[0])
	height := len(grid)
	directions := []Cell{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}

	visited := make(map[Cell]bool)
	queue := []struct{ X, Y, Dist int }{{start.X, start.Y, 0}}

	for len(queue) > 0 {
		front := queue[0]
		queue = queue[1:]
		if front.X == end.X && front.Y == end.Y {
			return front.Dist
		}
		c := Cell{front.X, front.Y}
		if visited[c] {
			continue
		}
		visited[c] = true
		for _, d := range directions {
			nx, ny := front.X+d.X, front.Y+d.Y
			if nx < 0 || nx >= width || ny < 0 || ny >= height {
				continue
			}
			ch := grid[ny][nx]
			if ch == '.' || ch == 'S' || ch == 'E' {
				queue = append(queue, struct{ X, Y, Dist int }{nx, ny, front.Dist + 1})
			}
		}
	}
	return math.MaxInt32
}

func dijkstraWithOneCheatStep(grid [][]rune, start, end Cell, baseCost, minSavings int) (map[[2]Cell]int, int) {
	width := len(grid[0])
	height := len(grid)
	directions := []Cell{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}

	// State: cost, x, y, cheatUsed, cheatEnded, c_sx, c_sy, c_ex, c_ey
	// We'll store visited as a map with a key:
	// key: (x, y, cheatUsed, cheatEnded, c_sx, c_sy, c_ex, c_ey)
	// However, c_ex, c_ey can be nil until cheat ended, same for c_sx, c_sy.
	// We'll store positions as integers:
	// If c_sx == nil, store as -1. Similarly for others.

	toInt := func(val *int) int {
		if val == nil {
			return -1
		}
		return *val
	}

	startState := &State{
		Cost: 0, X: start.X, Y: start.Y,
		CheatUsed: false, CheatEnded: false,
		CSX: nil, CSY: nil, CEX: nil, CEY: nil,
	}

	pq := &PriorityQueue{}
	heap.Init(pq)
	heap.Push(pq, startState)

	visited := make(map[[8]int]bool)
	cheatScenarios := make(map[[2]Cell]int)

	popCount := 0
	for pq.Len() > 0 {
		s := heap.Pop(pq).(*State)
		popCount++
		if popCount%100000 == 0 {
			fmt.Printf("Processed %d states...\n", popCount)
		}

		key := [8]int{s.X, s.Y, btoi(s.CheatUsed), btoi(s.CheatEnded), toInt(s.CSX), toInt(s.CSY), toInt(s.CEX), toInt(s.CEY)}
		if visited[key] {
			continue
		}
		visited[key] = true

		if s.X == end.X && s.Y == end.Y {
			// Check scenario validity
			if s.CheatUsed && s.CheatEnded && s.CSX != nil && s.CSY != nil && s.CEX != nil && s.CEY != nil && s.Cost < baseCost {
				timeSaved := baseCost - s.Cost
				scenarioKey := [2]Cell{{*s.CSX, *s.CSY}, {*s.CEX, *s.CEY}}
				if best, ok := cheatScenarios[scenarioKey]; !ok || best < timeSaved {
					cheatScenarios[scenarioKey] = timeSaved
				}
			}
			continue
		}

		for _, d := range directions {
			nx, ny := s.X+d.X, s.Y+d.Y
			if nx < 0 || nx >= width || ny < 0 || ny >= height {
				continue
			}

			ch := grid[ny][nx]
			newCost := s.Cost + 1

			if ch == '.' || ch == 'S' || ch == 'E' {
				// Track cell
				if s.CheatUsed && !s.CheatEnded {
					// Ending cheat now
					cx, cy := nx, ny
					ns := &State{
						Cost: newCost,
						X:    nx, Y: ny,
						CheatUsed:  true,
						CheatEnded: true,
						CSX:        s.CSX, CSY: s.CSY,
						CEX: &cx, CEY: &cy,
					}
					heap.Push(pq, ns)
				} else {
					ns := &State{
						Cost: newCost,
						X:    nx, Y: ny,
						CheatUsed:  s.CheatUsed,
						CheatEnded: s.CheatEnded,
						CSX:        s.CSX, CSY: s.CSY,
						CEX: s.CEX, CEY: s.CEY,
					}
					heap.Push(pq, ns)
				}
			} else {
				// Wall cell
				if s.CheatEnded {
					// Can't cheat anymore
					continue
				}
				if !s.CheatUsed {
					// Use single cheat step here
					sx, sy := s.X, s.Y
					ns := &State{
						Cost: newCost,
						X:    nx, Y: ny,
						CheatUsed:  true,
						CheatEnded: false,
						CSX:        &sx, CSY: &sy,
						CEX: nil, CEY: nil,
					}
					heap.Push(pq, ns)
				} else {
					// Already used cheat once, cannot do again
					continue
				}
			}
		}
	}

	count100 := 0
	for _, v := range cheatScenarios {
		if v >= minSavings {
			count100++
		}
	}

	return cheatScenarios, count100
}

func btoi(b bool) int {
	if b {
		return 1
	}
	return 0
}

func main() {
	filePath := "C:\\Programming\\Personal Projects\\AdventOfCode2024\\day20\\input.txt"
	//filePath := "C:\\Programming\\Personal Projects\\AdventOfCode2024\\day20\\input2.txt"
	grid, start, end := readGrid(filePath)

	timeWithoutCheat := bfsNoCheat(grid, start, end)
	fmt.Printf("Time without cheats: %d\n", timeWithoutCheat)

	cheatScenarios, count100 := dijkstraWithOneCheatStep(grid, start, end, timeWithoutCheat, 100)

	savingsCount := make(map[int]int)
	for _, ts := range cheatScenarios {
		savingsCount[ts]++
	}

	fmt.Println("All Cheats by Time Saved:")
	keys := make([]int, 0, len(savingsCount))
	for k := range savingsCount {
		keys = append(keys, k)
	}
	// Sort keys
	for i := 0; i < len(keys)-1; i++ {
		for j := i + 1; j < len(keys); j++ {
			if keys[i] > keys[j] {
				keys[i], keys[j] = keys[j], keys[i]
			}
		}
	}
	for _, k := range keys {
		fmt.Printf("Time saved: %d, Count: %d\n", k, savingsCount[k])
	}
	fmt.Printf("\nNumber of cheats that save at least 100 picoseconds: %d\n", count100)
}
