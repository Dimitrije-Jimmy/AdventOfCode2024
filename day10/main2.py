import numpy as np
import os
import sys
sys.setrecursionlimit(10**7)  # If needed for large input

def read_grid(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # strip whitespace and skip empty lines
    return lines

def neighbors(y, x, h, w):
    for ny, nx in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]:
        if 0 <= ny < h and 0 <= nx < w:
            yield ny, nx

def solve(lines):
    h = len(lines)
    w = len(lines[0])
    
    heights = [[int(ch) for ch in line] for line in lines]
    
    memo = [[None] * w for _ in range(h)]
    
    def dfs(y, x):
        # If memoized, return
        if memo[y][x] is not None:
            return memo[y][x]
        
        current_height = heights[y][x]
        # If current cell is 9, reachable set is just this cell
        if current_height == 9:
            memo[y][x] = {(y, x)}
            return memo[y][x]
        
        #result = set()
        # For part two instead of a union of unique sets you just sum up all possible sets
        result = []
        # Look for neighbors with height = current_height + 1
        for ny, nx in neighbors(y, x, h, w):
            if heights[ny][nx] == current_height + 1:
                #result |= dfs(ny, nx)  # union sets
                result += dfs(ny, nx)  # union sets
        
        memo[y][x] = result
        
        return result
    
    # Identify trailheads (cells with height 0)
    trailheads = [(y, x) for y in range(h) for x in range(w) if heights[y][x] == 0]

    total_score = 0
    for (y0, x0) in trailheads:
        reachable_nines = dfs(y0, x0)
        # Score is number of distinct '9' cells reachable
        score = len(reachable_nines)
        total_score += score
    
    return total_score

def main():
    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    file_path = directory+'input2.txt'

    lines = read_grid(file_path)

    total_score = solve(lines)
    
    print(total_score)

if __name__ == "__main__":
    main()

