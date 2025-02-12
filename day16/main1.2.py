import os
import heapq

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
        grid (list of list of str): 2D grid representing the warehouse.
    """
    for row in grid:
        print(''.join(row))

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
                heapq.heappush(heap, (new_cost + heuristic, new_cost, new_x, new_y, direction))

        # 2. Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        new_cost = cost + 1000
        heuristic = manhattan_distance(x, y, end_x, end_y)
        heapq.heappush(heap, (new_cost + heuristic, new_cost, x, y, new_dir))

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        new_cost = cost + 1000
        heuristic = manhattan_distance(x, y, end_x, end_y)
        heapq.heappush(heap, (new_cost + heuristic, new_cost, x, y, new_dir))

    # If End is unreachable
    return -1

def main():
    """
    Main function to execute the solution.
    """
    # Define the input file path
    # Adjust the path as necessary
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')

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

    # Perform Dijkstra's algorithm to find the lowest score
    lowest_score = a_star(grid, start_pos, end_pos)

    if lowest_score != -1:
        print(f"\nLowest score to reach the End Tile: {lowest_score}")
    else:
        print("\nEnd Tile is unreachable from the Start Tile.")

if __name__ == "__main__":
    main()