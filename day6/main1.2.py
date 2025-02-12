import re
import numpy as np
import pprint as pp

def read_map(file_path):
    with open(file_path, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]
    return grid

def find_start(grid):
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == '^':
                return row_idx, col_idx
    return None


def solve(grid):
    # Example input reading. Replace this with actual input reading logic.
    # In practice, you'll read lines from a file or standard input.
    # Here, we'll assume `lines` is a list of strings representing the map.
    lines = [
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#..."
    ]

    # Convert map into a 2D list for easy manipulation
    #grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions in order: Up, Right, Down, Left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_symbols = {'^': 0, '>': 1, 'v': 2, '<': 3}

    # Find guard initial position and direction
    guard_r = guard_c = None
    guard_dir = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in dir_symbols:
                guard_r, guard_c = r, c
                guard_dir = dir_symbols[grid[r][c]]
                grid[r][c] = '.'  # Replace with '.' after recording direction
                break
        if guard_r is not None:
            break

    # Check we found a guard start
    if guard_r is None or guard_c is None or guard_dir is None:
        raise ValueError("Guard start not found in the map")

    visited = set()
    visited.add((guard_r, guard_c))

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    while True:
        # Check the cell in front
        dr, dc = directions[guard_dir]
        front_r = guard_r + dr
        front_c = guard_c + dc

        # If out of bounds or obstacle, turn right
        if not in_bounds(front_r, front_c) or grid[front_r][front_c] == '#':
            guard_dir = (guard_dir + 1) % 4
        else:
            # Move forward
            guard_r, guard_c = front_r, front_c
            # Check if after move we are out of the map
            if not in_bounds(guard_r, guard_c):
                # Guard leaves the area
                break
            visited.add((guard_r, guard_c))

    # Now visited contains all distinct positions the guard visited
    print("Number of distinct positions visited:", len(visited))

    # (Optional) Marking visited positions with 'X'
    for (r, c) in visited:
        grid[r][c] = 'X'
    # Print the final map
    for row in grid:
        print(''.join(row))

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    #file_path = directory+'input.txt'

    grid = read_map(file_path)
    grid = np.array(grid)
    #pp.pprint(grid)
    #print(grid)
    start_pos = find_start(grid)

    if start_pos is None:
        print("Starting position 'S' not found in the map.")
        return
    start_row, start_col = start_pos

    solve(grid)
    
if __name__ == "__main__":
    main()