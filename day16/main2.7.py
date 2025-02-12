import os
import heapq
from collections import defaultdict, deque

def read_input(file_path):
    """
    Reads the input file and parses the maze map.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (grid, start_pos, end_pos)
            - grid (list of list of str): 2D grid representing the maze.
            - start_pos (tuple): (x, y) coordinates of the Start tile.
            - end_pos (tuple): (x, y) coordinates of the End tile.
    """
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
    """
    Rotates the current direction.

    Args:
        current_dir (str): Current direction ('N', 'E', 'S', 'W').
        turn (str): 'CW' for clockwise, 'CCW' for counterclockwise.

    Returns:
        str: New direction after rotation.
    """
    idx = DIRECTIONS.index(current_dir)
    if turn == 'CW':
        return DIRECTIONS[(idx + 1) % 4]
    elif turn == 'CCW':
        return DIRECTIONS[(idx - 1) % 4]
    else:
        raise ValueError("Invalid turn direction. Use 'CW' or 'CCW'.")

def print_grid(grid):
    """
    Prints the grid in a readable format.

    Args:
        grid (list of list of str): 2D grid representing the maze.
    """
    for row in grid:
        print(''.join(row))

def dijkstra_with_predecessors(grid, start_pos, end_pos):
    """
    Performs Dijkstra's algorithm to find the minimal cost paths from Start to End,
    while recording predecessor states for backtracking.

    Args:
        grid (list of list of str): 2D grid representing the maze.
        start_pos (tuple): (x, y) coordinates of the Start tile.
        end_pos (tuple): (x, y) coordinates of the End tile.

    Returns:
        tuple:
            - visited (dict): Maps (x, y, direction) to minimal cost.
            - predecessors (defaultdict): Maps (x, y, direction) to list of predecessor states.
    """
    heap = []
    initial_dir = 'E'  # Starting direction is East
    heapq.heappush(heap, (0, start_pos[0], start_pos[1], initial_dir))

    # Visited dictionary: (x, y, direction) -> cost
    visited = {}

    # Predecessors dictionary: (x, y, direction) -> list of predecessor (x_prev, y_prev, direction_prev)
    predecessors = defaultdict(list)

    while heap:
        cost, x, y, direction = heapq.heappop(heap)

        state = (x, y, direction)

        # If we've already found a better path to this state, skip it
        if state in visited and visited[state] < cost:
            continue

        # Record the minimal cost for this state
        visited[state] = cost

        # If we've reached the end, continue to process other states to find all possible predecessors
        # Do not terminate here

        # Explore possible actions

        # 1. Move Forward
        dx, dy = DIR_VECTORS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            target_cell = grid[new_y][new_x]
            if target_cell != '#':  # Can move forward
                new_state = (new_x, new_y, direction)
                new_cost = cost + 1
                if new_state not in visited or new_cost < visited[new_state]:
                    heapq.heappush(heap, (new_cost, new_x, new_y, direction))
                    predecessors[new_state].append(state)
                elif new_cost == visited.get(new_state, float('inf')):
                    predecessors[new_state].append(state)

        # 2. Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        new_state = (x, y, new_dir)
        new_cost = cost + 1000
        if new_state not in visited or new_cost < visited[new_state]:
            heapq.heappush(heap, (new_cost, x, y, new_dir))
            predecessors[new_state].append(state)
        elif new_cost == visited.get(new_state, float('inf')):
            predecessors[new_state].append(state)

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        new_state = (x, y, new_dir)
        new_cost = cost + 1000
        if new_state not in visited or new_cost < visited[new_state]:
            heapq.heappush(heap, (new_cost, x, y, new_dir))
            predecessors[new_state].append(state)
        elif new_cost == visited.get(new_state, float('inf')):
            predecessors[new_state].append(state)

    return visited, predecessors

def find_best_path_tiles(grid, start_pos, end_pos, visited, predecessors):
    """
    Identifies all tiles that are part of at least one best path.

    Args:
        grid (list of list of str): The maze grid.
        start_pos (tuple): (x, y) coordinates of the Start tile.
        end_pos (tuple): (x, y) coordinates of the End tile.
        visited (dict): Maps (x, y, direction) to minimal cost.
        predecessors (defaultdict): Maps (x, y, direction) to list of predecessor states.

    Returns:
        set: A set of (x, y) tuples representing tiles on at least one best path.
    """
    best_tiles = set()

    # Identify all end states: all states at (E_x, E_y) with minimal cost
    end_states = [state for state in visited if state[0] == end_pos[0] and state[1] == end_pos[1]]
    if not end_states:
        print("No paths found from Start to End.")
        return best_tiles

    # Find the minimal cost to reach E
    total_min_cost = min(visited[state] for state in end_states)

    # Filter end states to only those with the minimal cost
    optimal_end_states = [state for state in end_states if visited[state] == total_min_cost]

    # Use a queue for BFS traversal of predecessors
    queue = deque(optimal_end_states)
    visited_tiles = set()

    while queue:
        current_state = queue.popleft()
        x, y, direction = current_state

        if (x, y) in visited_tiles:
            continue  # Already processed this tile
        visited_tiles.add((x, y))
        best_tiles.add((x, y))

        # Traverse all predecessors of the current state
        for pred_state in predecessors.get(current_state, []):
            queue.append(pred_state)

    return best_tiles

def main():
    """
    Main function to execute the solution for Part Two.
    """
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    file_path = os.path.join(directory, 'input2.txt')
    file_path = os.path.join(directory, 'input3.txt')

    # Read and parse the input
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
    print("\nStarting Dijkstra's Algorithm...\n")

    # Perform Dijkstra's algorithm with predecessor tracking
    visited, predecessors = dijkstra_with_predecessors(grid, start_pos, end_pos)

    # Determine if End is reachable
    end_states = [state for state in visited if state[0] == end_pos[0] and state[1] == end_pos[1]]
    if not end_states:
        print("\nEnd Tile is unreachable from the Start Tile.")
        return

    # Find the minimal cost to reach E
    total_min_cost = min(visited[state] for state in end_states)
    print(f"\nLowest score to reach the End Tile: {total_min_cost}")

    # Identify all tiles that are part of at least one best path
    best_tiles = find_best_path_tiles(grid, start_pos, end_pos, visited, predecessors)

    print(f"\nNumber of tiles part of at least one best path: {len(best_tiles)}")

    # Optional: Mark the best path tiles on the grid for visualization
    marked_grid = [row.copy() for row in grid]
    for (x, y) in best_tiles:
        if (x, y) != start_pos and (x, y) != end_pos:
            marked_grid[y][x] = 'O'  # Mark with 'O'

    print("\nMarked Grid with Best Path Tiles (O):")
    print_grid(marked_grid)

if __name__ == "__main__":
    main()
