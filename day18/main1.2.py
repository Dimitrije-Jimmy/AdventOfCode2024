import os
import heapq
import pprint as pp

def read_input(file_path):
    """Reads the input and parses it into a list of (x, y) coordinates."""
    with open(file_path, 'r') as f:
        coords = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]
    return coords

def make_grid(coords, num_bytes, width, height):
    """Creates a grid and marks corrupted cells based on input coordinates."""
    grid = [['.' for _ in range(width + 1)] for _ in range(height + 1)]
    for i in range(min(num_bytes, len(coords))):
        x, y = coords[i]
        grid[y][x] = '#'
    return grid

def dijkstra(grid, start_pos, end_pos):
    """Finds the shortest path using Dijkstra's algorithm."""
    width, height = len(grid[0]), len(grid)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, Up, Right, Left
    heap = [(0, start_pos)]  # Priority queue: (cost, (x, y))
    visited = set()

    while heap:
        cost, (x, y) = heapq.heappop(heap)

        # If we reached the end position
        if (x, y) == end_pos:
            return cost

        # Skip if already visited
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != '#':
                heapq.heappush(heap, (cost + 1, (nx, ny)))

    # If no path found
    return -1

def main():
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')

    # Read and parse the input
    coords = read_input(file_path)

    # Define the grid size
    width, height = 6, 6
    num_bytes = 12
    width, height = 70, 70
    num_bytes = 1024

    # Create the grid
    grid = make_grid(coords, num_bytes, width, height)
    #pp.pprint(grid)
    print(grid)

    # Define start and end positions
    start_pos = (0, 0)
    end_pos = (width, height)

    # Run Dijkstra's algorithm
    shortest_path_cost = dijkstra(grid, start_pos, end_pos)

    print(f"The minimum number of steps needed to reach the exit: {shortest_path_cost}")

if __name__ == "__main__":
    main()
