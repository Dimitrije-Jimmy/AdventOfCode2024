import os
import sys
from typing import List, Tuple, Set

def read_input(file_path: str) -> Tuple[List[str], str]:
    """
    Reads the input file and separates the map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (map_lines, moves)
            - map_lines (List[str]): Lines representing the warehouse map.
            - moves (str): String of movement instructions.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    map_lines = []
    move_lines = []
    is_map = True
    for line in lines:
        stripped = line.rstrip('\n')
        if stripped == '':
            is_map = False
            continue
        if is_map:
            map_lines.append(stripped)
        else:
            move_lines.append(stripped)

    moves = ''.join(move_lines).replace(' ', '').replace('\n', '')
    return map_lines, moves

def scale_up_map(original_map: List[str]) -> List[str]:
    """
    Scales up the original map by replacing each character with its scaled version.

    Args:
        original_map (List[str]): Lines representing the original warehouse map.

    Returns:
        List[str]: Lines representing the scaled-up warehouse map.
    """
    scaled_map = []
    for line in original_map:
        scaled_line = ''
        for char in line:
            if char == '#':
                scaled_line += '##'
            elif char == 'O':
                scaled_line += '[]'
            elif char == '.':
                scaled_line += '..'
            elif char == '@':
                scaled_line += '@.'
            else:
                # Handle any unexpected characters by treating them as empty spaces
                scaled_line += '..'
        scaled_map.append(scaled_line)
    return scaled_map

def parse_scaled_map(map_lines: List[str]) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], Tuple[int, int], Tuple[int, int, int, int]]:
    """
    Parses the scaled map to identify walls, boxes, and the robot's position.

    Args:
        map_lines (List[str]): Scaled map lines.

    Returns:
        tuple: (walls, boxes, robot_pos, map_size)
            - walls (Set[Tuple[int, int]]): Coordinates of walls.
            - boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
            - robot_pos (Tuple[int, int]): (x, y) coordinates of the robot.
            - map_size (Tuple[int, int, int, int]): (min_x, min_y, max_x, max_y) boundaries of the map.
    """
    walls = set()
    boxes = set()
    robot_pos = (0, 0)

    for y, line in enumerate(map_lines):
        x = 0
        while x < len(line):
            pair = line[x:x+2]
            if pair == '##':
                walls.add((x, y))
                walls.add((x+1, y))
            elif pair == '[]':
                boxes.add((x, y))      # Left cell of the box
                # The right cell (x+1, y) is part of the same box and not added separately
            elif pair == '@.':
                robot_pos = (x, y)
            elif pair == '..':
                pass  # Empty space
            else:
                # Handle any unexpected pairs as empty spaces to prevent visualization issues
                pass
            x += 2  # Move to the next pair

    # Determine map boundaries for GPS calculation
    all_positions = walls.union(boxes).union({robot_pos})
    min_x = min(x for x, y in all_positions)
    max_x = max(x for x, y in all_positions)
    min_y = min(y for x, y in all_positions)
    max_y = max(y for x, y in all_positions)

    return walls, boxes, robot_pos, (min_x, min_y, max_x, max_y)

def visualize_grid_scaled(
    walls: Set[Tuple[int, int]],
    boxes: Set[Tuple[int, int]],
    robot_pos: Tuple[int, int],
    map_boundaries: Tuple[int, int, int, int]
) -> None:
    """
    Prints the grid with the robot's current position and boxes.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
        robot_pos (Tuple[int, int]): (x, y) coordinates of the robot.
        map_boundaries (Tuple[int, int, int, int]): Map boundaries.
    """
    min_x, min_y, max_x, max_y = map_boundaries

    # Initialize the grid with empty spaces
    grid = [['..' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]

    # Mark walls
    for (x, y) in walls:
        grid[y - min_y][x - min_x] = '##'

    # Mark boxes (only left cells)
    for (x, y) in boxes:
        grid[y - min_y][x - min_x] = '[]'

    # Mark robot
    rx, ry = robot_pos
    if (rx, ry) in walls or (rx, ry) in boxes:
        print(f"Warning: Robot position {robot_pos} overlaps with another element.")
    grid[ry - min_y][rx - min_x] = '@.'

    # Build and print the grid
    for y in range(min_y, max_y + 1):
        row_str = ''
        for x in range(min_x, max_x + 1):
            cell = grid[y - min_y][x - min_x]
            row_str += cell
        print(row_str)
    print()

def simulate_moves_scaled(
    walls: Set[Tuple[int, int]],
    boxes: Set[Tuple[int, int]],
    robot_pos: Tuple[int, int],
    moves: str
) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes in the scaled-up warehouse.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
        robot_pos (Tuple[int, int]]): (x, y) coordinates of the robot.
        moves (str): String of movement directions.

    Returns:
        tuple: (updated_boxes, updated_robot_pos)
    """
    direction_map = {
        '^': (0, -1),  # Up
        'v': (0, 1),   # Down
        '<': (-1, 0),  # Left
        '>': (1, 0)    # Right
    }

    for move_num, move in enumerate(moves, start=1):
        if move not in direction_map:
            print(f"Move {move_num}: Invalid move '{move}'. Skipping.")
            continue

        dx, dy = direction_map[move]
        target_x = robot_pos[0] + dx
        target_y = robot_pos[1] + dy
        target_pos = (target_x, target_y)

        if target_pos in walls:
            print(f"Move {move_num}: '{move}' blocked by wall at {target_pos}. Move failed.")
            continue

        # Check if the target position has a box (only left cells)
        if target_pos in boxes:
            # Calculate the new position for the box
            new_box_x = target_x + dx
            new_box_y = target_y + dy
            new_box_pos = (new_box_x, new_box_y)

            # Check if the new position is blocked
            if new_box_pos in walls or new_box_pos in boxes:
                print(f"Move {move_num}: Cannot push box at {target_pos} to {new_box_pos}. Move failed.")
                continue

            # Push the box
            boxes.remove(target_pos)
            boxes.add(new_box_pos)
            print(f"Move {move_num}: Pushed box from {target_pos} to {new_box_pos}.")

            # Move the robot to the box's original position
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

        else:
            # Move the robot into empty space
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

    return boxes, robot_pos

