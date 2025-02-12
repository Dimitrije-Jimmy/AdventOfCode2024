import os
import numpy as np

def read_map(file_path):
    with open(file_path, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]
    return grid

def find_start(grid):
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell in ['^', '>', 'v', '<']:
                return row_idx, col_idx
    return None

def main():
    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'  # Adjust filename as needed
    file_path = directory+'input2.txt'  # Adjust filename as needed

    grid = read_map(file_path)
    grid = np.array(grid, dtype=str)
    start_pos = find_start(grid)

    if start_pos is None:
        print("Starting position (guard) not found in the map.")
        return
    guard_r, guard_c = start_pos

    # Directions in order: Up, Right, Down, Left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_symbols = {'^': 0, '>': 1, 'v': 2, '<': 3}

    rows, cols = grid.shape

    # Identify initial direction
    guard_dir = None
    if grid[guard_r, guard_c] in dir_symbols:
        guard_dir = dir_symbols[grid[guard_r, guard_c]]
        # Replace guard direction symbol with '.' after recording it
        grid[guard_r, guard_c] = '.'
    else:
        raise ValueError("Guard start position found, but no direction symbol.")

    visited = set()
    visited.add((guard_r, guard_c))

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    steps = 0  # Step counter for progress updates

    # Run the simulation while the guard is inside the map
    while in_bounds(guard_r, guard_c):
        steps += 1
        if steps % 1000 == 0:
            print(f"Steps taken: {steps}, Position: ({guard_r}, {guard_c}), Direction index: {guard_dir}")

        dr, dc = directions[guard_dir]
        front_r = guard_r + dr
        front_c = guard_c + dc

        # If front cell is out of bounds or an obstacle, turn right
        if not in_bounds(front_r, front_c) or grid[front_r, front_c] == '#':
            guard_dir = (guard_dir + 1) % 4
        else:
            # Move forward
            guard_r, guard_c = front_r, front_c
            visited.add((guard_r, guard_c))

    # Once the guard is out of bounds, we stop. visited contains all visited positions.
    print("Number of distinct positions visited:", len(visited))

    # (Optional) Mark visited positions with 'X'
    for (r, c) in visited:
        if in_bounds(r, c):  # Extra check, though all visited should be in bounds
            grid[r, c] = 'X'

    # Print the final map
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    main()
