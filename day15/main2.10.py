import os
import sys
from typing import List, Tuple, Set

def scale_map(map_lines: List[str]) -> List[str]:
    """
    Scales the original map to double its width according to Part Two's rules.

    Args:
        map_lines (List[str]): Original map lines.

    Returns:
        List[str]: Scaled map lines.
    """
    scaled_map = []
    for line in map_lines:
        scaled_line = ""
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
                # Treat any unexpected characters as empty spaces
                scaled_line += '..'
        scaled_map.append(scaled_line)
    return scaled_map

def read_input_part_two(file_path: str) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], Tuple[int, int], str]:
    """
    Reads the input file, scales the map for Part Two, and parses the warehouse map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (walls, boxes, robot_pos, moves)
            - walls (set of tuples): Coordinates of walls.
            - boxes (set of tuples): Coordinates of boxes (both left and right cells).
            - robot_pos (tuple): (x, y) coordinates of the robot.
            - moves (str): String of movement directions.
    """
    walls = set()
    boxes = set()
    robot_pos = (0, 0)
    moves = ''

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Separate map lines and move lines
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

    # Scale the map for Part Two
    scaled_map = scale_map(map_lines)

    # Parse the scaled map
    for y, line in enumerate(scaled_map):
        x = 0
        while x < len(line):
            pair = line[x:x+2]
            if pair == '##':
                walls.add((x, y))
                walls.add((x+1, y))
            elif pair == '[]':
                boxes.add((x, y))      # Left cell of the box
                boxes.add((x+1, y))    # Right cell of the box
            elif pair == '@.':
                robot_pos = (x, y)
                # The robot occupies only the first cell '@', the second cell '.' is empty
            elif pair == '..':
                pass  # Empty space
            else:
                # Treat any unexpected pairs as empty spaces to prevent '??'
                pass
            x += 2  # Move to the next pair

    # Concatenate all move lines into a single string
    moves = ''.join(move_lines).replace('\n', '').replace(' ', '')

    return walls, boxes, robot_pos, moves

def visualize_grid_part_two(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int]) -> None:
    """
    Prints the grid with the robot's current position for Part Two.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes (both left and right cells).
        robot_pos (tuple): (x, y) coordinates of the robot.
    """
    if not walls and not boxes:
        print("Empty grid.")
        return

    # Determine grid boundaries
    all_positions = walls.union(boxes).union({robot_pos})
    min_x = min(x for x, y in all_positions)
    max_x = max(x for x, y in all_positions)
    min_y = min(y for x, y in all_positions)
    max_y = max(y for x, y in all_positions)

    grid_rows = []
    for y in range(min_y, max_y + 1):
        row = []
        x = min_x
        while x <= max_x:
            pos = (x, y)
            pair = (x, y, x+1, y)
            if (x, y) in walls and (x+1, y) in walls:
                row.append('##')
            elif (x, y) in boxes and (x+1, y) in boxes:
                if (x, y) == robot_pos:
                    # If robot is on the left cell of a box, display robot and box
                    row.append('@[')
                elif (x+1, y) == robot_pos:
                    # If robot is on the right cell of a box, display box and robot
                    row.append('@]')
                else:
                    row.append('[]')
            elif pos == robot_pos:
                row.append('@.')
            else:
                row.append('..')
            x += 2  # Move to the next pair
        grid_rows.append(''.join(row))

    print('\n'.join(grid_rows))
    print()  # Add an empty line for better readability

def simulate_moves_part_two(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], moves: str) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes for Part Two, handling double-wide boxes and pushing multiple boxes at once.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes (both left and right cells).
        robot_pos (tuple): (x, y) coordinates of the robot.
        moves (str): String of movement directions.

    Returns:
        tuple: (updated_boxes, updated_robot_pos)
            - updated_boxes (set of tuples): Updated coordinates of boxes.
            - updated_robot_pos (tuple): Robot's final position.
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

        elif target_pos in boxes:
            # Determine all contiguous boxes in the direction of movement
            boxes_to_push = []
            current_pos = target_pos

            while current_pos in boxes:
                boxes_to_push.append(current_pos)
                current_pos = (current_pos[0] + dx, current_pos[1] + dy)

            # Check if the final position is free (not a wall or another box)
            if current_pos in walls or current_pos in boxes:
                print(f"Move {move_num}: Cannot push boxes in direction '{move}'. Blocked at {current_pos}. Move failed.")
                continue

            # Push all boxes one step in the direction
            can_push = True
            new_boxes_positions = set()

            for box_pos in boxes_to_push:
                new_box_pos = (box_pos[0] + dx, box_pos[1] + dy)
                new_boxes_positions.add(new_box_pos)

            # Check all new positions are free (not walls or existing boxes)
            if any(pos in walls or pos in boxes for pos in new_boxes_positions):
                print(f"Move {move_num}: Cannot push boxes in direction '{move}'. Path blocked after pushing. Move failed.")
                continue

            # Perform the push
            for box_pos in boxes_to_push:
                new_box_pos = (box_pos[0] + dx, box_pos[1] + dy)
                boxes.remove(box_pos)
                boxes.add(new_box_pos)
                print(f"Move {move_num}: Pushed box from {box_pos} to {new_box_pos}.")

            # Move the robot into the first box's original position
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

        else:
            # Move the robot into empty space
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

    return boxes, robot_pos

def calculate_gps_sum_part_two(boxes: Set[Tuple[int, int]]) -> int:
    """
    Calculates the sum of GPS coordinates of all boxes for Part Two.

    Args:
        boxes (set of tuples): Coordinates of boxes (both left and right cells).

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    gps_sum = 0
    processed_boxes = set()

    for (x, y) in boxes:
        if (x, y) in processed_boxes:
            continue

        # Check if this is the left cell of a double-wide box
        if (x + 1, y) in boxes:
            gps = 100 * y + x
            gps_sum += gps
            processed_boxes.add((x, y))
            processed_boxes.add((x + 1, y))
        else:
            # Single cell box (shouldn't occur in scaled map)
            gps = 100 * y + x
            gps_sum += gps
            processed_boxes.add((x, y))

    return gps_sum

def main_part_two():
    """
    Main function to execute the solution for Part Two.
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

    # Read and parse the input for Part Two
    walls, boxes, robot_pos, moves = read_input_part_two(file_path)
    print(f"Total moves: {len(moves)}\n")

    # Initial robot position
    print(f"Initial robot position: {robot_pos}\n")

    # Visualize the initial grid
    print("Initial Warehouse State:")
    visualize_grid_part_two(walls, boxes, robot_pos)

    # Simulate the robot's movements for Part Two
    updated_boxes, updated_robot_pos = simulate_moves_part_two(walls, boxes, robot_pos, moves)

    # Visualize the final grid
    print("\nFinal Warehouse State:")
    visualize_grid_part_two(walls, updated_boxes, updated_robot_pos)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum_part_two(updated_boxes)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main_part_two()
