import os
import heapq

def read_input(file_path):
    grid = []
    start_pos = None
    end_pos = None

    with open(file_path, 'r') as f:
        for y, line in enumerate(f):
            line = line.rstrip('\n')
            row = list(line)
            grid.append(row)
            for x, char in enumerate(row):
                if char == 'S':
                    start_pos = (x, y)
                elif char == 'E':
                    end_pos = (x, y)

    if start_pos is None or end_pos is None:
        raise ValueError("Start (S) or End (E) position not found in the map.")

    return grid, start_pos, end_pos

# Define directions with corresponding (dx, dy)
DIRECTIONS = ['N', 'E', 'S', 'W']
DIR_VECTORS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}

def rotate(current_dir, turn):
    idx = DIRECTIONS.index(current_dir)
    if turn == 'CW':
        return DIRECTIONS[(idx + 1) % 4]
    elif turn == 'CCW':
        return DIRECTIONS[(idx - 1) % 4]
    else:
        raise ValueError("Invalid turn direction. Use 'CW' or 'CCW'.")

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def dijkstra(grid, start_pos, end_pos, reverse=False):
    """
    Performs Dijkstra's algorithm to find the minimal cost from start_pos to end_pos or vice versa.

    Args:
        grid (list of list of str): 2D grid representing the maze.
        start_pos (tuple): (x, y) coordinates of the Start or End tile.
        end_pos (tuple): (x, y) coordinates of the End or Start tile.
        reverse (bool): If True, perform reverse search from end_pos to start_pos.

    Returns:
        dict: A dictionary mapping (x, y, direction) to the minimal cost.
    """
    heap = []
    initial_dir = 'E' if not reverse else 'W'  # Assuming reverse search starts facing West
    heapq.heappush(heap, (0, start_pos[0], start_pos[1], initial_dir))

    visited = {}

    while heap:
        cost, x, y, direction = heapq.heappop(heap)

        state = (x, y, direction)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        # If reached the target in forward search, or start in reverse search
        if (not reverse and (x, y) == end_pos):
            continue  # We want to explore all possible paths to E
        if (reverse and (x, y) == end_pos):
            continue  # In reverse search, end_pos is the new start

        # Explore possible actions

        # 1. Move Forward
        dx, dy = DIR_VECTORS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            target_cell = grid[new_y][new_x]
            if target_cell != '#':  # Can move forward
                heapq.heappush(heap, (cost + 1, new_x, new_y, direction))

        # 2. Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        heapq.heappush(heap, (cost + 1000, new_x if reverse else x, new_y if reverse else y, new_dir))

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        heapq.heappush(heap, (cost + 1000, new_x if reverse else x, new_y if reverse else y, new_dir))

    return visited

def find_best_path_tiles(grid, start_pos, end_pos, total_min_cost, cost_from_start, cost_to_end):
    """
    Identifies all tiles that are part of at least one best path.

    Args:
        grid (list of list of str): The maze grid.
        start_pos (tuple): (x, y) coordinates of the Start tile.
        end_pos (tuple): (x, y) coordinates of the End tile.
        total_min_cost (int): The minimal total cost to reach E from S.
        cost_from_start (dict): Minimal cost from S to each (x, y, direction).
        cost_to_end (dict): Minimal cost from each (x, y, direction) to E.

    Returns:
        int: Number of tiles that are part of at least one best path.
    """
    best_tiles = set()

    for (x, y, direction), cost_s in cost_from_start.items():
        print(x, y)
        # Get the cost to reach E from this state
        cost_e = cost_to_end.get((x, y, direction), float('inf'))
        if cost_s + cost_e == total_min_cost:
            best_tiles.add((x, y))

    return len(best_tiles)

def find_best_path_tiles_and_mark(grid, start_pos, end_pos, total_min_cost, cost_from_start, cost_to_end):
    best_tiles = set()

    for (x, y, direction), cost_s in cost_from_start.items():
        cost_e = cost_to_end.get((x, y, direction), float('inf'))
        if cost_s + cost_e == total_min_cost:
            best_tiles.add((x, y))

    # Create a copy of the grid to mark best path tiles
    marked_grid = [row.copy() for row in grid]
    for (x, y) in best_tiles:
        if (x, y) != start_pos and (x, y) != end_pos:
            marked_grid[y][x] = 'O'  # Mark with 'O'

    return len(best_tiles), marked_grid


def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    file_path = os.path.join(directory, 'input3.txt')
    #file_path = os.path.join(directory, 'input2.txt')

    try:
        grid, start_pos, end_pos = read_input(file_path)
    except ValueError as e:
        print(e)
        return

    print(f"Start Position: {start_pos}")
    print(f"End Position: {end_pos}\n")

    # Print the initial grid
    print("Initial Warehouse State:")
    print_grid(grid)
    print("\nStarting Dijkstra's Algorithm for Forward Search...\n")

    # Perform Dijkstra's algorithm to find the lowest score
    cost_from_start = dijkstra(grid, start_pos, end_pos, reverse=False)
    # Find the minimal cost to reach E from S
    total_min_cost = min(
        cost for (x, y, direction), cost in cost_from_start.items()
        if (x, y) == end_pos
    )

    print(f"\nLowest score to reach the End Tile: {total_min_cost}")

    print("\nStarting Dijkstra's Algorithm for Reverse Search...\n")
    # Perform Dijkstra's algorithm to find the minimal cost from each state to E
    cost_to_end = dijkstra(grid, end_pos, start_pos, reverse=True)

    print("\nIdentifying best path tiles...\n")
    # Find all tiles that are part of at least one best path
        # Find all tiles that are part of at least one best path and get the marked grid
    num_best_tiles, marked_grid = find_best_path_tiles_and_mark(
        grid, start_pos, end_pos, total_min_cost, cost_from_start, cost_to_end
    )

    print(f"Number of tiles part of at least one best path: {num_best_tiles}\n")

    # Optionally, print the marked grid
    print("Marked Grid with Best Path Tiles (O):")
    print_grid(marked_grid)


if __name__ == "__main__":
    main()
