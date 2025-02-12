import os
import sys
from typing import List, Tuple, Set

def read_input(file_path: str) -> Tuple[List[List[str]], str]:
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

def find_robot(grid: List[List[str]]) -> Tuple[int, int]:
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

def visualize_grid(grid: List[List[str]], robot_pos: Tuple[int, int]) -> None:
    """
    Prints the grid with the robot's current position.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        robot_pos (tuple): (x, y) coordinates of the robot.
    """
    visual_grid = [row.copy() for row in grid]
    x, y = robot_pos
    if visual_grid[y][x] == 'O':
        visual_grid[y][x] = '@'  # Represent robot on top of a box
    else:
        visual_grid[y][x] = '@'
    
    print("\n".join([''.join(row) for row in visual_grid]))
    print()  # Add an empty line for better readability

direction_map = {
    '^': (0, -1),  # Up
    'v': (0, 1),   # Down
    '<': (-1, 0),  # Left
    '>': (1, 0)    # Right
}

def simulate_moves(grid: List[List[str]], moves: str, robot_pos: Tuple[int, int]) -> Tuple[List[List[str]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        moves (str): String of movement directions.
        robot_pos (tuple): (x, y) coordinates of the robot.

    Returns:
        tuple: (updated_grid, updated_robot_pos)
            - updated_grid (list of list of str): Grid after all moves.
            - updated_robot_pos (tuple): Robot's final position.
    """
    x, y = robot_pos

    for move_num, move in enumerate(moves, start=1):
        if move not in direction_map:
            print(f"Move {move_num}: Invalid move '{move}'. Skipping.")
            continue

        dx, dy = direction_map[move]
        target_x, target_y = x + dx, y + dy

        # Check if target position is within grid bounds
        if not (0 <= target_x < len(grid[0]) and 0 <= target_y < len(grid)):
            print(f"Move {move_num}: '{move}' would move robot out of bounds. Skipping.")
            continue

        target_cell = grid[target_y][target_x]

        if target_cell == '.':
            # Move robot
            x, y = target_x, target_y
            print(f"Move {move_num}: Robot moved {move} to ({x}, {y}).")
        elif target_cell == 'O':
            # Attempt to push the box
            box_target_x, box_target_y = target_x + dx, target_y + dy

            # Check if box's target position is within grid bounds
            if not (0 <= box_target_x < len(grid[0]) and 0 <= box_target_y < len(grid)):
                print(f"Move {move_num}: '{move}' would push box out of bounds. Move failed.")
                continue

            box_target_cell = grid[box_target_y][box_target_x]

            if box_target_cell == '.':
                # Push the box
                grid[box_target_y][box_target_x] = 'O'
                grid[target_y][target_x] = '.'  # Previous box position becomes empty
                x, y = target_x, target_y
                print(f"Move {move_num}: Robot pushed box {move} to ({box_target_x}, {box_target_y}) and moved to ({x}, {y}).")
            else:
                # Cannot push the box; move fails
                print(f"Move {move_num}: '{move}' blocked by '{box_target_cell}'. Move failed.")
                continue
        elif target_cell == '#':
            # Wall; cannot move
            print(f"Move {move_num}: '{move}' blocked by wall '#'. Move failed.")
            continue
        else:
            # Unexpected cell content; treat as blocked
            print(f"Move {move_num}: '{move}' blocked by unknown cell '{target_cell}'. Move failed.")
            continue

    return grid, (x, y)

def calculate_gps_sum(grid: List[List[str]]) -> int:
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
    # If a file name is provided as a command-line argument, use it; otherwise, default to 'input.txt'
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input.txt'  # Default input file name

    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')
    file_path = os.path.join(directory, 'input3.txt')

    if not os.path.isfile(file_path):
        print(f"Input file '{input_file}' not found in the directory '{directory}'.")
        return

    # Read and parse the input
    grid, moves = read_input(file_path)
    print(f"Total moves: {len(moves)}\n")

    # Find the robot's initial position
    try:
        robot_pos = find_robot(grid)
        print(f"Initial robot position: {robot_pos}\n")
    except ValueError as e:
        print(e)
        return

    # Visualize the initial grid
    print("Initial Warehouse State:")
    visualize_grid(grid, robot_pos)

    # Simulate the robot's movements
    updated_grid, updated_robot_pos = simulate_moves(grid, moves, robot_pos)

    # Visualize the final grid
    print("\nFinal Warehouse State:")
    visualize_grid(updated_grid, updated_robot_pos)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum(updated_grid)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main()
