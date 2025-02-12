import os
import numpy as np

def read_map(file_path):
    with open(file_path, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]
    return grid

def find_position(grid):
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
                #break
                return guard_row, guard_col, drow, dcol
        if guard_row is not None:
            return guard_row, guard_col, drow, dcol
    return guard_row, guard_col, drow, dcol

def turn_right(drow, dcol):
    if (drow, dcol) == (-1, 0): return (0, 1)   # up -> right
    elif (drow, dcol) == (0, 1): return (1, 0)  # right -> down
    elif (drow, dcol) == (1, 0): return (0, -1) # down -> left
    elif (drow, dcol) == (0, -1): return (-1, 0)# left -> up
    return (drow, dcol) # fallback

def simulate(grid, guard_row, guard_col, drow, dcol):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
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
        #if (0 > front_r >= rows) or (0 > front_c >= cols):
        if front_r < 0 or front_r >= rows or front_c < 0 or front_c >= cols:
            # Guard leaves the map
            print("Guard leaves the map", len(set(visited_states)))
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
            print("Loop detected. The guard never leaves the map.", len(visited_states))
            return "loop"
        visited_states.add(state)

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    #file_path = directory+'input.txt'

    grid = read_map(file_path)
    grid = np.array(grid)
    start_pos = find_position(grid)
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if start_pos is None:
        print("Starting position '^' not found in the map.")
        return
    guard_row, guard_col, drow, dcol = start_pos

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
        
        result = simulate(grid, guard_row, guard_col, drow, dcol)
        if result == "loop":
            count += 1
        
        # Restore cell
        grid[r][c] = original

    print(count)
    
if __name__ == "__main__":
    main()