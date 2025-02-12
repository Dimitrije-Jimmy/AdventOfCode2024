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

def parse_map(map_lines: List[str]) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Parses the scaled map to identify walls, boxes, and the robot's position.

    Args:
        map_lines (List[str]): Scaled map lines.

    Returns:
        tuple: (walls, boxes, robot_pos)
            - walls (Set[Tuple[int, int]]): Coordinates of walls.
            - boxes (Set[Tuple[int, int]]): Coordinates of boxes (both left and right cells).
            - robot_pos (Tuple[int, int]): (x, y) coordinates of the robot.
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
                boxes.add((x+1, y))    # Right cell of the box
            elif pair == '@.':
                robot_pos = (x, y)
            elif pair == '..':
                pass  # Empty space
            else:
                # Handle any unexpected pairs as empty spaces to prevent visualization issues
                pass
            x += 2  # Move to the next pair

    return walls, boxes, robot_pos

def visualize_map(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int]) -> None:
    """
    Visualizes the warehouse map.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of boxes (both left and right cells).
        robot_pos (Tuple[int, int]): (x, y) coordinates of the robot.
    """
    if not walls and not boxes:
        print("Empty grid.")
        return

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
            if pos in walls and (x+1, y) in walls:
                row.append('##')
            elif pos in boxes and (x+1, y) in boxes:
                if pos == robot_pos:
                    row.append('@[')
                elif (x+1, y) == robot_pos:
                    row.append('@]')
                else:
                    row.append('[]')
            elif pos == robot_pos:
                row.append('@.')
            else:
                row.append('..')
            x += 2
        grid_rows.append(''.join(row))

    print('\n'.join(grid_rows))
    print()  # Add an empty line for better readability

def simulate_moves(walls: Set[Tuple[int, int]], boxes: Set[Tuple[int, int]], robot_pos: Tuple[int, int], moves: str) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    """
    Simulates the robot's movements and box pushes.

    Args:
        walls (Set[Tuple[int, int]]): Coordinates of walls.
        boxes (Set[Tuple[int, int]]): Coordinates of boxes (both left and right cells).
        robot_pos (Tuple[int, int]): (x, y) coordinates of the robot.
        moves (str): String of movement instructions.

    Returns:
        tuple: (updated_boxes, updated_robot_pos)
            - updated_boxes (Set[Tuple[int, int]]): Updated coordinates of boxes.
            - updated_robot_pos (Tuple[int, int]): Final position of the robot.
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
            # Identify all contiguous boxes in the direction of movement
            boxes_to_push = []
            current_pos = target_pos

            while current_pos in boxes:
                boxes_to_push.append(current_pos)
                current_pos = (current_pos[0] + dx, current_pos[1] + dy)

            # Determine the final position after pushing
            final_pos = current_pos

            # Check if the final position is free (not a wall or box)
            if final_pos in walls or final_pos in boxes:
                print(f"Move {move_num}: Cannot push boxes in direction '{move}'. Blocked at {final_pos}. Move failed.")
                continue

            # Push all boxes by one step in the direction
            # To handle double-wide boxes, ensure that both cells are moved
            # Sort boxes_to_push based on movement direction to prevent overlapping
            if dx > 0 or dy > 0:
                boxes_to_push_sorted = sorted(boxes_to_push, key=lambda pos: (pos[1], pos[0]), reverse=True)
            else:
                boxes_to_push_sorted = sorted(boxes_to_push, key=lambda pos: (pos[1], pos[0]))

            # Check all new positions are free
            can_push = True
            for box_pos in boxes_to_push_sorted:
                new_box_pos = (box_pos[0] + dx, box_pos[1] + dy)
                if new_box_pos in walls or new_box_pos in boxes:
                    can_push = False
                    break

            if not can_push:
                print(f"Move {move_num}: Cannot push boxes in direction '{move}'. Path blocked. Move failed.")
                continue

            # Perform the push
            for box_pos in boxes_to_push_sorted:
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

def calculate_gps_sum(boxes: Set[Tuple[int, int]]) -> int:
    """
    Calculates the sum of GPS coordinates of all boxes.

    Args:
        boxes (Set[Tuple[int, int]]): Coordinates of boxes (both left and right cells).

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

def main():
    """
    Main function to execute the solution for Part Two.
    """
    # Define the input file path
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input3.txt'  # Default input file name

    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, input_file)

    if not os.path.isfile(file_path):
        print(f"Input file '{input_file}' not found in the directory '{directory}'.")
        return

    # Read and parse the input
    map_lines, moves = read_input(file_path)
    walls, boxes, robot_pos = parse_map(map_lines)
    print(f"Total moves: {len(moves)}\n")
    print(f"Initial robot position: {robot_pos}\n")
    print("Initial Warehouse State:")
    visualize_map(walls, boxes, robot_pos)

    # Simulate the robot's movements
    updated_boxes, updated_robot_pos = simulate_moves(walls, boxes, robot_pos, moves)

    # Visualize the final warehouse state
    print("\nFinal Warehouse State:")
    visualize_map(updated_boxes, updated_boxes, updated_robot_pos)

    # Calculate the sum of GPS coordinates
    gps_sum = calculate_gps_sum(updated_boxes)
    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main()
