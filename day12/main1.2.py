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

def get_regions(grid):
    n = len(grid)
    m = len(grid[0])
    visited = [[False]*m for _ in range(n)]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    regions = []
    
    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                # Start a new region from this cell
                letter = grid[i][j]
                region_positions = []
                
                # BFS or DFS
                stack = [(i,j)]
                visited[i][j] = True
                
                while stack:
                    r, c = stack.pop()
                    region_positions.append((r,c))
                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < n and 0 <= nc < m:
                            if not visited[nr][nc] and grid[nr][nc] == letter:
                                visited[nr][nc] = True
                                stack.append((nr,nc))
                
                # Now region_positions contains one entire region of the same letter
                regions.append((letter, region_positions))
    
    return regions

def calculate_perimeter(region_positions, grid):
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    region_set = set(region_positions)
    perimeter = 0

    for (i, j) in region_positions:
        for dr, dc in directions:
            nr, nc = i+dr, j+dc
            if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]):
                perimeter += 1
            else:
                if (nr, nc) not in region_set:
                    perimeter += 1
            
    return perimeter

def solve(grid):
    regions = get_regions(grid)
    total_cost = 0
    for letter, region_positions in regions:
        area = len(region_positions)
        perim = calculate_perimeter(region_positions, grid)
        cost = area * perim
        total_cost += cost
    return total_cost


def main():
    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    file_path = directory+'input2.txt'

    lines = read_grid(file_path)
    print(lines)

    score = solve(lines)
    print(score)


if __name__ == "__main__":
    main()
    # part1: 1930
    # part1: 1518548

    # part2: 1240
    # part2: 917174

    """
    Mistake je bil da sem hotu delat z dictionarijem in mi je zato mergal iste letter regione
     ki so naceloma disconnected. Cant work with dicts this time.
    """