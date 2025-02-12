import os
import heapq
from collections import defaultdict, deque

def read_grid(file_path):
    """
    Reads the racetrack grid from the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: 2D grid, start position, and end position.
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


def dijkstra_with_cheats(grid, start, end, min_savings=100):
    """
    Perform Dijkstra's algorithm with cheat tracking.

    Args:
        grid (list): 2D grid.
        start (tuple): Starting position (x, y).
        end (tuple): Ending position (x, y).
        min_savings (int): Minimum time saved to count the cheat.

    Returns:
        dict: A dictionary of time saved -> count of cheats.
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heap = []
    visited = set()
    savings = defaultdict(int)

    # Initial state: cost=0, position=start, cheat_active=False
    heapq.heappush(heap, (0, start[0], start[1], False, None))

    while heap:
        cost, x, y, cheat_active, cheat_start = heapq.heappop(heap)

        # Skip if already visited
        state = (x, y, cheat_active)
        if state in visited:
            continue
        visited.add(state)

        # If we reach the end, record the cheat
        if (x, y) == end:
            if cheat_start is not None:
                time_saved = bfs(grid, start, end, allow_cheat=False) - cost
                if time_saved >= min_savings:
                    savings[time_saved] += 1
            continue

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check bounds
            if not (0 <= nx < width and 0 <= ny < height):
                continue

            # If the cell is walkable
            if grid[ny][nx] in ".SE":
                heapq.heappush(heap, (cost + 1, nx, ny, cheat_active, cheat_start))

            # If the cell is a wall and we can cheat
            if grid[ny][nx] == '#' and not cheat_active:
                heapq.heappush(heap, (cost + 1, nx, ny, True, (x, y)))

    return savings


def bfs(grid, start, end, allow_cheat=False):
    """
    Perform BFS to find the shortest path.

    Args:
        grid (list): 2D grid.
        start (tuple): Starting position (x, y).
        end (tuple): Ending position (x, y).
        allow_cheat (bool): Whether to allow passing through walls.

    Returns:
        int: Shortest path cost.
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start[0], start[1], 0, False)])
    visited = set()

    while queue:
        x, y, cost, cheat_used = queue.popleft()

        if (x, y) == end:
            return cost

        state = (x, y, cheat_used)
        if state in visited:
            continue
        visited.add(state)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if grid[ny][nx] in ".SE":
                queue.append((nx, ny, cost + 1, cheat_used))

            if grid[ny][nx] == '#' and not cheat_used and allow_cheat:
                queue.append((nx, ny, cost + 1, True))

    return float('inf')


def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')
    grid, start, end = read_grid(file_path)

    # Find the shortest time without cheats
    time_without_cheat = bfs(grid, start, end, allow_cheat=False)
    print(f"Time without cheats: {time_without_cheat}")

    # Find cheats with savings
    savings = dijkstra_with_cheats(grid, start, end, min_savings=1)  # Adjust for debugging
    print("Cheat Savings:")
    for time_saved, count in sorted(savings.items()):
        print(f"Time saved: {time_saved}, Count: {count}")


if __name__ == "__main__":
    main()
