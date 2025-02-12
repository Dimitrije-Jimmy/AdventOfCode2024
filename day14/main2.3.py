import re
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

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

    # Initialize scatter plot with empty data
    scatter = ax.scatter([], [], s=10, c='blue')

    # Optional: Draw grid lines for better visualization
    ax.set_xticks(range(0, width + 1, max(1, width // 10)))
    ax.set_yticks(range(0, height + 1, max(1, height // 10)))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    def init():
        # Initialize with empty offsets as a 2D array
        scatter.set_offsets(np.empty((0, 2)))
        return scatter,

    def update(frame):
        positions = positions_over_time[frame]
        if positions:
            # Convert list of tuples to a 2D NumPy array
            scatter.set_offsets(np.array(positions))
        else:
            # If no positions, set to empty 2D array
            scatter.set_offsets(np.empty((0, 2)))
        ax.set_title(f'Robot Positions at {frame} Seconds')
        return scatter,

    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(positions_over_time),
                         init_func=init, blit=True, repeat=False)

    # Save the animation
    anim.save(output_file, writer='ffmpeg', fps=1)
    print(f"Animation saved as {output_file}")

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
    seconds = 500  # As per Part Two

    # Simulate robot movements
    print("\nSimulating robot movements...")
    positions_over_time = simulate_movements(robots, width, height, seconds)
    print(f"Simulation completed for {seconds} seconds.")

    # Create and save the animation
    print("\nCreating animation...")
    output_file = 'robots_animation.mp4'  # You can change the filename and format if desired
    visualize_animation(positions_over_time, width, height, output_file=output_file)

if __name__ == "__main__":
    main()
