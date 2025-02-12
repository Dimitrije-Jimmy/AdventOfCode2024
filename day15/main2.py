import os
import sys
from typing import List, Tuple, Set

def read_input(file_path: str) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], Tuple[int, int], str]:
    """
    Reads the input file and parses the warehouse map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (walls, boxes, robot_pos, moves)
            - walls (set of tuples): Coordinates of walls.
            - boxes (set of tuples): Coordinates of boxes.
            - robot_pos (tuple): (x, y) coordinates of the robot.
            - moves (str): String of movement directions.
    """
    walls = set()
    boxes = set()
    robot_pos = (0, 0)
    moves = ''

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Process map lines until an empty line is encountered
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

    # Parse the map
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char == '#':
                walls.add((x, y))
            elif char == 'O':
                boxes.add((x, y))
            elif char == '@':
                robot_pos = (x, y)
            elif char == '[':
                # Assuming box is represented as '[]', so we add box at current x
                # and skip the next character
                boxes.add((x, y))
            # '.' represents empty space; no action needed

    # Concatenate all move lines into a single string
    moves = ''.join(move_lines).replace('\n', '').replace(' ', '')

    return walls, boxes, robot_pos, moves

def visualize_grid(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], box_width: int = 1) -> None:
    """
    Prints the grid with the robot's current position.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes.
        robot_pos (tuple): (x, y) coordinates of the robot.
        box_width (int): Width of the box. Default is 1 for Part One, 2 for Part Two.
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
                    # Check if next position is also a box to represent '[]'
                    next_pos = (x + 1, y)
                    if next_pos in boxes:
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

def simulate_moves_part1(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], moves: str) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes for Part One, allowing multiple boxes to be pushed in a single move.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes.
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
            # Attempt to push one or more boxes in the direction
            # Find the sequence of boxes in the movement direction
            boxes_to_push = []
            current_pos = target_pos
            while current_pos in boxes:
                boxes_to_push.append(current_pos)
                current_pos = (current_pos[0] + dx, current_pos[1] + dy)
            
            # Check if the next position after the last box is free
            if current_pos in walls or current_pos in boxes:
                print(f"Move {move_num}: '{move}' blocked by box or wall at {current_pos}. Move failed.")
                continue
            else:
                # Move all boxes one step in the direction, starting from the farthest
                for box in reversed(boxes_to_push):
                    new_box_pos = (box[0] + dx, box[1] + dy)
                    boxes.remove(box)
                    boxes.add(new_box_pos)
                    print(f"Move {move_num}: Pushed box from {box} to {new_box_pos}.")
                # Move the robot to the first box's previous position
                robot_pos = target_pos
                print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")
        else:
            # Move the robot into empty space
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

    return boxes, robot_pos

def simulate_moves_part2(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], moves: str) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes for Part Two, allowing multiple boxes to be pushed in a single move.
    Boxes are two characters wide, represented as '[]'.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes (left x-coordinate of '[]').
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

        # In Part Two, boxes occupy two horizontal positions: (x, y) and (x+1, y)
        # So, when checking for boxes, ensure that both positions are accounted for

        if target_pos in walls:
            print(f"Move {move_num}: '{move}' blocked by wall at {target_pos}. Move failed.")
            continue
        elif target_pos in boxes:
            # Attempt to push one or more boxes in the direction
            # Find the sequence of boxes in the movement direction
            boxes_to_push = []
            current_pos = target_pos
            while current_pos in boxes:
                boxes_to_push.append(current_pos)
                current_pos = (current_pos[0] + dx, current_pos[1] + dy)
            
            # In Part Two, each box occupies two horizontal positions, so we need to ensure that pushing them doesn't overlap
            # For simplicity, assume that boxes are not stacked vertically, only horizontally

            # Check if the next position after the last box is free (considering box width)
            # For direction '>', the last box's x + 1 should have space
            # For direction '<', the last box's x - 1 should have space
            # For 'v' and '^', boxes are not stacked horizontally, but since boxes are two-wide, movement still applies

            last_box = boxes_to_push[-1]
            new_last_box_pos = (last_box[0] + dx, last_box[1] + dy)

            # For horizontal movements, ensure that both parts of the box can move
            if move in ('<', '>'):
                if move == '>':
                    # Check the position after the last box's right side
                    check_pos = (last_box[0] + 2 * dx, last_box[1] + dy)
                else:
                    # move == '<'
                    # Check the position before the last box's left side
                    check_pos = (last_box[0] + dx, last_box[1] + dy)
            else:
                # For vertical movements, boxes are two-wide, so need to check both parts
                # Assume boxes do not overlap vertically
                check_pos = new_last_box_pos

            if check_pos in walls or check_pos in boxes:
                print(f"Move {move_num}: '{move}' blocked by box or wall at {check_pos}. Move failed.")
                continue
            else:
                # Move all boxes one step in the direction, starting from the farthest
                for box in reversed(boxes_to_push):
                    new_box_pos = (box[0] + dx, box[1] + dy)
                    boxes.remove(box)
                    boxes.add(new_box_pos)
                    print(f"Move {move_num}: Pushed box from {box} to {new_box_pos}.")
                # Move the robot to the first box's previous position
                robot_pos = target_pos
                print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")
        else:
            # Move the robot into empty space
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

    return boxes, robot_pos

def calculate_gps_sum_part2(boxes: Set[Tuple[int, int]], box_width: int = 2) -> int:
    """
    Calculates the sum of GPS coordinates of all boxes for Part Two.

    Args:
        boxes (set of tuples): Coordinates of boxes (left x-coordinate of '[]').
        box_width (int): Width of the box. Default is 2 for Part Two.

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    gps_sum = 0
    for (x, y) in boxes:
        # GPS is based on the closest edge of the box
        # For horizontal boxes, the left edge is x, right edge is x + 1
        # Distance from top is y
        # Distance from left is x
        # Since distance is to the closest edge, it's the minimum of left and right
        # But according to the problem, it's just distance from left edge to left of box
        # So GPS = 100 * y + x
        gps = 100 * y + x
        gps_sum += gps
    return gps_sum

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
                scaled_line += char  # Retain any unexpected characters
            i += 1
        scaled_map.append(scaled_line)
    return scaled_map

