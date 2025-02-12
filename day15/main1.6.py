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
            # '.' represents empty space; no action needed

    # Concatenate all move lines into a single string
    moves = ''.join(move_lines).replace('\n', '').replace(' ', '')
    print(moves)

    return walls, boxes, robot_pos, moves

def visualize_grid(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int]) -> None:
    """
    Prints the grid with the robot's current position.

    Args:
        walls (set of tuples): Coordinates of walls.
        boxes (set of tuples): Coordinates of boxes.
        robot_pos (tuple): (x, y) coordinates of the robot.
    """
    if not walls and not boxes:
        print("Empty grid.")
        return

    # Determine grid boundaries
    min_x = min(x for x, y in walls.union(boxes).union({robot_pos}))
    max_x = max(x for x, y in walls.union(boxes).union({robot_pos}))
    min_y = min(y for x, y in walls.union(boxes).union({robot_pos}))
    max_y = max(y for x, y in walls.union(boxes).union({robot_pos}))

    grid_rows = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos in walls:
                row.append('#')
            elif pos in boxes:
                row.append('O')
            elif pos == robot_pos:
                # If robot is on a box, display both (optional)
                row.append('@')
            else:
                row.append('.')
        grid_rows.append(''.join(row))
    
    print('\n'.join(grid_rows))
    print()  # Add an empty line for better readability

def simulate_moves(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], moves: str) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes.

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
            # Attempt to push the box
            box_target_x = target_x + dx
            box_target_y = target_y + dy
            box_target_pos = (box_target_x, box_target_y)

            #if box_target_pos in walls or box_target_pos in boxes:
            if box_target_pos in walls:# or box_target_pos in boxes:
                print(f"Move {move_num}: '{move}' blocked by box or wall at {box_target_pos}. Move failed.")
                continue
            else:
                # Push the box
                boxes.remove(target_pos)
                boxes.add(box_target_pos)
                # Move the robot
                robot_pos = target_pos
                print(f"Move {move_num}: Pushed box from {target_pos} to {box_target_pos}. Robot moved to {robot_pos}.")
        else:
            # Move the robot into empty space
            robot_pos = target_pos
            print(f"Move {move_num}: Robot moved '{move}' to {robot_pos}.")

    return boxes, robot_pos

def calculate_gps_sum(boxes: Set[Tuple[int, int]]) -> int:
    """
    Calculates the sum of GPS coordinates of all boxes.

    Args:
        boxes (set of tuples): Coordinates of boxes.

    Returns:
        int: Sum of all boxes' GPS coordinates.
    """
    gps_sum = 0
    for (x, y) in boxes:
        gps = 100 * y + x
        #gps = 100 * x + y
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
    walls, boxes, robot_pos, moves = read_input(file_path)
    print(f"Total moves: {len(moves)}\n")

    # Initial robot position
    print(f"Initial robot position: {robot_pos}\n")

    # Visualize the initial grid
    print("Initial Warehouse State:")
    visualize_grid(walls, boxes, robot_pos)

    # Simulate the robot's movements
    updated_boxes, updated_robot_pos = simulate_moves(walls, boxes, robot_pos, moves)

    # Visualize the final grid
    print("\nFinal Warehouse State:")
    visualize_grid(walls, updated_boxes, updated_robot_pos)

    # Calculate the sum of GPS coordinates of all boxes
    gps_sum = calculate_gps_sum(updated_boxes)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main()
