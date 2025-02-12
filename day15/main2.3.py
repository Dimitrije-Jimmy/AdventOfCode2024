import os
import sys
from typing import List, Tuple, Set

def read_input(file_path: str) -> Tuple[List[str], List[str]]:
    """
    Reads the input file and separates the warehouse map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (map_lines, move_lines)
            - map_lines (list of str): Original warehouse map lines.
            - move_lines (list of str): Movement sequence lines.
    """
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

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

    return map_lines, move_lines

def scale_map_part2(map_lines: List[str]) -> List[str]:
    """
    Scales up the map for Part Two by doubling the width and applying the specified transformations.

    Args:
        map_lines (list of str): Original map lines.

    Returns:
        list of str: Scaled-up map lines.
    """
    scaled_map = []
    for line in map_lines:
        scaled_line = ''
        i = 0
        while i < len(line):
            char = line[i]
            if char == '#':
                scaled_line += '##'
            elif char == 'O':
                scaled_line += '[]'
            elif char == '.':
                scaled_line += '..'
            elif char == '@':
                scaled_line += '@.'
            else:
                # Retain any unexpected characters by doubling them
                scaled_line += char * 2
            i += 1
        scaled_map.append(scaled_line)
    return scaled_map

def parse_scaled_map(scaled_map: List[str]) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Parses the scaled map to identify walls, boxes, and the robot's position.

    Args:
        scaled_map (list of str): Scaled-up warehouse map lines.

    Returns:
        tuple: (walls, boxes, robot_pos)
            - walls (set of tuples): Coordinates of walls.
            - boxes (set of tuples): Coordinates of boxes (left x-coordinate of '[]').
            - robot_pos (tuple): (x, y) coordinates of the robot.
    """
    walls = set()
    boxes = set()
    robot_pos = (0, 0)

    for y, line in enumerate(scaled_map):
        x = 0
        while x < len(line):
            pair = line[x:x+2]
            if pair == '##':
                walls.add((x, y))
                x += 2
            elif pair == '[]':
                boxes.add((x, y))
                x += 2
            elif pair.startswith('@'):
                # Robot is represented as '@.' after scaling
                robot_pos = (x, y)
                x += 2
            elif pair == '..':
                # Empty space
                x += 2
            else:
                # Handle any unexpected pair by treating each character separately
                char = line[x]
                if char == '#':
                    walls.add((x, y))
                elif char == '[':
                    # Assume it's part of a box and check the next character
                    if x+1 < len(line) and line[x+1] == ']':
                        boxes.add((x, y))
                        x += 2
                        continue
                elif char == '@':
                    robot_pos = (x, y)
                x += 1

    return walls, boxes, robot_pos

def visualize_grid(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], box_width: int = 2) -> None:
    """
    Prints the grid with the robot's current position.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes.
        robot_pos (tuple): (x, y) coordinates of the robot.
        box_width (int): Width of the box. Default is 2 for Part Two.
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
            if pos == robot_pos:
                row.append('@')
                x += 1
                continue
            elif pos in walls:
                row.append('#')
                x += 1
                continue
            elif pos in boxes:
                if box_width == 2:
                    # Ensure we don't go out of bounds
                    if x + 1 <= max_x and (x + 1, y) in boxes:
                        row.append('[]')
                        x += 2
                        continue
                    else:
                        row.append('[')  # Incomplete box representation
                        x += 1
                        continue
                else:
                    row.append('O')
                    x += 1
                    continue
            else:
                if box_width == 2:
                    row.append('.')
                    x += 1
                else:
                    row.append('.')
                    x += 1
        grid_rows.append(''.join(row))

    print('\n'.join(grid_rows))
    print()  # Add an empty line for better readability

def simulate_moves_part2(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], moves: List[str]) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes for Part Two, allowing multiple boxes to be pushed in a single move.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes (left x-coordinate of '[]').
        robot_pos (tuple): (x, y) coordinates of the robot.
        moves (list of str): List of movement directions.

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
            # Attempt to push one or more boxes in the direction
            boxes_to_push = []
            current_pos = target_pos

            while current_pos in boxes:
                boxes_to_push.append(current_pos)
                current_pos = (current_pos[0] + dx, current_pos[1] + dy)

            # Check if the space after the last box is free
            # Since boxes are two-wide, ensure that after pushing, both positions are free
            # Determine the new positions for all boxes
            can_push = True
            new_box_positions = []
            for box in boxes_to_push:
                new_box_x = box[0] + dx
                new_box_y = box[1] + dy
                new_box_pos = (new_box_x, new_box_y)
                # For Part Two, boxes are two-wide. Ensure that the right part is also free.
                right_part_new = (new_box_x + 1, new_box_y)
                if new_box_pos in walls or new_box_pos in boxes or right_part_new in walls or right_part_new in boxes:
                    can_push = False
                    print(f"Move {move_num}: Cannot push box from {box} to {new_box_pos}. Blocked by wall or another box.")
                    break
                new_box_positions.append(new_box_pos)

            if not can_push:
                print(f"Move {move_num}: '{move}' move failed due to obstruction.")
                continue

            # Perform the push: move all boxes one step in the direction
            for original_box, new_box in zip(boxes_to_push, new_box_positions):
                boxes.remove(original_box)
                boxes.add(new_box)
                print(f"Move {move_num}: Pushed box from {original_box} to {new_box}.")

            # Move the robot to the first box's original position
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

        else:
            # Move the robot into empty space
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

    return boxes, robot_pos

def calculate_gps_sum_part2(boxes: Set[Tuple[int, int]]) -> int:
    """
    Calculates the sum of GPS coordinates of all boxes for Part Two.

    Args:
        boxes (set of tuples): Coordinates of boxes (left x-coordinate of '[]').

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    gps_sum = 0
    for (x, y) in boxes:
        # GPS is based on the distance from the top and left edges to the closest edge of the box
        # Since boxes are two-wide, we consider the leftmost x as the distance from the left
        # Distance from the top is y
        gps = 100 * y + x
        gps_sum += gps
    return gps_sum

def main():
    """
    Main function to execute Part Two of the solution.
    """
    #if len(sys.argv) != 2:
    #    print("Usage: python warehouse_part2.py input_file")
    #    return

    #input_file = sys.argv[1]
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')

    #if not os.path.isfile(file_path):
    #    print(f"Input file '{input_file}' not found in the directory '{directory}'.")
    #    return

    # Read and separate the input
    original_map, move_lines = read_input(file_path)

    # Scale the map for Part Two
    scaled_map = scale_map_part2(original_map)
    print("Scaled-Up Map for Part Two:")
    for line in scaled_map:
        print(line)
    print()

    # Parse the scaled map
    walls, boxes, robot_pos = parse_scaled_map(scaled_map)

    # Concatenate all move lines into a single list of moves
    moves = ''.join(move_lines).replace('\n', '').replace(' ', '')
    moves = list(moves)

    print(f"Total moves: {len(moves)}\n")
    print(f"Initial robot position: {robot_pos}\n")

    # Visualize the initial scaled grid
    print("Scaled Initial Warehouse State:")
    visualize_grid(walls, boxes, robot_pos, box_width=2)

    # Simulate the robot's movements for Part Two
    updated_boxes, updated_robot_pos = simulate_moves_part2(walls, boxes, robot_pos, moves)

    # Visualize the final scaled grid
    print("\nFinal Scaled Warehouse State:")
    visualize_grid(walls, updated_boxes, updated_robot_pos, box_width=2)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum_part2(updated_boxes)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main()
