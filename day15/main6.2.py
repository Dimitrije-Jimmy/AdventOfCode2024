import os
import sys
from collections import deque
from typing import List, Tuple

def read_input(file_path: str) -> Tuple[List[str], str]:
    with open(file_path, 'r') as f:
        content = f.read().strip('\n')

    parts = content.split('\n\n')
    map_lines = parts[0].split('\n')
    moves_lines = parts[1].split('\n') if len(parts) > 1 else []
    moves = ''.join(moves_lines).replace(' ', '')
    return map_lines, moves

def scale_map_for_part2(map_lines: List[str]) -> List[str]:
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
                # According to the puzzle: '@' -> '@.'
                new_line.append('@.')
            else:
                # Just in case, treat unknown as empty
                new_line.append('..')
        new_lines.append(''.join(new_line))
    return new_lines

def to_tile_grid(scaled_map: List[str]) -> List[List[str]]:
    # Each row is a string with 2*original_width chars.
    # We split each row into tiles of width 2 chars.
    tile_grid = []
    for row in scaled_map:
        width_chars = len(row)
        # Each tile is 2 chars
        tiles = [row[i:i+2] for i in range(0, width_chars, 2)]
        tile_grid.append(tiles)
    return tile_grid

def find_robot(tile_grid: List[List[str]]) -> Tuple[int,int]:
    for y, row in enumerate(tile_grid):
        for x, tile in enumerate(row):
            if tile.startswith('@'):
                return x, y
    raise ValueError("Robot not found")

def is_wall(tile: str) -> bool:
    return tile == '##'

def is_box(tile: str) -> bool:
    return tile == '[]'

def is_empty_tile(tile: str) -> bool:
    # Empty tile is '..' or the second char of '@.' after robot moves
    return tile == '..'

def simulate_moves(tile_grid: List[List[str]], moves: str) -> List[List[str]]:
    height = len(tile_grid)
    width = len(tile_grid[0])

    direction_map = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0)
    }

    rx, ry = find_robot(tile_grid)

    for move in moves:
        if move not in direction_map:
            continue
        dx, dy = direction_map[move]
        nx, ny = rx + dx, ry + dy

        # Check bounds
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            # Out of bounds, ignore move
            continue

        target_tile = tile_grid[ny][nx]

        if is_wall(target_tile):
            # blocked by wall
            continue

        if is_empty_tile(target_tile):
            # move robot
            # Clear old robot position
            tile_grid[ry][rx] = '..'
            # Place robot at new position
            tile_grid[ny][nx] = '@.'
            rx, ry = nx, ny
        elif is_box(target_tile):
            # Need to push boxes
            cluster = collect_box_cluster(tile_grid, nx, ny)
            if can_move_cluster(tile_grid, cluster, dx, dy):
                move_cluster(tile_grid, cluster, dx, dy)
                # Move robot
                tile_grid[ry][rx] = '..'
                tile_grid[ny][nx] = '@.'
                rx, ry = nx, ny
            else:
                # can't move
                continue
        else:
            # Could be '@.' or something else unexpected; treat as blocked.
            continue

    return tile_grid

def collect_box_cluster(tile_grid: List[List[str]], sx: int, sy: int) -> List[Tuple[int,int]]:
    height = len(tile_grid)
    width = len(tile_grid[0])
    visited = set()
    visited.add((sx, sy))
    queue = deque([(sx, sy)])
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited and is_box(tile_grid[ny][nx]):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return list(visited)

def can_move_cluster(tile_grid: List[List[str]], cluster: List[Tuple[int,int]], dx: int, dy: int) -> bool:
    height = len(tile_grid)
    width = len(tile_grid[0])
    cluster_set = set(cluster)

    for (x, y) in cluster:
        nx, ny = x+dx, y+dy
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            return False
        nt = tile_grid[ny][nx]
        if is_wall(nt):
            return False
        if is_box(nt) and (nx, ny) not in cluster_set:
            return False
        # '@.' also cannot be pushed into unless the robot moves first
        if nt.startswith('@') and (nx, ny) not in cluster_set:
            return False
    return True

def move_cluster(tile_grid: List[List[str]], cluster: List[Tuple[int,int]], dx: int, dy: int):
    # Save old tiles
    old_tiles = {}
    for (x,y) in cluster:
        old_tiles[(x,y)] = tile_grid[y][x]

    # Clear old positions
    for (x,y) in cluster:
        tile_grid[y][x] = '..'

    # Place in new positions
    for (x,y) in cluster:
        nx, ny = x+dx, y+dy
        tile_grid[ny][nx] = old_tiles[(x,y)]

def calculate_gps_sum(tile_grid: List[List[str]]) -> int:
    # For each box tile '[]', GPS = 100*y + x_char
    # x_char = tile_x*2 because each tile is 2 chars wide
    gps_sum = 0
    for y, row in enumerate(tile_grid):
        for tx, tile in enumerate(row):
            if tile == '[]':
                x_char = tx * 2
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
    tile_grid = simulate_moves(tile_grid, moves)
    gps_sum = calculate_gps_sum(tile_grid)
    print(gps_sum)

if __name__ == "__main__":
    main()

    # main6.py
    # 10207
    # 1419137

    # main6.2.py
    # 10828
    # 1409566