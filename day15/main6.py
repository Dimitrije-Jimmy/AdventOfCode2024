import os
import sys
from collections import deque
from typing import List, Tuple

def read_input(file_path: str) -> Tuple[List[str], str]:
    """
    Reads the input file and returns the map lines and the moves as strings.
    For part two, we will transform the map after reading.
    """
    with open(file_path, 'r') as f:
        lines = f.read().split('\n')

    map_lines = []
    moves_lines = []
    is_map = True
    for line in lines:
        if line.strip() == '':
            is_map = False
            continue
        if is_map:
            map_lines.append(line)
        else:
            moves_lines.append(line)

    moves = ''.join(moves_lines).replace('\n', '').replace(' ', '')
    return map_lines, moves

def scale_map_for_part2(map_lines: List[str]) -> List[str]:
    """
    Scale the map horizontally according to the rules:
    '#' -> '##'
    'O' -> '[]'
    '.' -> '..'
    '@' -> '@.'
    """
    transformed_lines = []
    for line in map_lines:
        new_line = []
        for ch in line:
            if ch == '#':
                new_line.append('##')
            elif ch == 'O':
                new_line.append('[]')
            elif ch == '.':
                new_line.append('..')
            elif ch == '@':
                new_line.append('@.')
            else:
                # If there's any unexpected char, treat as '.'
                new_line.append('..')
        transformed_lines.append(''.join(new_line))
    return transformed_lines

def find_robot_position(grid: List[str]) -> Tuple[int, int]:
    """
    Find the robot '@' in the scaled grid.
    Returns (x, y) coordinates.
    """
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '@':
                return (x, y)
    raise ValueError("Robot '@' not found in the grid")

def get_dimensions(grid: List[str]) -> Tuple[int, int]:
    return len(grid[0]), len(grid)

def in_bounds(x: int, y: int, width: int, height: int) -> bool:
    return 0 <= x < width and 0 <= y < height

def is_wall(ch: str) -> bool:
    return ch == '#'

def is_box(ch: str) -> bool:
    return ch in ['[', ']']

def is_empty(ch: str) -> bool:
    return ch == '.'

def simulate_moves(grid: List[str], moves: str) -> List[str]:
    """
    Simulate the robot moves on the scaled map.
    grid is a list of strings, each row is a string.
    We'll convert it into a mutable structure for convenience.
    """
    # Convert grid to a list of list of chars for mutability
    grid = [list(row) for row in grid]
    height = len(grid)
    width = len(grid[0])

    # Directions
    direction_map = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0)
    }

    # Find robot initial position
    rx, ry = find_robot_position([''.join(r) for r in grid])

    for move_num, move in enumerate(moves, start=1):
        if move not in direction_map:
            continue
        dx, dy = direction_map[move]
        nx, ny = rx + dx, ry + dy

        if not in_bounds(nx, ny, width, height):
            # Out of bounds - can't move
            continue

        target_ch = grid[ny][nx]

        if is_wall(target_ch):
            # Move blocked by wall
            continue

        if is_empty(target_ch):
            # Just move
            # Move robot '@' and also move the '.' after '@.' if needed
            # Actually, robot occupies '@' only. The '.' after it is just part of scaling.
            # Set old robot position to '.' and new to '@'
            grid[ry][rx] = '.'  # old robot cell now empty
            grid[ny][nx] = '@'
            rx, ry = nx, ny
        elif is_box(target_ch):
            # Need to push boxes
            # First, find all connected box cells that form the cluster to move.
            # We'll BFS from (nx, ny) including all connected box cells.
            box_cells = collect_box_cluster(grid, nx, ny)

            # Check if we can move all these box cells one step (dx, dy)
            if can_move_cluster(grid, box_cells, dx, dy):
                # Move cluster
                move_cluster(grid, box_cells, dx, dy)
                # Move robot into new position
                grid[ry][rx] = '.'  # old robot
                grid[ny][nx] = '@'
                rx, ry = nx, ny
            else:
                # Can't move this turn
                continue

    # Convert grid back to list of strings
    grid = [''.join(row) for row in grid]
    return grid

