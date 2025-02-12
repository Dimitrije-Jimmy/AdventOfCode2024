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
    visited = [[-1 for _ in range(cols)] for _ in range(rows)]  # -1 indicates unvisited
    queue = deque()
    queue.append((start_row, start_col))
    visited[start_row][start_col] = 0  # Distance from start to start is 0

    while queue:
        row, col = queue.popleft()
        current_distance = visited[row][col]

        #if current_distance >= target_distance:
        if current_distance > target_distance:
            continue  # We've reached or exceeded the target distance

        # Possible moves: up, down, left, right
        for delta_row, delta_col in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_row = row + delta_row
            new_col = col + delta_col

            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                cell = grid[new_row][new_col]
                if cell == '.' or cell == 'S':
                    if visited[new_row][new_col] == -1 or visited[new_row][new_col] > current_distance + 1:
                        visited[new_row][new_col] = current_distance + 1
                        queue.append((new_row, new_col))

    # Count positions at exactly target_distance
    count = 0
    for row in range(rows):
        for col in range(cols):
            if visited[row][col] == target_distance and (grid[row][col] == '.' or grid[row][col] == 'S'):
                count += 1
    return count

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    #file_path = directory+'input.txt'

    grid = read_map(file_path)
    start_pos = find_start(grid)
    if start_pos is None:
        print("Starting position 'S' not found in the map.")
        return
    start_row, start_col = start_pos
    target_distance = 6

    reachable_positions = bfs(grid, start_row, start_col, target_distance)
    print(f"Number of garden plots reachable in exactly {target_distance} steps: {reachable_positions}")

if __name__ == "__main__":
    main()
