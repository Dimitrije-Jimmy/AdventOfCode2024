import re
import os

def read_robots(file_path):
    """
    Reads the input file and parses each robot's configuration.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list of dict: Each dict contains robot's initial position and velocity.
    """
    robots = []
    pattern = r'p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)'

    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(pattern, line.strip())
            if match:
                x, y, vx, vy = map(int, match.groups())
                robots.append({'x': x, 'y': y, 'vx': vx, 'vy': vy})
            else:
                print("Warning: Failed to parse line:", line.strip())
    return robots

def simulate_movements(robots, width, height, seconds):
    """
    Simulates the movement of robots over a given number of seconds.

    Args:
        robots (list of dict): List of robots with positions and velocities.
        width (int): Width of the grid.
        height (int): Height of the grid.
        seconds (int): Number of seconds to simulate.

    Returns:
        list of dict: Updated list of robots with final positions.
    """
    for second in range(seconds):
        for robot in robots:
            # Update positions with wrapping
            robot['x'] = (robot['x'] + robot['vx']) % width
            robot['y'] = (robot['y'] + robot['vy']) % height
    return robots

def get_bounding_box(robots):
    """
    Calculates the bounding box of all robots' positions.

    Args:
        robots (list of dict): List of robots with positions.

    Returns:
        tuple: (min_x, max_x, min_y, max_y)
    """
    xs = [robot['x'] for robot in robots]
    ys = [robot['y'] for robot in robots]
    return min(xs), max(xs), min(ys), max(ys)

def calculate_area(bounding_box):
    """
    Calculates the area of the bounding box.

    Args:
        bounding_box (tuple): (min_x, max_x, min_y, max_y)

    Returns:
        int: Area of the bounding box.
    """
    min_x, max_x, min_y, max_y = bounding_box
    return (max_x - min_x) * (max_y - min_y)

def find_minimal_spread_time(robots, width, height, max_seconds=20000):
    """
    Finds the time when robots are most clustered (minimal bounding box area).

    Args:
        robots (list of dict): List of robots with initial positions and velocities.
        width (int): Width of the grid.
        height (int): Height of the grid.
        max_seconds (int, optional): Maximum seconds to simulate. Defaults to 20000.

    Returns:
        tuple: (time, robots_at_min_time)
    """
    min_area = float('inf')
    min_time = 0
    robots_at_min_time = []
    consecutive_increases = 0
    threshold = 100  # Number of consecutive increases to stop

    for second in range(max_seconds):
        # Simulate one second
        simulate_movements(robots, width, height, 1)
        
        # Calculate current bounding box area
        bounding_box = get_bounding_box(robots)
        area = calculate_area(bounding_box)

        # Check if current area is the smallest so far
        if area < min_area:
            min_area = area
            min_time = second + 1  # +1 because we simulated this second
            # Deep copy robots' positions
            robots_at_min_time = [{'x': robot['x'], 'y': robot['y']} for robot in robots]
            consecutive_increases = 0  # Reset counter
        else:
            consecutive_increases += 1
            if consecutive_increases >= threshold:
                # Assume that the minimal spread has been passed
                break

    return min_time, robots_at_min_time

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

    return Q1, Q2, Q3, Q4

def calculate_safety_factor(Q1, Q2, Q3, Q4):
    """
    Calculates the safety factor by multiplying quadrant counts.

    Args:
        Q1 (int): Count of robots in Quadrant I.
        Q2 (int): Count of robots in Quadrant II.
        Q3 (int): Count of robots in Quadrant III.
        Q4 (int): Count of robots in Quadrant IV.

    Returns:
        int: The safety factor.
    """
    return Q1 * Q2 * Q3 * Q4

def visualize_robots(robots, width, height):
    """
    Prints the grid with robots' positions.

    Args:
        robots (list of dict): List of robots with positions.
        width (int): Width of the grid.
        height (int): Height of the grid.
    """
    # Create an empty grid
    grid = [['.' for _ in range(width)] for _ in range(height)]
    
    # Place robots on the grid
    for robot in robots:
        x, y = robot['x'], robot['y']
        if grid[y][x] == '.':
            grid[y][x] = '1'
        else:
            grid[y][x] = str(int(grid[y][x]) + 1)
    
    # Print the grid
    for row in grid:
        print(''.join(row))

def main():
    """
    Main function to execute the solution.
    """
    directory = os.path.dirname(__file__) + '\\'
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    # file_path = os.path.join(directory, 'input2.txt')

    # Read robots from input file
    robots = read_robots(file_path)
    print(f"Total robots parsed: {len(robots)}")
    for idx, robot in enumerate(robots, start=1):
        print(f"Robot {idx}: x={robot['x']}, y={robot['y']} | vx={robot['vx']}, vy={robot['vy']}")

    # Define grid size
    width, height = 101, 103  # As per problem statement
    # For testing with smaller grid, uncomment below:
    # width, height = 11, 7
    # seconds = 5

    # Find the time when robots are most clustered
    min_time, robots_at_min_time = find_minimal_spread_time(robots, width, height, max_seconds=20000)
    print(f"\nMinimal spread occurs at {min_time} seconds.")
    print(f"Robot positions at {min_time} seconds:")

    for idx, robot in enumerate(robots_at_min_time, start=1):
        print(f"Robot {idx}: x={robot['x']}, y={robot['y']}")

    # Optionally, visualize the robot positions
    print("\nRobot positions grid at minimal spread time:")
    visualize_robots(robots_at_min_time, width, height)

    # Categorize robots into quadrants
    Q1, Q2, Q3, Q4 = categorize_quadrants(robots_at_min_time, width, height)
    print(f"\nQuadrant I: {Q1} robots")
    print(f"Quadrant II: {Q2} robots")
    print(f"Quadrant III: {Q3} robots")
    print(f"Quadrant IV: {Q4} robots")

    # Compute safety factor
    safety_factor = calculate_safety_factor(Q1, Q2, Q3, Q4)
    print(f"\nSafety Factor: {safety_factor}")

if __name__ == "__main__":
    main()