def collect_box_cluster(grid: List[List[str]], sx: int, sy: int) -> List[Tuple[int,int]]:
    """
    Collect all connected box cells starting from (sx, sy).
    Connectivity is orthogonal. A box cluster might form complex shapes.
    Return a list of coordinates (x, y) of all box cells in the cluster.
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    queue = deque()
    queue.append((sx, sy))
    visited.add((sx, sy))

    # Orthogonal directions
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if in_bounds(nx, ny, width, height):
                if (nx, ny) not in visited:
                    if is_box(grid[ny][nx]):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
    return list(visited)

def can_move_cluster(grid: List[List[str]], cluster: List[Tuple[int,int]], dx: int, dy: int) -> bool:
    """
    Check if we can move the entire cluster by (dx, dy).
    Conditions:
    - All target cells must be in bounds.
    - None of the target cells can be walls (#).
    - None of the target cells can be occupied by boxes not in the cluster.
    """
    height = len(grid)
    width = len(grid[0])
    cluster_set = set(cluster)
    for (x, y) in cluster:
        nx, ny = x+dx, y+dy
        if not in_bounds(nx, ny, width, height):
            return False
        ch = grid[ny][nx]
        if is_wall(ch):
            return False
        # If it's a box cell not in our cluster, can't move
        if is_box(ch) and (nx, ny) not in cluster_set:
            return False
        # Empty or '@' or '.' is fine
    return True

def move_cluster(grid: List[List[str]], cluster: List[Tuple[int,int]], dx: int, dy: int):
    """
    Move all cells in cluster by (dx, dy).
    Must do this carefully to avoid overwriting.
    We'll move them from bottom-right to top-left or something stable.
    Actually, we can first clear all cluster cells, then fill them in new positions.
    """
    # Clear old positions
    for (x,y) in cluster:
        grid[y][x] = '.'  # now empty

    # Place boxes in new positions
    for (x,y) in cluster:
        nx, ny = x+dx, y+dy
        # We don't know which char was box cell '[' or ']'.
        # We must preserve the box shape. So we must remember what they were originally.
        # Wait, we lost that info by clearing to '.' first.
        # We must store original chars before clearing.
        # Let's fix that by adjusting the approach:
        pass

def move_cluster(grid: List[List[str]], cluster: List[Tuple[int,int]], dx: int, dy: int):
    """
    Improved approach:
    We'll remember the old chars, then clear, then place them shifted.
    """
    # Remember old chars
    old_cells = {}
    for (x,y) in cluster:
        old_cells[(x,y)] = grid[y][x]

    # Clear old positions
    for (x,y) in cluster:
        grid[y][x] = '.'

    # Place in new positions
    for (x,y) in cluster:
        nx, ny = x+dx, y+dy
        grid[ny][nx] = old_cells[(x,y)]

def calculate_gps_sum(grid: List[str]) -> int:
    """
    Calculate sum of GPS coordinates of all boxes.
    For each '[]' pair, the GPS is 100*y + x of the '[' cell.
    We'll find all '[' cells and compute coordinates.
    """
    gps_sum = 0
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '[':
                # This is the left cell of a box
                # GPS = 100*y + x
                gps = 100 * y + x
                gps_sum += gps
    return gps_sum

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'input.txt'
        #input_file = 'input2.txt'

    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, input_file)

    if not os.path.isfile(file_path):
        print(f"Input file '{input_file}' not found.")
        return

    original_map, moves = read_input(file_path)
    # Scale map
    scaled_map = scale_map_for_part2(original_map)

    # Simulate moves on the scaled map
    final_grid = simulate_moves(scaled_map, moves)

    # Calculate GPS sum
    gps_sum = calculate_gps_sum(final_grid)
    print(gps_sum)

if __name__ == "__main__":
    main()
