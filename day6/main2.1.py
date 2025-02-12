import sys
import os
directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'  # Adjust filename as needed
#file_path = directory+'input2.txt'  # Adjust filename as needed

# Read the map from stdin
#grid = [list(line.rstrip('\n')) for line in sys.stdin if line.strip() != '']
with open(file_path, 'r') as f:
    grid = [list(line.rstrip('\n')) for line in f if line.strip() != '']

rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0

directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

guard_row = guard_col = None
drow = dcol = None
for r in range(rows):
    for c in range(cols):
        if grid[r][c] in directions:
            guard_row, guard_col = r, c
            drow, dcol = directions[grid[r][c]]
            # Replace guard symbol with '.'
            grid[r][c] = '.'
            break
    if guard_row is not None:
        break

def turn_right(drow, dcol):
    if (drow, dcol) == (-1, 0): return (0, 1)   # up -> right
    elif (drow, dcol) == (0, 1): return (1, 0)  # right -> down
    elif (drow, dcol) == (1, 0): return (0, -1) # down -> left
    elif (drow, dcol) == (0, -1): return (-1, 0)# left -> up
    return (drow, dcol) # fallback

def simulate(grid):
    # Restore initial conditions for each run
    start_r, start_c = guard_row, guard_col
    start_drow, start_dcol = drow, dcol
    
    visited_states = set()
    gr, gc = start_r, start_c
    dr, dc = start_drow, start_dcol
    
    visited_states.add((gr, gc, dr, dc))
    
    while True:
        front_r, front_c = gr + dr, gc + dc
        
        # Check if leaving map
        if front_r < 0 or front_r >= rows or front_c < 0 or front_c >= cols:
            # Guard leaves the map
            return "leaves"
        
        # Check obstacle
        if grid[front_r][front_c] == '#':
            # Turn right
            dr, dc = turn_right(dr, dc)
        else:
            # Move forward
            gr, gc = front_r, front_c
            
        # Check loop
        state = (gr, gc, dr, dc)
        if state in visited_states:
            # Loop detected
            return "loop"
        visited_states.add(state)

# Identify candidate positions for new obstruction
candidates = []
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '.' and not (r == guard_row and c == guard_col):
            candidates.append((r,c))

count = 0
for (r,c) in candidates:
    # Place obstruction
    original = grid[r][c]
    grid[r][c] = '#'
    
    result = simulate(grid)
    if result == "loop":
        count += 1
    
    # Restore cell
    grid[r][c] = original

print(count)
