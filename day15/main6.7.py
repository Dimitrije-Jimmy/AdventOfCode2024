import os
import sys
from collections import deque
from typing import List, Tuple

def read_input(file_path: str) -> Tuple[List[str], str]:
    with open(file_path, 'r') as f:
        content = f.read()

    # Split by double newline
    parts = content.split('\n\n')
    map_lines = parts[0].strip('\n').split('\n')
    moves_lines = []
    if len(parts) > 1:
        moves_lines = parts[1].split('\n')
    moves = ''.join(m.strip() for m in moves_lines)
    return map_lines, moves

def scale_map_for_part2(map_lines: List[str]) -> List[str]:
    """
    Scale the map horizontally according to the rules:
    '#' -> '##'
    'O' -> '[]'
    '.' -> '..'
    '@' -> '@.'
    """
    new_lines = []
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
                # Just in case: unknown tiles as '..'
                new_line.append('..')
        new_lines.append(''.join(new_line))
    return new_lines

def to_tile_grid(scaled_map: List[str]) -> List[List[str]]:
    # Convert each row (string) into a list of 2-char tiles
    tile_grid = []
    for row in scaled_map:
        width_chars = len(row)
        tiles = [row[i:i+2] for i in range(0, width_chars, 2)]
        tile_grid.append(tiles)
    return tile_grid

def convert_robot_tile(tile_grid: List[List[str]]):
    # Convert '@.' tiles into '@' for simplicity
    height = len(tile_grid)
    width = len(tile_grid[0])
    for y in range(height):
        for x in range(width):
            if tile_grid[y][x] == '@.':
                tile_grid[y][x] = '@'

def find_robot(tile_grid: List[List[str]]) -> Tuple[int,int]:
    for y, row in enumerate(tile_grid):
        for x, tile in enumerate(row):
            if tile == '@':
                return x, y
    raise ValueError("Robot '@' not found")

def is_wall(tile: str) -> bool:
    return tile == '##'

def is_box(tile: str) -> bool:
    return tile == '[]'

def is_empty_tile(tile: str) -> bool:
    # Consider '.' and '@' as well. Actually '@' is robot, not empty.
    # But for pushing logic, we treat the robot's current position as empty after it moves.
    # We'll handle that by special logic in can_move functions.
    return tile == '..'

def in_bounds(x: int, y: int, grid: List[List[str]]) -> bool:
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

direction_map = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0)
}

def simulate_moves(tile_grid: List[List[str]], moves: str) -> List[List[str]]:
    rx, ry = find_robot(tile_grid)

    for move in moves:
        if move not in direction_map:
            continue
        dx, dy = direction_map[move]
        nx, ny = rx + dx, ry + dy
        if not in_bounds(nx, ny, tile_grid):
            # out of bounds
            continue

        target = tile_grid[ny][nx]

        if is_wall(target):
            # blocked by wall
            continue

        if is_empty_tile(target):
            # Move robot forward
            tile_grid[ry][rx] = '..'
            tile_grid[ny][nx] = '@'
            rx, ry = nx, ny
        elif is_box(target):
            # Need to push boxes
            if dx != 0 and dy == 0:
                # Horizontal push
                if push_boxes_horizontally(tile_grid, rx, ry, dx):
                    tile_grid[ry][rx] = '..'
                    tile_grid[ny][nx] = '@'
                    rx, ry = nx, ny
                else:
                    continue
            elif dy != 0 and dx == 0:
                # Vertical push
                if push_boxes_vertically(tile_grid, rx, ry, dy):
                    tile_grid[ry][rx] = '..'
                    tile_grid[ny][nx] = '@'
                    rx, ry = nx, ny
                else:
                    continue
        else:
            # If tile is '@', means robot tries to move into itself?
            # This can happen if there's some error, but just skip.
            continue
    return tile_grid

def push_boxes_horizontally(grid: List[List[str]], rx: int, ry: int, dx: int) -> bool:
    # Gather boxes in the horizontal direction from (rx+dx, ry)
    x = rx + dx
    y = ry
    box_positions = []
    while in_bounds(x, y, grid) and is_box(grid[y][x]):
        box_positions.append((x,y))
        x += dx
    # Check if we can move these boxes by one step horizontally
    if can_move_boxes(grid, box_positions, dx, 0, rx, ry):
        move_boxes(grid, box_positions, dx, 0)
        return True
    return False

def push_boxes_vertically(grid: List[List[str]], rx: int, ry: int, dy: int) -> bool:
    startx, starty = rx, ry+dy
    box_positions = collect_vertical_block(grid, startx, starty)
    if can_move_boxes(grid, box_positions, 0, dy, rx, ry):
        move_boxes(grid, box_positions, 0, dy)
        return True
    return False

def collect_vertical_block(grid: List[List[str]], sx: int, sy: int) -> List[Tuple[int,int]]:
    # Collect all connected boxes forming a block around (sx, sy)
    # BFS on boxes
    if not in_bounds(sx, sy, grid) or not is_box(grid[sy][sx]):
        return []
    visited = set()
    visited.add((sx, sy))
    q = deque([(sx, sy)])
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if in_bounds(nx, ny, grid) and (nx, ny) not in visited:
                if is_box(grid[ny][nx]):
                    visited.add((nx, ny))
                    q.append((nx, ny))
    return list(visited)

def can_move_boxes(grid: List[List[str]], box_positions: List[Tuple[int,int]], dx: int, dy: int, rx: int, ry: int) -> bool:
    # Check if we can move all these boxes by (dx, dy)
    # Treat '@' as empty since robot will vacate
    cluster = set(box_positions)
    for (x,y) in box_positions:
        nx, ny = x+dx, y+dy
        if not in_bounds(nx, ny, grid):
            return False
        tile = grid[ny][nx]
        if is_wall(tile):
            return False
        if is_box(tile) and (nx, ny) not in cluster:
            return False
        # If tile is '@', treat it as empty: allowed to push
        # If tile is '..', allowed
        # No extra checks needed
    return True

def move_boxes(grid: List[List[str]], box_positions: List[Tuple[int,int]], dx: int, dy: int):
    # Move boxes by clearing old positions first to avoid overwriting
    old_tiles = {}
    for (x,y) in box_positions:
        old_tiles[(x,y)] = grid[y][x]
        grid[y][x] = '..'

    for (x,y) in box_positions:
        nx, ny = x+dx, y+dy
        grid[ny][nx] = old_tiles[(x,y)]

def calculate_gps_sum(grid: List[List[str]]) -> int:
    gps_sum = 0
    # Check puzzle instructions if we need +1 offset. The final example says 9021 is correct for final state.
    # Let's try without +1 offset first:
    for y, row in enumerate(grid):
        for tx, tile in enumerate(row):
            if tile == '[]':
                x_char = tx * 2
                # If needed, uncomment the +1 offset:
                # x_char += 1
                gps = 100 * y + x_char
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
    scaled_map = scale_map_for_part2(original_map)
    tile_grid = to_tile_grid(scaled_map)
    # Convert '@.' to '@'
    convert_robot_tile(tile_grid)
    tile_grid = simulate_moves(tile_grid, moves)
    gps_sum = calculate_gps_sum(tile_grid)
    print(gps_sum)

if __name__ == "__main__":
    main()
