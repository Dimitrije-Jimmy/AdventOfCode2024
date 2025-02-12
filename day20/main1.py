import os
from collections import deque

def read_grid(file_path):
    """
    Reads the racetrack grid from the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list: 2D list representing the grid.
        tuple: Start position (x, y).
        tuple: End position (x, y).
    """
    grid = []
    start = end = None
    with open(file_path, 'r') as f:
        for y, line in enumerate(f):
            row = list(line.strip())
            grid.append(row)
            if 'S' in row:
                start = (row.index('S'), y)
            if 'E' in row:
                end = (row.index('E'), y)
    return grid, start, end


def bfs(grid, start, end, allow_cheat=False):
    """
    Performs BFS to find the shortest path with optional cheating.

    Args:
        grid (list): 2D list representing the grid.
        start (tuple): Start position (x, y).
        end (tuple): End position (x, y).
        allow_cheat (bool): Whether to allow cheating.

    Returns:
        int: Shortest time to reach the end.
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start[0], start[1], 0, 0)])  # x, y, cost, cheats_used
    visited = set()

    while queue:
        x, y, cost, cheats_used = queue.popleft()

        if (x, y, cheats_used) in visited:
            continue
        visited.add((x, y, cheats_used))

        if (x, y) == end:
            return cost

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == '.' or grid[ny][nx] in 'SE':
                    queue.append((nx, ny, cost + 1, cheats_used))
                elif grid[ny][nx] == '#' and allow_cheat and cheats_used < 2:
                    queue.append((nx, ny, cost + 1, cheats_used + 1))

    return float('inf')


def count_cheats(grid, start, end, time_without_cheat):
    """
    Counts the number of cheats that save at least 100 picoseconds.

    Args:
        grid (list): 2D list representing the grid.
        start (tuple): Start position (x, y).
        end (tuple): End position (x, y).
        time_without_cheat (int): Time without any cheat.

    Returns:
        int: Number of cheats saving at least 100 picoseconds.
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    cheats_count = 0

    for y in range(height):
        for x in range(width):
            if grid[y][x] == '#':
                # Temporarily make this cell walkable to simulate a cheat
                grid[y][x] = '.'
                time_with_cheat = bfs(grid, start, end, allow_cheat=True)
                grid[y][x] = '#'  # Restore the cell

                if time_without_cheat - time_with_cheat >= 1:
                    #print(time_with_cheat)
                    cheats_count += 1

    return cheats_count


def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')
    grid, start, end = read_grid(file_path)

    # Find shortest time without any cheat
    time_without_cheat = bfs(grid, start, end, allow_cheat=False)
    print(f"Time without cheat: {time_without_cheat}")

    # Count the cheats that save at least 100 picoseconds
    cheats_count = count_cheats(grid, start, end, time_without_cheat)
    print(f"Number of cheats saving at least 100 picoseconds: {cheats_count}")


if __name__ == "__main__":
    main()