def calculate_gps_sum_scaled(
    boxes: Set[Tuple[int, int]],
    map_boundaries: Tuple[int, int, int, int]
) -> int:
    """
    Calculates the sum of GPS coordinates of all boxes.

    Args:
        boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
        map_boundaries (Tuple[int, int, int, int]): Map boundaries.

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    min_x, min_y, max_x, max_y = map_boundaries
    gps_sum = 0
    for (x, y) in boxes:
        distance_top = y - min_y
        distance_left = x - min_x
        gps = 100 * distance_top + distance_left
        gps_sum += gps
    return gps_sum

def main_part_two():
    """
    Main function to execute part two of the solution.
    """
    # Define the input file path
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input4.txt'  # Default input file name

    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, input_file)

    if not os.path.isfile(file_path):
        print(f"Input file '{input_file}' not found in the directory '{directory}'.")
        return

    # Read and parse the original input
    original_map_lines, moves = read_input(file_path)
    print("Original Warehouse Map:")
    for line in original_map_lines:
        print(line)
    print()

    # Scale up the map
    scaled_map_lines = scale_up_map(original_map_lines)
    print("Scaled-Up Warehouse Map:")
    for line in scaled_map_lines:
        print(line)
    print()

    # Parse the scaled-up map
    walls, boxes, robot_pos, map_boundaries = parse_scaled_map(scaled_map_lines)
    print(f"Initial robot position: {robot_pos}\n")

    # Visualize the initial scaled-up grid
    print("Initial Scaled-Up Warehouse State:")
    visualize_grid_scaled(walls, boxes, robot_pos, map_boundaries)

    # Simulate the robot's movements
    updated_boxes, updated_robot_pos = simulate_moves_scaled(walls, boxes, robot_pos, moves)

    # Visualize the final scaled-up grid
    print("\nFinal Scaled-Up Warehouse State:")
    visualize_grid_scaled(walls, updated_boxes, updated_robot_pos, map_boundaries)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum_scaled(updated_boxes, map_boundaries)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main_part_two()
