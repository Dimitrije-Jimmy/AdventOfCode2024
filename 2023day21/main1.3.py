from collections import deque

def read_map(file_path):
    with open(file_path, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]
    return grid

def find_start(grid):
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 'S':
                return row_idx, col_idx
    return None

def bfs(grid, start_row, start_col, target_distance):
    rows = len(grid)
    cols = len(grid[0])
    queue = deque()
    queue.append((start_row, start_col, 0))  # row, col, steps
    positions_at_target_distance = set()
    visited = set()  # Keep track of (row, col, steps)

    while queue:
        row, col, steps = queue.popleft()

        if steps > target_distance:
            continue  # Exceeded the target steps

        # Add position to result set if we've reached the target steps
        if steps == target_distance:
            positions_at_target_distance.add((row, col))
            continue  # No need to explore further from here

        # Possible moves: up, down, left, right
        for delta_row, delta_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + delta_row
            new_col = col + delta_col

            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                cell = grid[new_row][new_col]
                if cell == '.' or cell == 'S':
                    next_step = steps + 1
                    state = (new_row, new_col, next_step)
                    if state not in visited:
                        visited.add(state)
                        queue.append((new_row, new_col, next_step))

    return len(positions_at_target_distance)

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    file_path = directory+'input.txt'

    grid = read_map(file_path)
    start_pos = find_start(grid)
    if start_pos is None:
        print("Starting position 'S' not found in the map.")
        return
    start_row, start_col = start_pos
    target_distance = 6  # Change to 6 for the example map

    reachable_positions = bfs(grid, start_row, start_col, target_distance)
    print(f"Number of garden plots reachable in exactly {target_distance} steps: {reachable_positions}")

if __name__ == "__main__":
    main()
