import numpy as np
import os
import sys
sys.setrecursionlimit(10**7)

def read_grid(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # strip whitespace and skip empty lines
    return lines
    #with open(file_path, 'r') as f:
    #    data = f.read().strip()
    #return data

def build_initial_counts(grid):
    counts = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            key = grid[i][j]
            if key in counts:
                counts[grid[i][j]] += [(i, j)]
            else:
                counts[grid[i][j]] = [(i, j)]
    return counts

def area(counts):
    counts_area = {}
    for key in counts:
        area = len(counts[key])
        counts_area[key] = area
    return counts_area
"""
def perimeter(grid, counts):
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    counts_perimeter = {}
    for key in counts:
        perimeter = 4
        for i, j in counts[key]:
            # Check if neighbours are on the grid, remove 1 from the perimeter of 4
            # grid - (n, m)

            # index (0, 0)
            if i == 0 and j == 0:
                if grid[i+1][j] == key:
                    perimeter -= 1
                if grid[i][j+1] == key:
                    perimeter -= 1
            # index (0, m)
            elif i == 0 and j == len(grid[0])-1:
                if grid[i+1][j] == key:
                    perimeter -= 1
                if grid[i][j-1] == key:
                    perimeter -= 1
            # index (n, 0)
            elif i == len(grid)-1 and j == 0:
                if grid[i-1][j] == key:
                    perimeter -= 1
                if grid[i][j+1] == key:
                    perimeter -= 1
            # index (n, m)
            elif i == len(grid)-1 and j == len(grid[0])-1:
                if grid[i-1][j] == key:
                    perimeter -= 1
                if grid[i][j-1] == key:
                    perimeter -= 1
            #[(-1, 0), (1, 0), (0, -1), (0, 1)]
            # index (0, #)
            elif i == 0 and j != 0 and j != len(grid[0])-1:
                new_neighbours = list(neighbours[1:])
                for dr, dc in new_neighbours:
                    if grid[i+dr][j+dc] == key:
                        perimeter -= 1

            # index (#, 0)
            elif i != 0 and i != len(grid)-1 and j == 0:
                new_neighbours = list(neighbours[0:2]+neighbours[3:])
                for dr, dc in new_neighbours:
                    if grid[i+dr][j+dc] == key:
                        perimeter -= 1

            # index (n, #)
            elif i == len(grid)-1 and j != 0 and j != len(grid[0])-1:
                new_neighbours = list(neighbours[:0]+neighbours[2:])
                for dr, dc in new_neighbours:
                    if grid[i+dr][j+dc] == key:
                        perimeter -= 1

            # index (#, m)
            elif i != 0 and i != len(grid)-1 and j == len(grid[0])-1:
                new_neighbours = list(neighbours[0:2])
                for dr, dc in new_neighbours:
                    if grid[i+dr][j+dc] == key:
                        perimeter -= 1

            # index (#, #)
            elif i != 0 and i != len(grid)-1 and j != 0 and j != len(grid[0])-1:
                for dr, dc in neighbours:
                    if grid[i+dr][j+dc] == key:
                        perimeter -= 1

        if counts_perimeter.get(key) is None:   
            counts_perimeter[key] = perimeter
        else:
            counts_perimeter[key] += perimeter

    return counts_perimeter
"""
def perimeter(grid, counts):
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    counts_perimeter = {}

    # For each region (key)
    for key, positions in counts.items():
        # Create a set of positions for O(1) lookups
        region_positions = set(positions)
        
        region_perimeter = 0
        for (i, j) in region_positions:
            # Check all 4 neighbors
            for dr, dc in neighbours:
                nr, nc = i + dr, j + dc
                # If neighbor is out of bounds, +1 perimeter
                if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]):
                    region_perimeter += 1
                else:
                    # If neighbor is in bounds but not the same region
                    if (nr, nc) not in region_positions:
                        region_perimeter += 1
        
        counts_perimeter[key] = region_perimeter

    return counts_perimeter


def calculate_cost(area, perimeter):
    return area*perimeter

def total_score(counts_area, counts_perimeter):
    total_score = 0
    for key in counts_area:
        total_score += calculate_cost(counts_area[key], counts_perimeter[key])
    return total_score

def main():
    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    file_path = directory+'input2.txt'

    lines = read_grid(file_path)
    print(lines)

    counts = build_initial_counts(lines)
    print(counts)

    counts_area = area(counts)
    print(counts_area)

    counts_perimeter = perimeter(lines, counts)
    print(counts_perimeter)

    score = total_score(counts_area, counts_perimeter)
    print(score)


if __name__ == "__main__":
    main()


