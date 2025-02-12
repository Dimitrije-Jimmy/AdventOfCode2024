import os

# Define the input file and read its contents
input_file = 'input.txt'
#input_file = 'input2.txt'
directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(directory, input_file)

with open(file_path, 'r') as f:
    file_content = f.read()

# Split the input by a blank line into two parts: the grid and the instructions
grid_text, instructions_text = file_content.strip().split('\n\n')
grid_lines = grid_text.split('\n')
instruction_lines = instructions_text.split('\n')

# Combine all instructions lines into a single string with no spaces
instructions = ''.join(line.strip() for line in instruction_lines)

# Directions dictionary maps characters to (row_delta, column_delta)
directions_dict = {
    '<': (0, -1),
    '>': (0, 1),
    '^': (-1, 0),
    'v': (1, 0)
}

# PART 1:
# The initial map uses the characters:
# '#' for walls
# '.' for empty
# 'O' for boxes
# '@' for the robot

# Store the warehouse map in a dictionary 'map_part1' keyed by (row, column)
map_part1 = {}
robot_start_position = None

for row_index, line in enumerate(grid_lines):
    for col_index, char in enumerate(line):
        map_part1[(row_index, col_index)] = char
        if char == '@':
            robot_start_position = (row_index, col_index)

def draw_map_part1(warehouse_map):
    """
    Draw the map (part 1) based on the 'warehouse_map' dictionary.
    """
    max_row = max(pos[0] for pos in warehouse_map.keys())
    max_col = max(pos[1] for pos in warehouse_map.keys())
    drawing = []
    for r in range(max_row + 1):
        row_str = ''
        for c in range(max_col + 1):
            row_str += warehouse_map.get((r,c), ' ')
        drawing.append(row_str)
    print("\n".join(drawing))
    print()

print("Initial Part 1 Map:")
draw_map_part1(map_part1)

def move_robot_part1(current_position, direction_delta, warehouse_map):
    """
    Attempt to move the robot and push boxes in Part 1.
    The logic:
    - Start from the robot's current position.
    - Follow the direction until you either hit a wall or find empty space.
    - Boxes ('O') line up and push forward if empty space is found.
    - Robot ends up in the first position of the chain.

    Returns the new robot position after the move.
    """
    (current_r, current_c) = current_position
    (dr, dc) = direction_delta

    # We'll store positions in 'queue' to represent the chain of movement
    movement_queue = [current_position]
    box_count = 0

    # Traverse along the direction, collecting boxes until we hit an empty space or wall
    for (r, c) in movement_queue:
        if warehouse_map.get((r, c), '#') == '#':
            # If we hit a wall, break - no movement possible
            break
        next_r = r + dr
        next_c = c + dc
        next_tile = warehouse_map.get((next_r, next_c), '#')

        if next_tile == 'O':
            # It's a box, add to queue and increment box count
            box_count += 1
            movement_queue.append((next_r, next_c))
        elif next_tile == '.':
            # Empty space found - movement can happen
            movement_queue.append((next_r, next_c))
            break
        else:
            # If it's not '.' or 'O', probably a wall or outside map, stop.
            break

    # movement_queue now has the chain of positions: [robot, boxes..., final empty]
    # We'll rewrite these positions in reverse order:
    # - The last position in the queue is empty and will become '@' (robot)
    # - The preceding 'box_count' positions will become 'O'
    # - Everything else behind them becomes '.'

    still_placing_robot = True
    for pos in reversed(movement_queue):
        if box_count > 0:
            # Place a box 'O' here
            warehouse_map[pos] = 'O'
            box_count -= 1
        elif box_count == 0 and still_placing_robot:
            # Place the robot '@' here
            warehouse_map[pos] = '@'
            new_robot_pos = pos
            still_placing_robot = False
        else:
            # Place empty '.'
            warehouse_map[pos] = '.'

    return new_robot_pos

# Execute all instructions for part 1
robot_position = robot_start_position
for instruction in instructions:
    robot_position = move_robot_part1(robot_position, directions_dict[instruction], map_part1)

# After all moves, calculate the sum of GPS coordinates for boxes in part 1
part1_sum = 0
for (r, c) in map_part1:
    if map_part1[(r,c)] == 'O':
        gps = 100 * r + c
        part1_sum += gps

print("Final Part 1 Map:")
draw_map_part1(map_part1)
print("Part 1 GPS Sum:", part1_sum)

# PART 2:
# Now we scale the map horizontally.
# '#'=> '##'
# 'O'=> '[]'
# '.'=> '..'
# '@'=> '@.' (robot tile)
map_part2 = {}
robot_start_part2 = None

