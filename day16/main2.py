import heapq
from collections import defaultdict
import os

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

def manhattan_distance(x1, y1, x2, y2):
    """
    Calculates the Manhattan distance between two points.
    
    Args:
        x1, y1 (int): Coordinates of the first point.
        x2, y2 (int): Coordinates of the second point.
    
    Returns:
        int: Manhattan distance.
    """
    return abs(x1 - x2) + abs(y1 - y2)

def read_input(file_path):
    """
    Reads the input file and parses the warehouse map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (grid, start_pos, end_pos)
            - grid (list of list of str): 2D grid representing the warehouse.
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

def dijkstra(grid, start_pos, end_pos):
    """
    Performs Dijkstra's algorithm to find the lowest score path from Start to End.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        start_pos (tuple): (x, y) coordinates of the Start tile.
        end_pos (tuple): (x, y) coordinates of the End tile.

    Returns:
        int: The lowest total score to reach End from Start.
    """
    # Initialize the priority queue
    heap = []
    # Initial state: cost=0, position=start_pos, facing East
    initial_dir = 'E'
    heapq.heappush(heap, (0, start_pos[0], start_pos[1], initial_dir))

    # Visited dictionary: (x, y, direction) -> cost
    visited = {}

    while heap:
        cost, x, y, direction = heapq.heappop(heap)

        # If reached the end, return the cost
        if (x, y) == end_pos:
            return cost

        # If this state has been visited with a lower cost, skip
        state = (x, y, direction)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

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
        heapq.heappush(heap, (cost + 1000, x, y, new_dir))

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        heapq.heappush(heap, (cost + 1000, x, y, new_dir))

    # If End is unreachable
    return -1

def a_star(grid, start_pos, end_pos):
    """
    Performs the A* algorithm to find the lowest score path from Start to End.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        start_pos (tuple): (x, y) coordinates of the Start tile.
        end_pos (tuple): (x, y) coordinates of the End tile.

    Returns:
        int: The lowest total score to reach End from Start.
    """
    # Initialize the priority queue
    heap = []
    # Initial state: cost=0, position=start_pos, facing East
    initial_dir = 'E'
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    heuristic = manhattan_distance(start_x, start_y, end_x, end_y)
    heapq.heappush(heap, (heuristic, 0, start_x, start_y, initial_dir))

    # Visited dictionary: (x, y, direction) -> cost
    visited = {}

    while heap:
        f, cost, x, y, direction = heapq.heappop(heap)

        # If reached the end, return the cost
        if (x, y) == end_pos:
            return cost

        # If this state has been visited with a lower cost, skip
        state = (x, y, direction)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        # Explore possible actions

        # 1. Move Forward
        dx, dy = DIR_VECTORS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            target_cell = grid[new_y][new_x]
            if target_cell != '#':  # Can move forward
                new_cost = cost + 1
                heuristic = manhattan_distance(new_x, new_y, end_x, end_y)
                new_f = new_cost + heuristic
                heapq.heappush(heap, (new_f, new_cost, new_x, new_y, direction))

        # 2. Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        new_cost = cost + 1000
        heuristic = manhattan_distance(x, y, end_x, end_y)
        new_f = new_cost + heuristic
        heapq.heappush(heap, (new_f, new_cost, x, y, new_dir))

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        new_cost = cost + 1000
        heuristic = manhattan_distance(x, y, end_x, end_y)
        new_f = new_cost + heuristic
        heapq.heappush(heap, (new_f, new_cost, x, y, new_dir))

    # If End is unreachable
    return -1

def a_star_with_predecessors(grid, start_pos, end_pos):
    """
    Performs the A* algorithm to find the lowest score path from Start to End,
    and records predecessors for tracing all optimal paths.
    
    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        start_pos (tuple): (x, y) coordinates of the Start tile.
        end_pos (tuple): (x, y) coordinates of the End tile.
    
    Returns:
        tuple: (lowest_score, predecessors, optimal_end_states)
            - lowest_score (int): The lowest total score to reach End from Start.
            - predecessors (dict): Mapping from state to list of predecessor states.
            - optimal_end_states (list): List of end states with minimal cost.
    """
    # Initialize the priority queue
    heap = []
    # Initial state: cost=0, position=start_pos, facing East
    initial_dir = 'E'
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    heuristic = manhattan_distance(start_x, start_y, end_x, end_y)
    heapq.heappush(heap, (heuristic, 0, start_x, start_y, initial_dir))

    # Visited dictionary: (x, y, direction) -> cost
    visited = {}

    # Predecessors dictionary: (x, y, direction) -> list of predecessor states
    predecessors = defaultdict(list)

    while heap:
        f, cost, x, y, direction = heapq.heappop(heap)

        # If reached the end, continue to ensure all optimal paths are found
        if (x, y) == end_pos:
            if (x, y, direction) in visited and visited[(x, y, direction)] < cost:
                continue
            # Do not return immediately; continue to find all optimal paths

        # If this state has been visited with a lower cost, skip
        state = (x, y, direction)
        if state in visited and visited[state] < cost:
            continue
        elif state in visited and visited[state] == cost:
            # Multiple paths leading to the same state with the same cost
            pass
        visited[state] = cost

        # Explore possible actions

        # 1. Move Forward
        dx, dy = DIR_VECTORS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            target_cell = grid[new_y][new_x]
            if target_cell != '#':  # Can move forward
                new_cost = cost + 1
                heuristic_val = manhattan_distance(new_x, new_y, end_x, end_y)
                new_f = new_cost + heuristic_val
                new_state = (new_x, new_y, direction)
                heapq.heappush(heap, (new_f, new_cost, new_x, new_y, direction))
                predecessors[new_state].append(state)

        # 2. Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        new_cost = cost + 1000
        heuristic_val = manhattan_distance(x, y, end_x, end_y)
        new_f = new_cost + heuristic_val
        new_state = (x, y, new_dir)
        heapq.heappush(heap, (new_f, new_cost, x, y, new_dir))
        predecessors[new_state].append(state)

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        new_cost = cost + 1000
        heuristic_val = manhattan_distance(x, y, end_x, end_y)
        new_f = new_cost + heuristic_val
        new_state = (x, y, new_dir)
        heapq.heappush(heap, (new_f, new_cost, x, y, new_dir))
        predecessors[new_state].append(state)

    # Find the minimal cost among all end states
    min_cost = float('inf')
    end_states = [state for state in visited if (state[0], state[1]) == end_pos]
    for state in end_states:
        if visited[state] < min_cost:
            min_cost = visited[state]

    # Collect all end states with minimal cost
    optimal_end_states = [state for state in end_states if visited[state] == min_cost]

    return min_cost, predecessors, optimal_end_states

def collect_tiles_on_best_paths(predecessors, optimal_end_states, start_pos):
    """
    Collects all unique tiles that are part of any optimal path.
    
    Args:
        predecessors (dict): Mapping from state to list of predecessor states.
        optimal_end_states (list): List of end states with minimal cost.
        start_pos (tuple): (x, y) coordinates of the Start tile.
    
    Returns:
        set: Set of (x, y) tuples representing tiles on best paths.
    """
    tiles = set()
    stack = []

    for end_state in optimal_end_states:
        stack.append(end_state)

    while stack:
        current_state = stack.pop()
        x, y, direction = current_state
        tiles.add((x, y))
        preds = predecessors.get(current_state, [])
        for pred in preds:
            stack.append(pred)

    return tiles

def print_grid_with_tiles(grid, tiles):
    """
    Prints the grid, marking tiles that are part of any best path.
    
    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        tiles (set): Set of (x, y) tuples representing tiles on best paths.
    """
    for y, row in enumerate(grid):
        display_row = []
        for x, cell in enumerate(row):
            if (x, y) in tiles:
                if cell == '.' or cell == 'S' or cell == 'E':
                    display_row.append('O')  # Mark as part of a best path
                else:
                    display_row.append(cell)
            else:
                display_row.append(cell)
        print(''.join(display_row))

def calculate_gps_sum(grid):
    """
    Calculates the sum of GPS coordinates of all boxes.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    gps_sum = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'O':
                #gps = 100 * y + x
                #gps_sum += gps
                gps_sum += 1
    return gps_sum

def main():
    """
    Main function to execute the solution.
    """
    # Define the input file path
    # Adjust the path as necessary
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
    for row in grid:
        print(''.join(row))
    print("\nStarting A* Algorithm with Predecessors Tracking...\n")

    # Perform A* algorithm with predecessors tracking
    lowest_score, predecessors, optimal_end_states = a_star_with_predecessors(grid, start_pos, end_pos)

    if lowest_score != float('inf'):
        print(f"\nLowest score to reach the End Tile: {lowest_score}")
    else:
        print("\nEnd Tile is unreachable from the Start Tile.")
        return

    # Collect all tiles on best paths
    tiles_on_best_paths = collect_tiles_on_best_paths(predecessors, optimal_end_states, start_pos)
    print(f"\nNumber of tiles on at least one best path: {len(tiles_on_best_paths)}\n")

    # Optionally, visualize the grid with best path tiles marked
    print("Warehouse State with Best Path Tiles Marked (O):")
    print_grid_with_tiles(grid, tiles_on_best_paths)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum(grid)
    print(f"\nSum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main()
