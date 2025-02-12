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
        content = f.read()

    grid, instructions = content.strip().split('\n\n')
    map_lines = grid.split('\n')
    move_lines = instructions.split('\n')
    moves = ''.join(move_lines).replace(' ', '').replace('\n', '')
    return map_lines, moves

def parse_map(map_lines: List[str]) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Parses the original map to identify walls and the robot's starting position.

    Args:
        map_lines (List[str]): Lines representing the warehouse map.

    Returns:
        tuple: (walls, start)
            - walls (Set[Tuple[int, int]]): Coordinates of walls.
            - start (Tuple[int, int]): (row, column) coordinates of the robot.
    """
    walls = set()
    start = (0, 0)
    for r, line in enumerate(map_lines):
        for c, v in enumerate(line):
            if v == '#':
                walls.add((r, c))
            elif v == '@':
                start = (r, c)
    return walls, start

def scale_up_map(original_map: List[str]) -> List[str]:
    """
    Scales up the original map by doubling its width and adjusting characters.

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
                # Treat unexpected characters as empty spaces
                scaled_line += '..'
        scaled_map.append(scaled_line)
    return scaled_map

def parse_scaled_map(map_lines: List[str]) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], Tuple[int, int], Tuple[int, int, int, int]]:
    """
    Parses the scaled map to identify walls, boxes, and the robot's position.

    Args:
        map_lines (List[str]): Scaled map lines.

    Returns:
        tuple: (walls, boxes, robot_pos, map_boundaries)
            - walls (Set[Tuple[int, int]]): Coordinates of walls.
            - boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
            - robot_pos (Tuple[int, int]): (row, column) coordinates of the robot.
            - map_boundaries (Tuple[int, int, int, int]): (min_r, min_c, max_r, max_c) boundaries of the map.
    """
    walls = set()
    boxes = set()
    robot_pos = (0, 0)

    for r, line in enumerate(map_lines):
        for c in range(0, len(line), 2):
            pair = line[c:c+2]
            if pair == '##':
                walls.add((r, c))
                walls.add((r, c+1))
            elif pair == '[]':
                boxes.add((r, c))  # Only left cell
                # Do not add (r, c+1) to avoid duplication
            elif pair == '@.':
                robot_pos = (r, c)
            elif pair == '..':
                pass  # Empty space
            else:
                # Treat unexpected pairs as empty spaces
                pass

    # Determine map boundaries
    all_positions = walls.union(boxes).union({robot_pos})
    min_r = min(r for r, c in all_positions)
    max_r = max(r for r, c in all_positions)
    min_c = min(c for r, c in all_positions)
    max_c = max(c for r, c in all_positions)

    return walls, boxes, robot_pos, (min_r, min_c, max_r, max_c)

def visualize_map(
    walls: Set[Tuple[int, int]],
    boxes: Set[Tuple[int, int]],
    robot_pos: Tuple[int, int],
    map_boundaries: Tuple[int, int, int, int]
) -> None:
    """
    Prints the current state of the map with walls, boxes, and the robot.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
        robot_pos (Tuple[int, int]): (row, column) coordinates of the robot.
        map_boundaries (Tuple[int, int, int, int]): Map boundaries.
    """
    min_r, min_c, max_r, max_c = map_boundaries
    grid = [['..' for _ in range(min_c, max_c + 1)] for _ in range(min_r, max_r + 1)]

    # Mark walls
    for (r, c) in walls:
        grid[r - min_r][c - min_c] = '##'

    # Mark boxes
    for (r, c) in boxes:
        grid[r - min_r][c - min_c] = '[]'

    # Mark robot
    r, c = robot_pos
    if (r, c) in walls or (r, c) in boxes:
        print(f"Warning: Robot position {robot_pos} overlaps with another element.")
    grid[r - min_r][c - min_c] = '@.'

    # Build and print the grid
    for row in grid:
        row_str = ''.join(row)
        print(row_str)
    print()  # Empty line for readability