for r, line in enumerate(grid_lines):
    for c, v in enumerate(line):
        if v == '#':
            map_part2[(r, 2*c)] = '#'
            map_part2[(r, 2*c+1)] = '#'
        elif v == 'O':
            map_part2[(r, 2*c)] = '['
            map_part2[(r, 2*c+1)] = ']'
        elif v == '.':
            map_part2[(r, 2*c)] = '.'
            map_part2[(r, 2*c+1)] = '.'
        elif v == '@':
            robot_start_part2 = (r, 2*c)
            map_part2[(r, 2*c)] = '@'
            map_part2[(r, 2*c+1)] = '.'

def draw_map_part2(warehouse_map):
    """
    Draw the scaled warehouse map (part 2).
    """
    max_row = max(pos[0] for pos in warehouse_map.keys())
    max_col = max(pos[1] for pos in warehouse_map.keys())
    drawing = []
    for rr in range(max_row + 1):
        line_str = ''
        for cc in range(max_col + 1):
            line_str += warehouse_map.get((rr,cc), ' ')
        drawing.append(line_str)
    print("\n".join(drawing))
    print()

print("Initial Part 2 Map:")
draw_map_part2(map_part2)

def move_left_right(part2_pos, direction_delta, warehouse_map):
    """
    Move the robot horizontally in part 2 scenario.
    This tries to push boxes represented by '[]' horizontally.
    """
    (r, c) = part2_pos
    (dr, dc) = direction_delta
    movement_queue = [part2_pos]
    box_count = 0

    # Collect boxes until we find an empty space '.' or fail
    for (cur_r, cur_c) in movement_queue:
        if warehouse_map.get((cur_r, cur_c), '#') == '#':
            break
        next_r = cur_r + dr
        next_c = cur_c + dc
        next_tile = warehouse_map.get((next_r, next_c), '#')
        if next_tile in '[]':
            # It's part of a box
            box_count += 1
            movement_queue.append((next_r, next_c))
        elif next_tile == '.':
            # Found empty space, can stop collecting
            movement_queue.append((next_r, next_c))
            break
        else:
            # Can't move here
            return part2_pos

    # Similar logic: place robot at the last position, boxes before it, and '.' behind
    placing_robot = True
    for pos in reversed(movement_queue):
        (rr, cc) = pos
        if box_count > 0:
            # Move the box forward
            prev_r = rr - dr
            prev_c = cc - dc
            warehouse_map[(rr, cc)] = warehouse_map[(prev_r, prev_c)]
            box_count -= 1
        elif box_count == 0 and placing_robot:
            warehouse_map[(rr, cc)] = '@'
            result_pos = (rr, cc)
            placing_robot = False
        else:
            warehouse_map[(rr, cc)] = '.'
    return result_pos

def move_up_down(part2_pos, direction_delta, warehouse_map):
    """
    Move the robot vertically in part 2 scenario.
    Push boxes vertically as a block.

    The logic uses a BFS to collect all boxes connected to the line of movement.
    Then it shifts them one step up or down if possible.
    """
    (dr, dc) = direction_delta
    queue = [part2_pos]
    new_positions_dict = {}
    # Collect vertical block
    for (r, c) in queue:
        if warehouse_map.get((r, c), '#') == '#':
            return part2_pos
        nr, nc = r + dr, c + dc
        new_positions_dict[(nr, nc)] = warehouse_map.get((r, c), '.')
        next_tile = warehouse_map.get((nr, nc), '.')
        if next_tile == '#':
            return part2_pos
        if next_tile in '[]':
            queue.append((nr, nc))
            # If it's '[' or ']', also consider the adjacent character to form a full box tile
            if next_tile == '[':
                queue.append((nr, nc+1))
            else: # next_tile == ']'
                queue.append((nr, nc-1))

    # Clear old positions
    for pos in queue:
        warehouse_map[pos] = '.'

    # Place the collected tiles in new positions
    for pos in new_positions_dict:
        warehouse_map[pos] = new_positions_dict[pos]

    (r, c) = part2_pos
    return (r+dr, c+dc)

# Execute all instructions for part 2
part2_robot_position = robot_start_part2
for instruction in instructions:
    if instruction in '<>':
        part2_robot_position = move_left_right(part2_robot_position, directions_dict[instruction], map_part2)
    else:
        part2_robot_position = move_up_down(part2_robot_position, directions_dict[instruction], map_part2)

# After all moves in part 2, calculate the sum of GPS for boxes.
part2_sum = 0
for (r, c) in map_part2:
    if map_part2[(r,c)] == '[':
        # '[' is the left part of the box
        gps = 100 * r + c
        part2_sum += gps

print("Final Part 2 Map:")
draw_map_part2(map_part2)
print("Part 2 GPS Sum:", part2_sum)

# Results from the original code:
# # 1414416 for Part 1
# # 1386070 for Part 2
# This code maintains the same logic as the original, just more verbose.
