import re
import os

def read_positions(file_path):
    """
    Reads the input file and parses the warehouse map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (map_lines, moves)
            - map_lines (list of str): List of strings representing each row of the map.
            - moves (str): String of movement directions.
    """
    map_lines = []
    moves = ''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Process map lines until an empty line is encountered
    is_map = True
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            is_map = False
            continue
        if is_map:
            map_lines.append(stripped)
        else:
            moves += stripped.replace(' ', '').replace('\n', '')
    return map_lines, moves

def build_grid(map_lines):
    """
    Builds a 2D grid from the map lines.

    Args:
        map_lines (list of str): List of strings representing each row of the map.

    Returns:
        list of list of str: 2D grid representing the warehouse.
    """
    grid = []
    for line in map_lines:
        grid.append(list(line))
    return grid

def find_robot(grid):
    """
    Finds the robot's position in the grid.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.

    Returns:
        tuple: (x, y) coordinates of the robot.
    """
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '@':
                return (x, y)
    raise ValueError("Robot '@' not found in the grid.")

direction_map = {
    '^': (0, -1),  # Up
    'v': (0, 1),   # Down
    '<': (-1, 0),  # Left
    '>': (1, 0)    # Right
}

def make_step(grid, move, robot_pos):
    """
    Executes a single move.

    Args:
        grid (list of list of str): Current grid.
        move (str): Direction of the move ('^', 'v', '<', '>').
        robot_pos (tuple): Current position of the robot (x, y).

    Returns:
        tuple: Updated grid and robot position.
    """
    if move not in direction_map:
        print(f"Invalid move: {move}")
        return grid, robot_pos

    dx, dy = direction_map[move]
    x, y = robot_pos
    target_x, target_y = x + dx, y + dy

    # Check bounds
    if not (0 <= target_x < len(grid[0]) and 0 <= target_y < len(grid)):
        print(f"Move {move} at position ({x}, {y}) is out of bounds.")
        return grid, robot_pos

    target_cell = grid[target_y][target_x]

    if target_cell == '.':
        # Move robot
        grid[y][x] = '.'
        grid[target_y][target_x] = '@'
        robot_pos = (target_x, target_y)
        print(f"Robot moved {move} to ({target_x}, {target_y}).")
    elif target_cell == 'O':
        # Attempt to push the box
        box_target_x, box_target_y = target_x + dx, target_y + dy

        # Check bounds for the box
        if not (0 <= box_target_x < len(grid[0]) and 0 <= box_target_y < len(grid)):
            print(f"Cannot push box at ({target_x}, {target_y}) out of bounds. Move failed.")
            return grid, robot_pos

        box_target_cell = grid[box_target_y][box_target_x]

        if box_target_cell == '.':
            # Push the box
            grid[box_target_y][box_target_x] = 'O'
            grid[target_y][target_x] = '@'
            grid[y][x] = '.'  # Previous robot position becomes empty
            robot_pos = (target_x, target_y)
            print(f"Robot pushed box {move} to ({box_target_x}, {box_target_y}) and moved to ({target_x}, {target_y}).")
        else:
            # Cannot push the box
            print(f"Cannot push box at ({target_x}, {target_y}) into '{box_target_cell}'. Move failed.")
    elif target_cell == '#':
        # Wall; cannot move
        print(f"Move {move} blocked by wall at ({target_x}, {target_y}).")
    else:
        # Unexpected cell content
        print(f"Encountered unexpected cell '{target_cell}' at ({target_x}, {target_y}). Move failed.")

    return grid, robot_pos

def make_step_whole(grid, moves, robot_pos):
    """
    Executes all moves in sequence.

    Args:
        grid (list of list of str): Initial grid.
        moves (str): String of movement directions.
        robot_pos (tuple): Initial position of the robot.

    Returns:
        list of list of str: Updated grid after all moves.
    """
    for move_num, move in enumerate(moves, start=1):
        print(f"\nExecuting Move {move_num}: {move}")
        grid, robot_pos = make_step(grid, move, robot_pos)
    return grid

def categorize_quadrants(grid, width, height):
    """
    Categorizes boxes into quadrants based on their positions.

    Args:
        grid (list of list of str): Final grid.
        width (int): Width of the grid.
        height (int): Height of the grid.

    Returns:
        tuple: Counts of boxes in Quadrant I, II, III, IV.
    """
    mid_x = width // 2
    mid_y = height // 2
    Q1, Q2, Q3, Q4 = 0, 0, 0, 0

    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'O':
                if x < mid_x and y < mid_y:
                    Q1 += 1
                elif x >= mid_x and y < mid_y:
                    Q2 += 1
                elif x < mid_x and y >= mid_y:
                    Q3 += 1
                elif x >= mid_x and y >= mid_y:
                    Q4 += 1
    return Q1, Q2, Q3, Q4

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
                gps = 100 * y + x
                gps_sum += gps
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

    # Read and parse the input
    map_lines, moves = read_positions(file_path)
    print(f"Total moves: {len(moves)}")

    # Build the grid
    grid = build_grid(map_lines)

    # Find the robot's initial position
    try:
        robot_pos = find_robot(grid)
        print(f"Initial robot position: {robot_pos}")
    except ValueError as e:
        print(e)
        return

    # Simulate the robot's movements
    updated_grid = make_step_whole(grid, moves, robot_pos)

    # Print the final grid
    print("\nFinal Warehouse State:")
    for row in updated_grid:
        print(''.join(row))

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum(updated_grid)
    print(f"\nSum of all boxes' GPS coordinates: {gps_sum}")

    # Optionally, categorize quadrants
    width = len(grid[0])
    height = len(grid)
    Q1, Q2, Q3, Q4 = categorize_quadrants(updated_grid, width, height)
    print(f"\nQuadrant I: {Q1} boxes")
    print(f"Quadrant II: {Q2} boxes")
    print(f"Quadrant III: {Q3} boxes")
    print(f"Quadrant IV: {Q4} boxes")
    print(f"Total Boxes: {Q1 + Q2 + Q3 + Q4}")

if __name__ == "__main__":
    main()
