import sys
import os
directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'  # Adjust filename as needed
file_path = directory+'input2.txt'  # Adjust filename as needed

# Read the map from stdin
#grid = [list(line.rstrip('\n')) for line in sys.stdin if line.strip() != '']
with open(file_path, 'r') as f:
    grid = [list(line.rstrip('\n')) for line in f if line.strip() != '']

# Dimensions of the map
rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0

# Find the guard's initial position and direction
directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

reverse_dir_map = {  # To restore direction symbol if needed
    (-1,0): '^',
    (1,0): 'v',
    (0,-1): '<',
    (0,1): '>'
}

guard_row = guard_col = None
drow = dcol = None

for r in range(rows):
    for c in range(cols):
        if grid[r][c] in directions:
            guard_row, guard_col = r, c
            drow, dcol = directions[grid[r][c]]
            # Replace the guard symbol with '.' to simplify processing
            grid[r][c] = '.'
            break
    if guard_row is not None:
        break

if guard_row is None:
    print("No guard found in the input!")
    sys.exit(1)

# Function to turn right
def turn_right(drow, dcol):
    # up (-1,0) -> right (0,1)
    # right (0,1) -> down (1,0)
    # down (1,0) -> left (0,-1)
    # left (0,-1) -> up (-1,0)
    if (drow, dcol) == (-1, 0):
        return (0, 1)
    elif (drow, dcol) == (0, 1):
        return (1, 0)
    elif (drow, dcol) == (1, 0):
        return (0, -1)
    elif (drow, dcol) == (0, -1):
        return (-1, 0)
    else:
        # Should not happen
        return (drow, dcol)

visited_positions = set()
visited_positions.add((guard_row, guard_col))

visited_states = set()
visited_states.add((guard_row, guard_col, drow, dcol))

while True:
    # Check the cell in front
    front_row = guard_row + drow
    front_col = guard_col + dcol
    
    # Check if leaving the map
    if front_row < 0 or front_row >= rows or front_col < 0 or front_col >= cols:
        # Guard is about to leave the map
        # Count how many distinct positions visited
        print(len(visited_positions))
        break
    
    # Check if obstacle ahead
    if grid[front_row][front_col] == '#':
        # Turn right
        drow, dcol = turn_right(drow, dcol)
    else:
        # Move forward
        guard_row, guard_col = front_row, front_col
        visited_positions.add((guard_row, guard_col))
        
    # Check for loops
    state = (guard_row, guard_col, drow, dcol)
    if state in visited_states:
        # We have returned to a previous state -> infinite loop detected
        print("Loop detected. The guard never leaves the map.")
        # Decide how to handle this scenario; just break or print visited count.
        # For this puzzle, we might just break or print how many visited so far.
        break
    else:
        visited_states.add(state)
