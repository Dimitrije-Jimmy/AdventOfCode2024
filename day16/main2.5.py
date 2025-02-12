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

def dijkstra_with_predecessors(grid, start_pos, end_pos):
    """
    Performs Dijkstra's algorithm to find all optimal paths from Start to End,
    tracking predecessors to identify all tiles on any best path.

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
    heap = []
    initial_dir = 'E'  # Reindeer starts facing East
    start_x, start_y = start_pos
    heapq.heappush(heap, (0, start_x, start_y, initial_dir))

    cost_so_far = {}
    predecessors = defaultdict(list)

    while heap:
        cost, x, y, direction = heapq.heappop(heap)
        state = (x, y, direction)

        # If we've already found a better path to this state, skip it
        if state in cost_so_far and cost > cost_so_far[state]:
            continue

        # If this is the first time visiting this state or found a better path
        if state not in cost_so_far or cost < cost_so_far[state]:
            cost_so_far[state] = cost
            # Reset predecessors since we've found a better path
            predecessors[state] = []

        # If reached the end, continue to find all optimal paths
        if (x, y) == end_pos:
            continue  # Do not terminate; ensure all optimal paths are found

        # Explore possible actions

        # 1. Move Forward
        dx, dy = DIR_VECTORS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            target_cell = grid[new_y][new_x]
            if target_cell != '#':  # Can move forward
                new_cost = cost + 1
                new_state = (new_x, new_y, direction)
                if new_state not in cost_so_far or new_cost < cost_so_far.get(new_state, float('inf')):
                    heapq.heappush(heap, (new_cost, new_x, new_y, direction))
                    predecessors[new_state].append(state)
                elif new_cost == cost_so_far.get(new_state, float('inf')):
                    heapq.heappush(heap, (new_cost, new_x, new_y, direction))
                    predecessors[new_state].append(state)

        # 2. Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        new_cost = cost + 1000
        new_state = (x, y, new_dir)
        if new_state not in cost_so_far or new_cost < cost_so_far.get(new_state, float('inf')):
            heapq.heappush(heap, (new_cost, x, y, new_dir))
            predecessors[new_state].append(state)
        elif new_cost == cost_so_far.get(new_state, float('inf')):
            heapq.heappush(heap, (new_cost, x, y, new_dir))
            predecessors[new_state].append(state)

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        new_cost = cost + 1000
        new_state = (x, y, new_dir)
        if new_state not in cost_so_far or new_cost < cost_so_far.get(new_state, float('inf')):
            heapq.heappush(heap, (new_cost, x, y, new_dir))
            predecessors[new_state].append(state)
        elif new_cost == cost_so_far.get(new_state, float('inf')):
            heapq.heappush(heap, (new_cost, x, y, new_dir))
            predecessors[new_state].append(state)

    # Find the minimal cost among all end states
    min_cost = float('inf')
    end_states = [state for state in cost_so_far if (state[0], state[1]) == end_pos]
    for state in end_states:
        if cost_so_far[state] < min_cost:
            min_cost = cost_so_far[state]

    # Collect all end states with minimal cost
    optimal_end_states = [state for state in end_states if cost_so_far[state] == min_cost]

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
    visited_states = set()  # To prevent processing the same state multiple times

    # Initialize the stack with all optimal end states
    for end_state in optimal_end_states:
        stack.append(end_state)

    while stack:
        current_state = stack.pop()

        # Skip processing if the state has already been visited
        if current_state in visited_states:
            continue
        visited_states.add(current_state)

        x, y, direction = current_state
        tiles.add((x, y))  # Add the tile's position to the set

        # Retrieve all predecessor states for the current state
        preds = predecessors.get(current_state, [])
        for pred in preds:
            stack.append(pred)  # Add predecessor states to the stack for processing

    return tiles

def read_input(file_path):
    """
    Reads the input file and parses the warehouse map.

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

def mark_tiles_on_grid(grid, tiles):
    """
    Marks the tiles on the grid that are part of any optimal path.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        tiles (set): Set of (x, y) tuples representing tiles on best paths.

    Returns:
        list of list of str: Updated grid with 'O' marking the tiles on best paths.
    """
    marked_grid = [row.copy() for row in grid]  # Create a copy to avoid modifying the original grid
    for (x, y) in tiles:
        if marked_grid[y][x] == '.' or marked_grid[y][x] == 'S' or marked_grid[y][x] == 'E':
            marked_grid[y][x] = 'O'
    return marked_grid

def print_marked_grid(marked_grid):
    for row in marked_grid:
        print(''.join(row))

def main():
    """
    Main function to execute the solution.
    """
    # Define the input file path
    # Assumes 'input.txt' is in the same directory as this script
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    file_path = os.path.join(directory, 'input2.txt')
    file_path = os.path.join(directory, 'input2.txt')

    # Read and parse the input
    try:
        grid, start_pos, end_pos = read_input(file_path)
    except ValueError as e:
        print(e)
        return

    print(f"Start Position: {start_pos}")
    print(f"End Position: {end_pos}\n")

    # Perform Dijkstra's algorithm with predecessor tracking
    lowest_score, predecessors, optimal_end_states = dijkstra_with_predecessors(grid, start_pos, end_pos)

    if lowest_score != float('inf'):
        print(f"Lowest score to reach the End Tile: {lowest_score}")
    else:
        print("End Tile is unreachable from the Start Tile.")
        return

    # Collect all tiles on best paths
    tiles_on_best_paths = collect_tiles_on_best_paths(predecessors, optimal_end_states, start_pos)
    print(f"Number of tiles on at least one best path: {len(tiles_on_best_paths)}\n")

    # Optional: Visualize the grid with best path tiles marked
    marked_grid = mark_tiles_on_grid(grid, tiles_on_best_paths)
    print("Warehouse State with Best Path Tiles Marked (O):")
    print_marked_grid(marked_grid)

if __name__ == "__main__":
    main()
