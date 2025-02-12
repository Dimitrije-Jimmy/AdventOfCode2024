import re
import os
import sys
import pprint as pp

def read_machines(file_path):
    """
    Reads the input file and parses each machine's configuration.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list of dict: Each dict contains button movements and prize coordinates.
    """
    with open(file_path, 'r') as f:
        #content = f.read()
        blocks = [block.strip() for block in f.read().split('\n') if block.strip()]
    
    # Split the input into blocks separated by empty lines
    #blocks = [block.strip() for block in content.split('\n') if block.strip()]
    
    machines = []
    
    # Define regex patterns to extract numbers
    pattern = r'p\=(-?\d+),(-?\d+)\sv\=(-?\d+),(-?\d+)'

    for block in blocks:
        pattern_match = re.search(pattern, block)

        if pattern_match:
            x, y, vx, vy = int(pattern_match.group(1)), int(pattern_match.group(2)), int(pattern_match.group(3)), int(pattern_match.group(4))
            
            machines.append({
                'id': len(machines),
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy
            })
        else:
            print("Warning: Failed to parse a machine block:")
            print(block)
    
    return machines


def build_grid(width, height, machines):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for machine in machines:
        pos = grid[machine['y']][machine['x']]
        if pos != '.':
            amount = int(pos)
            grid[machine['y']][machine['x']] = str(amount + 1)
        else:
            grid[machine['y']][machine['x']] = '1'
    return grid

def make_step(grid, machines):
    new_grid = grid
    width, height = len(grid[0]), len(grid)
    for machine in machines:
        x, y = machine['x'], machine['y']
        pos_prev = grid[y][x]
        x_new = x + machine['vx']
        y_new = y + machine['vy']

        if x_new < 0:
            x_new += width
        if y_new < 0:
            y_new += height
        if x_new >= width:
            x_new -= width
        if y_new >= height:
            y_new -= height

        pos_new = grid[y_new][x_new]

        """if pos_new != '.':
            amount_new = int(pos_new)
            new_grid[y_new][x_new] = str(amount_new + 1)
        else:
            new_grid[y_new][x_new] = '1'
        
        if pos_prev != '.':
            amount_prev = int(pos_prev)
            new_grid[y][x] = str(amount_prev + 1)
        else:
            new_grid[y][x] = '.'"""
        if pos_new != '.':
            amount_new = int(pos_new)
            new_grid[y_new][x_new] = str(amount_new + 1)
        else:
            new_grid[y_new][x_new] = '1'
        
        if pos_prev != '.':
            amount_prev = int(pos_prev)
            if amount_prev > 1:
                new_grid[y][x] = str(amount_prev - 1)
            else:
                new_grid[y][x] = '.'

    return new_grid


def make_step_whole(grid, machines, seconds=100):
    new_grid = grid.copy()
    width, height = len(grid[0]), len(grid)
    for machine in machines:
        x, y = machine['x'], machine['y']
        pos_prev = grid[y][x]
        x_new = x + machine['vx']
        y_new = y + machine['vy']
        for _ in range(seconds):
            x_new += machine['vx']
            y_new += machine['vy']

            if x_new < 0:
                x_new += width
            if y_new < 0:
                y_new += height
            if x_new >= width:
                x_new -= width
            if y_new >= height:
                y_new -= height

        pos_new = grid[y_new][x_new]

        if pos_new != '.':
            amount_new = int(pos_new)
            new_grid[y_new][x_new] = str(amount_new + 1)
        else:
            new_grid[y_new][x_new] = '1'
        
        if pos_prev != '.':
            amount_prev = int(pos_prev)
            if amount_prev > 1:
                new_grid[y][x] = str(amount_prev - 1)
            else:
                new_grid[y][x] = '.'

        machine['x'] = x_new
        machine['y'] = y_new

    return new_grid

def move_machines(grid, machines, seconds):
    grid = grid
    for _ in range(seconds):
        grid = make_step(grid, machines)
    
    return grid


def total_safety_factor(grid, machines):
    safety_factor = 0
    width, height = len(grid[0]), len(grid)
    w_half, h_half = width // 2, height // 2
    #block1 = grid[:w_half][:h_half]
    #block2 = grid[w_half:][:h_half]
    #block3 = grid[:w_half][h_half:]
    #block4 = grid[w_half:][h_half:]
    b1,b2,b3,b4 = 0,0,0,0
    for machine in machines:
        y = machine['y']
        x = machine['x']
        pos = grid[y][x]
        if pos != '.':
            if (y < w_half) and (x < h_half):
                b1 += 1
            elif (y < w_half) and (x > h_half):
                b2 += 1
            elif (y > w_half) and (x < h_half):
                b3 += 1
            elif (y > w_half) and (x > h_half):
                b4 += 1

    print(b1,b2,b3,b4)
    return b1*b2*b3*b4

def categorize_quadrants(robots, width, height):
    """
    Categorizes robots into quadrants based on their positions.

    Args:
        robots (list of dict): List of robots with final positions.
        width (int): Width of the grid.
        height (int): Height of the grid.

    Returns:
        tuple: Counts of robots in Quadrant I, II, III, IV.
    """
    mid_x = width // 2
    mid_y = height // 2
    Q1, Q2, Q3, Q4 = 0, 0, 0, 0

    for robot in robots:
        x = robot['x']
        y = robot['y']

        if x < mid_x and y < mid_y:
            Q1 += 1
        elif x > mid_x and y < mid_y:
            Q2 += 1
        elif x < mid_x and y > mid_y:
            Q3 += 1
        elif x > mid_x and y > mid_y:
            Q4 += 1
        # Robots on midlines are not counted in any quadrant

    print(Q1, Q2, Q3, Q4)
    return Q1*Q2*Q3*Q4

def main():
    """
    Main function to execute the solution.
    """
    directory = os.path.dirname(__file__) + '\\'
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    #file_path = os.path.join(directory, 'input2.txt')
    
    width, height = 101, 103
    seconds = 100
    #width, height = 11, 7
    #seconds = 5
    seconds = 100

    machines = read_machines(file_path)
    print(f"Total machines parsed: {len(machines)}")
    for idx, machine in enumerate(machines, start=1):
        print(f"Machine {idx}: x={machine['x']}, y={machine['y']} | "
              f"vx={machine['vx']}, vy={machine['vy']}")
    
    # Adjust prize coordinates for Part Two
    grid = build_grid(width, height, machines)
    #pp.pprint(grid)
    print(grid)
    
    new_grid = make_step_whole(grid, machines, seconds)
    #pp.pprint(new_grid)
    print(grid)
    
    total_count = total_safety_factor(new_grid, machines)
    total_count = categorize_quadrants(machines, width, height)
    print(f"Final Total Count Required: {total_count}")
    #220375148  <-- neki ni cist prav v moji kodi z out of bounds travel
    #210587128
    
if __name__ == "__main__":
    main()