def simulate_part_one(
    walls: Set[Tuple[int, int]],
    start: Tuple[int, int],
    moves: str
) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes for Part One.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        start (Tuple[int, int]): (row, column) coordinates of the robot.
        moves (str): String of movement instructions.

    Returns:
        tuple: (boxes, final_robot_pos)
            - boxes (Set[Tuple[int, int]]): Coordinates of boxes after movements.
            - final_robot_pos (Tuple[int, int]): Robot's final position.
    """
    # Initialize boxes from the map
    boxes = set()
    # Assuming Part One uses 'O' for boxes
    for pos, v in kaart_part_one.items():
        if v == 'O':
            boxes.add(pos)

    dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

    def move(p, d):
        r, c = p
        dr, dc = d
        target_r, target_c = r + dr, c + dc
        target_pos = (target_r, target_c)

        if target_pos in walls:
            # Move blocked by wall
            return p

        if target_pos in boxes:
            # Attempt to push the box
            new_box_pos = (target_r + dr, target_c + dc)
            if new_box_pos in walls or new_box_pos in boxes:
                # Cannot push box due to obstacle
                return p
            else:
                # Push the box
                boxes.remove(target_pos)
                boxes.add(new_box_pos)
                # Move robot into the box's original position
                return target_pos
        else:
            # Move into empty space
            return target_pos

    robot_pos = start
    for move_dir in moves:
        if move_dir in dirs:
            robot_pos = move(robot_pos, dirs[move_dir])
        else:
            # Invalid move direction
            continue

    return boxes, robot_pos

def simulate_part_two(
    walls: Set[Tuple[int, int]],
    boxes: Set[Tuple[int, int]],
    robot_pos: Tuple[int, int],
    moves: str
) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes for Part Two.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
        robot_pos (Tuple[int, int]): (row, column) coordinates of the robot.
        moves (str): String of movement instructions.

    Returns:
        tuple: (boxes, final_robot_pos)
            - boxes (Set[Tuple[int, int]]): Coordinates of boxes after movements.
            - final_robot_pos (Tuple[int, int]): Robot's final position.
    """
    dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

    def movelr(p, d):
        r, c = p
        dr, dc = d
        target_r, target_c = r + dr, c + dc
        target_pos = (target_r, target_c)

        if target_pos in walls:
            # Move blocked by wall
            return p

        if target_pos in boxes:
            # Attempt to push the box
            new_box_r, new_box_c = target_r + dr, target_c + dc
            new_box_pos = (new_box_r, new_box_c)

            if new_box_pos in walls or new_box_pos in boxes:
                # Cannot push box due to obstacle
                return p
            else:
                # Push the box
                boxes.remove(target_pos)
                boxes.add(new_box_pos)
                # Move robot into the box's original position
                return target_pos
        else:
            # Move into empty space
            return target_pos

    def moveud(p, d):
        r, c = p
        dr, dc = d
        target_r, target_c = r + dr, c + dc
        target_pos = (target_r, target_c)

        if target_pos in walls:
            # Move blocked by wall
            return p

        if target_pos in boxes:
            # Attempt to push the box
            new_box_r, new_box_c = target_r + dr, target_c + dc
            new_box_pos = (new_box_r, new_box_c)

            if new_box_pos in walls or new_box_pos in boxes:
                # Cannot push box due to obstacle
                return p
            else:
                # Push the box
                boxes.remove(target_pos)
                boxes.add(new_box_pos)
                # Move robot into the box's original position
                return target_pos
        else:
            # Move into empty space
            return target_pos

    robot_pos = robot_pos
    for move_dir in moves:
        if move_dir not in dirs:
            continue
        if move_dir in '<>':
            robot_pos = movelr(robot_pos, dirs[move_dir])
        else:
            robot_pos = moveud(robot_pos, dirs[move_dir])

    return boxes, robot_pos

def calculate_gps_sum(boxes: Set[Tuple[int, int]]) -> int:
    """
    Calculates the sum of GPS coordinates for all boxes.

    Args:
        boxes (Set[Tuple[int, int]]): Coordinates of boxes.

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    gps_sum = 0
    for (r, c) in boxes:
        gps_sum += 100 * r + c
    return gps_sum

def calculate_gps_sum_scaled(boxes: Set[Tuple[int, int]], map_boundaries: Tuple[int, int, int, int]) -> int:
    """
    Calculates the sum of GPS coordinates for all boxes in the scaled map.

    Args:
        boxes (Set[Tuple[int, int]]): Coordinates of box left cells.
        map_boundaries (Tuple[int, int, int, int]): Map boundaries.

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    min_r, min_c, max_r, max_c = map_boundaries
    gps_sum = 0
    for (r, c) in boxes:
        distance_top = r - min_r
        distance_left = c - min_c
        gps_sum += 100 * distance_top + distance_left
    return gps_sum

def main():
    """
    Main function to execute both Part One and Part Two of the solution.
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

    # Read and parse the input
    original_map_lines, moves = read_input(file_path)

    # Part One
    print("----- Part One -----\n")
    walls_part_one, start_part_one = parse_map(original_map_lines)
    # Initialize 'kaart_part_one'
    kaart_part_one = {}
    for r, line in enumerate(original_map_lines):
        for c, v in enumerate(line):
            kaart_part_one[(r, c)] = v
            if v == '@':
                start_part_one = (r, c)

    # Simulate Part One
    boxes_part_one, final_robot_pos_part_one = simulate_part_one(walls_part_one, start_part_one, moves)

    # Calculate GPS Sum for Part One
    gps_sum_part_one = calculate_gps_sum(boxes_part_one)
    print(f"Sum of all boxes' GPS coordinates (Part One): {gps_sum_part_one}\n")

    # Part Two
    print("----- Part Two -----\n")
    # Scale up the map for Part Two
    scaled_map_lines = scale_up_map(original_map_lines)
    # Initialize 'kaart_part_two'
    walls_part_two, boxes_part_two, robot_pos_part_two, map_boundaries_part_two = parse_scaled_map(scaled_map_lines)

    # Simulate Part Two
    boxes_part_two, final_robot_pos_part_two = simulate_part_two(walls_part_two, boxes_part_two, robot_pos_part_two, moves)

    # Visualize the final state of Part Two
    print("Final Scaled-Up Warehouse State (Part Two):")
    visualize_map(walls_part_two, boxes_part_two, final_robot_pos_part_two, map_boundaries_part_two)

    # Calculate GPS Sum for Part Two
    gps_sum_part_two = calculate_gps_sum_scaled(boxes_part_two, map_boundaries_part_two)
    print(f"Sum of all boxes' GPS coordinates (Part Two): {gps_sum_part_two}")

if __name__ == "__main__":
    main()