def main_part2():
    """
    Main function to execute Part Two of the solution.
    """
    # Define the input file path
    # If a file name is provided as a command-line argument, use it; otherwise, default to 'input.txt'
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input.txt'  # Default input file name

    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, input_file)

    if not os.path.isfile(file_path):
        print(f"Input file '{input_file}' not found in the directory '{directory}'.")
        return

    # Read and parse the original input
    walls, boxes, robot_pos, moves = read_input(file_path)
    
    # Read the original map lines again for scaling
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    map_lines = []
    is_map = True
    for line in lines:
        stripped = line.rstrip('\n')
        if stripped == '':
            break
        map_lines.append(stripped)
    
    # Scale the map for Part Two
    scaled_map = scale_map_part2(map_lines)
    print("Scaled-Up Map for Part Two:")
    for line in scaled_map:
        print(line)
    print()

    # Parse the scaled map
    scaled_file_path = 'scaled_input.txt'
    with open(scaled_file_path, 'w') as f:
        for line in scaled_map:
            f.write(line + '\n')
        # Append the move sequence
        f.write('\n')
        for line in lines:
            stripped = line.rstrip('\n')
            if stripped == '':
                continue
            if stripped[0] in ['<', '>', '^', 'v']:
                f.write(stripped)

    # Now, read the scaled input
    scaled_walls, scaled_boxes, scaled_robot_pos, scaled_moves = read_input(scaled_file_path)
    
    # Remove the robot's extra '.' from '@.'
    # Since the robot remains as '@', find its exact position
    # Assuming robot is represented as '@.' in the scaled map
    # Adjust robot's position accordingly
    # Find the robot's new position by checking '@' in the scaled map
    scaled_robot_pos = None
    for y, line in enumerate(scaled_map):
        x = line.find('@')
        if x != -1:
            scaled_robot_pos = (x, y)
            break
    if scaled_robot_pos is None:
        print("Robot '@' not found in the scaled map.")
        return

    # Adjust boxes: remove the '.' next to '@' if present
    # Because '@' was scaled to '@.', but we have already captured the robot's position

    # Now, visualize the scaled initial grid
    print("Scaled Initial Warehouse State:")
    visualize_grid(scaled_walls, scaled_boxes, scaled_robot_pos, box_width=2)

    # Simulate the robot's movements for Part Two
    updated_scaled_boxes, updated_scaled_robot_pos = simulate_moves_part2(scaled_walls, scaled_boxes, scaled_robot_pos, scaled_moves)

    # Visualize the final scaled grid
    print("\nFinal Scaled Warehouse State:")
    visualize_grid(scaled_walls, updated_scaled_boxes, updated_scaled_robot_pos, box_width=2)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum_scaled = calculate_gps_sum_part2(updated_scaled_boxes, box_width=2)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum_scaled}")

