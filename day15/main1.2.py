import re
import os

def read_input(file_path):
    """
    Reads the input file and parses the warehouse map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (grid, moves)
            - grid (list of list of str): 2D grid representing the warehouse.
            - moves (str): String of movement directions.
    """
    grid = []
    moves = ''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Process map lines until an empty line is encountered
    map_lines = []
    move_lines = []
    is_map = True
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            is_map = False
            continue
        if is_map:
            map_lines.append(stripped)
        else:
            move_lines.append(stripped)

    # Build the grid
    for line in map_lines:
        grid.append(list(line))

    # Concatenate all move lines into a single string
    moves = ''.join(move_lines).replace('\n', '').replace(' ', '')

    return grid, moves

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

def simulate_moves(grid, moves, robot_pos):
    """
    Simulates the robot's movements and box pushes.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        moves (str): String of movement directions.
        robot_pos (tuple): (x, y) coordinates of the robot.

    Returns:
        list of list of str: Updated grid after all moves.
    """
    x, y = robot_pos

    for move_num, move in enumerate(moves, start=1):
        if move not in direction_map:
            print(f"Invalid move '{move}' at move number {move_num}. Skipping.")
            continue

        dx, dy = direction_map[move]
        target_x, target_y = x + dx, y + dy

        # Check if target position is within grid bounds
        if not (0 <= target_x < len(grid[0]) and 0 <= target_y < len(grid)):
            print(f"Move '{move}' at move number {move_num} would move robot out of bounds. Skipping.")
            continue

        target_cell = grid[target_y][target_x]

        if target_cell == '.':
            # Move robot
            grid[y][x] = '.'  # Previous position becomes empty
            grid[target_y][target_x] = '@'
            x, y = target_x, target_y
            print(f"Move {move_num}: Robot moved {move} to ({x}, {y}).")
        elif target_cell == 'O':
            # Attempt to push the box
            box_target_x, box_target_y = target_x + dx, target_y + dy

            # Check if box's target position is within grid bounds
            if not (0 <= box_target_x < len(grid[0]) and 0 <= box_target_y < len(grid)):
                print(f"Move '{move}' at move number {move_num} would push box out of bounds. Move failed.")
                continue

            box_target_cell = grid[box_target_y][box_target_x]

            if box_target_cell == '.':
                # Push the box
                grid[box_target_y][box_target_x] = 'O'
                grid[target_y][target_x] = '@'
                grid[y][x] = '.'  # Previous robot position becomes empty
                x, y = target_x, target_y
                print(f"Move {move_num}: Robot pushed box {move} to ({box_target_x}, {box_target_y}) and moved to ({x}, {y}).")
            else:
                # Cannot push the box; move fails
                print(f"Move '{move}' at move number {move_num} blocked by '{box_target_cell}'. Move failed.")
                continue
        elif target_cell == '#':
            # Wall; cannot move
            print(f"Move '{move}' at move number {move_num} blocked by wall '#'. Move failed.")
            continue
        else:
            # Unexpected cell content; treat as blocked
            print(f"Move '{move}' at move number {move_num} blocked by unknown cell '{target_cell}'. Move failed.")
            continue

    return grid

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
    # file_path = os.path.join(directory, 'input2.txt')

    # Read and parse the input
    grid, moves = read_input(file_path)
    print(f"Total moves: {len(moves)}")

    # Find the robot's initial position
    try:
        robot_pos = find_robot(grid)
        print(f"Initial robot position: {robot_pos}")
    except ValueError as e:
        print(e)
        return

    # Simulate the robot's movements
    updated_grid = simulate_moves(grid, moves, robot_pos)

    # Optionally, print the final grid
    print("\nFinal Warehouse State:")
    for row in updated_grid:
        print(''.join(row))

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum(updated_grid)
    print(f"\nSum of all boxes' GPS coordinates: {gps_sum}")
