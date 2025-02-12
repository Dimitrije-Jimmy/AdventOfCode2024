import re
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

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
        list of list of tuple: Positions of robots at each second.
    """
    # Initialize a list to store positions at each second
    positions_over_time = []

    for second in range(seconds + 1):  # Including second 0
        # Record current positions
        current_positions = [(robot['x'], robot['y']) for robot in robots]
        positions_over_time.append(current_positions)

        # Update positions for next second
        for robot in robots:
            robot['x'] = (robot['x'] + robot['vx']) % width
            robot['y'] = (robot['y'] + robot['vy']) % height

    return positions_over_time

def find_minimal_spread_time(positions_over_time):
    """
    Finds the time when robots are most clustered (minimal bounding box area).

    Args:
        positions_over_time (list of list of tuple): Robots' positions at each second.

    Returns:
        tuple: (time, positions_at_min_time)
    """
    min_area = float('inf')
    min_time = 0
    positions_at_min_time = []

    for second, positions in enumerate(positions_over_time):
        xs = [pos[0] for pos in positions]
        ys = [pos[1] for pos in positions]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        area = (max_x - min_x) * (max_y - min_y)

        if area < min_area:
            min_area = area
            min_time = second
            positions_at_min_time = positions.copy()
        else:
            # Assuming that after the area starts increasing, we've passed the minimal spread
            # To handle fluctuations, you can introduce a threshold
            pass

    return min_time, positions_at_min_time

def visualize_animation(positions_over_time, width, height, output_file='robots_animation.mp4'):
    """
    Creates and saves an animation of robots' movements over time.

    Args:
        positions_over_time (list of list of tuple): Robots' positions at each second.
        width (int): Width of the grid.
        height (int): Height of the grid.
        output_file (str, optional): Filename for the saved animation. Defaults to 'robots_animation.mp4'.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title('Robot Positions at 0 Seconds')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    scatter = ax.scatter([], [])

    # Optional: Draw grid lines for better visualization
    ax.set_xticks(range(0, width + 1, max(1, width // 10)))
    ax.set_yticks(range(0, height + 1, max(1, height // 10)))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    def init():
        scatter.set_offsets([])
        return scatter,

    def update(frame):
        positions = positions_over_time[frame]
        scatter.set_offsets(positions)
        ax.set_title(f'Robot Positions at {frame} Seconds')
        return scatter,

    anim = FuncAnimation(fig, update, frames=len(positions_over_time),
                         init_func=init, blit=True, repeat=False)

    # Save the animation
    anim.save(output_file, writer='ffmpeg', fps=30)
    print(f"Animation saved as {output_file}")

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
        if 0 <= x < width and 0 <= y < height:
            if grid[y][x] == '.':
                grid[y][x] = '1'
            else:
                try:
                    grid[y][x] = str(int(grid[y][x]) + 1)
                except ValueError:
                    grid[y][x] = '1'  # In case of unexpected character
    
    # Print the grid
    for row in grid:
        print(''.join(row))

def main():
    """
    Main function to execute the solution.
    """
    # Define the input file path
    # Adjust the path as necessary
    directory = os.path.dirname(__file__)
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
    # For testing with smaller grid and seconds, uncomment below:
    # width, height = 11, 7
    # seconds = 5
    seconds = 100  # As per Part Two

    # Simulate robot movements
    print("\nSimulating robot movements...")
    positions_over_time = simulate_movements(robots, width, height, seconds)
    print(f"Simulation completed for {seconds} seconds.")

    # Find minimal spread time (optional)
    # Uncomment the following lines if you want to identify the minimal spread time
    # min_time, positions_at_min_time = find_minimal_spread_time(positions_over_time)
    # print(f"\nMinimal spread occurs at {min_time} seconds.")
    # print("Robot positions at minimal spread time:")
    # for idx, pos in enumerate(positions_at_min_time, start=1):
    #     print(f"Robot {idx}: x={pos[0]}, y={pos[1]}")
    # visualize_robots(robots_at_min_time, width, height)

    # Create and save the animation
    print("\nCreating animation...")
    output_file = 'robots_animation.mp4'  # You can change the filename and format if desired
    visualize_animation(positions_over_time, width, height, output_file=output_file)

    # Optionally, display the final positions
    # final_positions = positions_over_time[-1]
    # print("\nFinal Robot Positions:")
    # visualize_robots([{'x': pos[0], 'y': pos[1]} for pos in final_positions], width, height)

if __name__ == "__main__":
    main()