def main():
    """
    Main function to execute the solution.
    Determines whether to run Part One or Part Two based on command-line arguments.
    """
    # Determine the mode: Part One or Part Two
    # Usage:
    #   python warehouse_simulation.py part1 input.txt
    #   python warehouse_simulation.py part2 input.txt
    if len(sys.argv) < 3:
        print("Usage: python warehouse_simulation.py [part1|part2] input_file")
        return

    part = sys.argv[1].lower()
    input_file = sys.argv[2]

    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')

    if not os.path.isfile(file_path):
        print(f"Input file '{input_file}' not found in the directory '{directory}'.")
        return

    # Read and parse the input
    walls, boxes, robot_pos, moves = read_input(file_path)
    print(f"Total moves: {len(moves)}\n")

    # Initial robot position
    print(f"Initial robot position: {robot_pos}\n")

    if part == 'part1':
        # Visualize the initial grid for Part One
        print("Initial Warehouse State:")
        visualize_grid(walls, boxes, robot_pos)

        # Simulate the robot's movements for Part One
        updated_boxes, updated_robot_pos = simulate_moves_part1(walls, boxes, robot_pos, moves)

        # Visualize the final grid for Part One
        print("\nFinal Warehouse State:")
        visualize_grid(walls, updated_boxes, updated_robot_pos)

        # Calculate the sum of GPS coordinates of all boxes
        gps_sum = calculate_gps_sum(updated_boxes)
        print(f"Sum of all boxes' GPS coordinates: {gps_sum}")
    elif part == 'part2':
        # Part Two requires scaling the map
        # Scale the map according to the specified rules
        scaled_map = scale_map_part2([line for line in open(file_path, 'r').read().splitlines() if line.strip() != ''])
        print("Scaled-Up Map for Part Two:")
        for line in scaled_map:
            print(line)
        print()

        # Parse the scaled map
        scaled_file_path = 'scaled_input.txt'
        with open(scaled_file_path, 'w') as f:
            for line in scaled_map:
                f.write(line + '\n')
            # Append the move sequence
            f.write('\n')
            # Assuming the move sequence starts after the empty line
            move_lines = []
            is_map = True
            with open(file_path, 'r') as original_f:
                for line in original_f:
                    stripped = line.rstrip('\n')
                    if stripped == '':
                        is_map = False
                        continue
                    if not is_map:
                        move_lines.append(stripped)
            for line in move_lines:
                f.write(line)

        # Now, read the scaled input
        scaled_walls, scaled_boxes, scaled_robot_pos, scaled_moves = read_input(scaled_file_path)
        
        # Find the robot's position in the scaled map
        scaled_robot_pos = None
        for y, line in enumerate(scaled_map):
            x = line.find('@')
            if x != -1:
                scaled_robot_pos = (x, y)
                break
        if scaled_robot_pos is None:
            print("Robot '@' not found in the scaled map.")
            return

        # Now, visualize the scaled initial grid
        print("Scaled Initial Warehouse State:")
        visualize_grid(scaled_walls, scaled_boxes, scaled_robot_pos, box_width=2)

        # Simulate the robot's movements for Part Two
        updated_scaled_boxes, updated_scaled_robot_pos = simulate_moves_part2(scaled_walls, scaled_boxes, scaled_robot_pos, scaled_moves)

        # Visualize the final scaled grid
        print("\nFinal Scaled Warehouse State:")
        visualize_grid(scaled_walls, updated_scaled_boxes, updated_scaled_robot_pos, box_width=2)

        # Calculate the sum of GPS coordinates of all boxes
        gps_sum_scaled = calculate_gps_sum_part2(updated_scaled_boxes, box_width=2)
        print(f"Sum of all boxes' GPS coordinates: {gps_sum_scaled}")
    else:
        print("Invalid part specified. Use 'part1' or 'part2'.")

if __name__ == "__main__":
    main()
