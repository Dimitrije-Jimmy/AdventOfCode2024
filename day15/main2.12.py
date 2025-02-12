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
            - boxes (Set[Tuple[int, int]]): Coordinates of box starting positions (left cell of each box).
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
                # The right cell (x+1, y) is part of the box, not a separate box
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

def visualize_grid_scaled(map_lines: List[str]) -> None:
    """
    Prints the scaled-up grid.

    Args:
        map_lines (List[str]): Scaled map lines.
    """
    for line in map_lines:
        print(line)
    print()  # Add an empty line for better readability

def visualize_grid_scaled_state(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], map_boundaries: Tuple[int, int, int, int]) -> None:
    """
    Prints the grid with the robot's current position and boxes.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of box starting positions.
        robot_pos (Tuple[int, int]): (x, y) coordinates of the robot.
        map_boundaries (Tuple[int, int, int, int]): Map boundaries.
    """
    min_x, min_y, max_x, max_y = map_boundaries

    grid_rows = []
    for y in range(min_y, max_y + 1):
        row = []
        x = min_x
        while x <= max_x:
            pos = (x, y)
            pair = ''
            if pos in walls:
                # Check if the next cell is also a wall for '##'
                if (x + 1, y) in walls:
                    pair = '##'
                else:
                    pair = '#.'  # Incomplete wall pair
            elif pos in boxes:
                # Boxes are represented as '[]'
                pair = '[]'
            elif pos == robot_pos:
                # Robot is represented as '@.'
                pair = '@.'
            else:
                pair = '..'  # Empty space
            row.append(pair)
            x += 2  # Move to next pair
        grid_rows.append(''.join(row))

    print('\n'.join(grid_rows))
    print()  # Add an empty line for better readability

def simulate_moves_scaled(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], moves: str) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes in the scaled-up warehouse.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of box starting positions (left cell of each box).
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

        # Check if the target position is part of a box
        box_to_push = None
        for box in boxes:
            box_cells = {box, (box[0]+1, box[1])}  # The two cells occupied by the box
            if target_pos in box_cells:
                box_to_push = box
                break

        if target_pos in walls:
            print(f"Move {move_num}: '{move}' blocked by wall at {target_pos}. Move failed.")
            continue

        elif box_to_push is not None:
            # Determine the new position for the box
            new_box_x = box_to_push[0] + dx
            new_box_y = box_to_push[1] + dy
            new_box_pos = (new_box_x, new_box_y)

            # Check if the new box position is free (both cells must be free)
            new_box_cells = {new_box_pos, (new_box_x + 1, new_box_y)}
            collision = False
            if new_box_cells & walls:
                collision = True
            else:
                for other_box in boxes:
                    if other_box != box_to_push:
                        other_box_cells = {other_box, (other_box[0]+1, other_box[1])}
                        if new_box_cells & other_box_cells:
                            collision = True
                            break

            if collision:
                print(f"Move {move_num}: Cannot push box at {box_to_push} in direction '{move}'. Blocked at {new_box_pos}. Move failed.")
                continue

            # Push the box
            boxes.remove(box_to_push)
            boxes.add(new_box_pos)
            print(f"Move {move_num}: Pushed box from {box_to_push} to {new_box_pos}.")

            # Move the robot into the box's original position
            robot_pos = box_to_push
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

        else:
            # Move the robot into empty space
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

    return boxes, robot_pos

def calculate_gps_sum_scaled(boxes: Set[Tuple[int, int]], map_boundaries: Tuple[int, int, int, int]) -> int:
    """
    Calculates the sum of GPS coordinates of all boxes.

    Args:
        boxes (Set[Tuple[int, int]]): Coordinates of box starting positions (left cell of each box).
        map_boundaries (Tuple[int, int, int, int]): (min_x, min_y, max_x, max_y) boundaries of the map.

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

def visualize_grid_scaled(map_lines: List[str]) -> None:
    """
    Prints the scaled-up grid.

    Args:
        map_lines (List[str]): Scaled map lines.
    """
    for line in map_lines:
        print(line)
    print()  # Add an empty line for better readability

def visualize_grid_scaled_state(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], map_boundaries: Tuple[int, int, int, int]) -> None:
    """
    Prints the grid with the robot's current position and boxes.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of box starting positions.
        robot_pos (Tuple[int, int]]): (x, y) coordinates of the robot.
        map_boundaries (Tuple[int, int, int, int]): Map boundaries.
    """
    min_x, min_y, max_x, max_y = map_boundaries

    grid_rows = []
    for y in range(min_y, max_y + 1):
        row = []
        x = min_x
        while x <= max_x:
            pos = (x, y)
            pair = ''
            if pos in walls:
                # Check if the next cell is also a wall for '##'
                if (x + 1, y) in walls:
                    pair = '##'
                else:
                    pair = '#.'  # Incomplete wall pair
            elif pos in boxes:
                # Boxes are represented as '[]'
                pair = '[]'
            elif pos == robot_pos:
                # Robot is represented as '@.'
                pair = '@.'
            else:
                pair = '..'  # Empty space
            row.append(pair)
            x += 2  # Move to next pair
        grid_rows.append(''.join(row))

    print('\n'.join(grid_rows))
    print()  # Add an empty line for better readability

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
    visualize_grid_scaled(scaled_map_lines)

    # Parse the scaled-up map
    walls, boxes, robot_pos, map_boundaries = parse_scaled_map(scaled_map_lines)
    print(f"Initial robot position: {robot_pos}\n")

    # Visualize the initial scaled-up grid
    print("Initial Scaled-Up Warehouse State:")
    visualize_grid_scaled_state(walls, boxes, robot_pos, map_boundaries)

    # Simulate the robot's movements
    updated_boxes, updated_robot_pos = simulate_moves_scaled(walls, boxes, robot_pos, moves)

    # Visualize the final scaled-up grid
    print("\nFinal Scaled-Up Warehouse State:")
    visualize_grid_scaled_state(walls, updated_boxes, updated_robot_pos, map_boundaries)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum_scaled(updated_boxes, map_boundaries)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main_part_two()
