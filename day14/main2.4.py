import re
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label
import shutil

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

def simulate_movements(robots, width, height, max_seconds, save_frames=True, frames_dir='frames'):
    """
    Simulates the movement of robots over a given number of seconds.
    Optionally saves each frame as an image and detects clusters.

    Args:
        robots (list of dict): List of robots with initial positions and velocities.
        width (int): Width of the grid.
        height (int): Height of the grid.
        max_seconds (int): Number of seconds to simulate.
        save_frames (bool, optional): Whether to save frames as images. Defaults to True.
        frames_dir (str, optional): Directory to save frames. Defaults to 'frames'.

    Returns:
        None
    """
    if save_frames:
        # Create or clean the frames directory
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
        os.makedirs(frames_dir)

    for second in range(max_seconds + 1):  # Including second 0
        # Create grid
        grid = np.zeros((height, width), dtype=int)

        for robot in robots:
            x, y = robot['x'], robot['y']
            if 0 <= x < width and 0 <= y < height:
                grid[y, x] += 1  # Increment if multiple robots on the same tile

        # Visualization
        if save_frames:
            plt.figure(figsize=(8, 8))
            # Invert colors: 0 -> white, 1+ -> black
            # Use a colormap where 0 is white and any positive integer is black
            cmap = plt.cm.gray_r  # Reverse gray to have white as background
            plt.imshow(grid, cmap=cmap, interpolation='nearest')
            plt.title(f'Robot Positions at {second} Seconds')
            plt.axis('off')  # Hide axes for better visualization

            # Save frame
            frame_filename = os.path.join(frames_dir, f'frame_{second:05d}.png')
            plt.savefig(frame_filename, bbox_inches='tight', pad_inches=0)
            plt.close()

        # Detect clusters using flood fill (connected components)
        # Consider connectivity=1 for 4-connectivity or 2 for 8-connectivity
        structure = np.ones((3, 3), dtype=int)  # 8-connectivity
        labeled, ncomponents = label(grid > 0, structure=structure)

        # Find the size of the largest connected component
        if ncomponents > 0:
            component_sizes = np.bincount(labeled.ravel())
            component_sizes[0] = 0  # Ignore background
            largest_component = component_sizes.max()
        else:
            largest_component = 0

        # Check if the largest connected component exceeds 50
        if largest_component > 50:
            print(f"Potential Christmas tree detected at {second} seconds with {largest_component} connected robots.")
            # Optionally, save or highlight this frame
            # For example, copy the frame to a 'detected' directory
            detected_dir = os.path.join(frames_dir, 'detected')
            if not os.path.exists(detected_dir):
                os.makedirs(detected_dir)
            frame_filename = os.path.join(frames_dir, f'frame_{second:05d}.png')
            detected_filename = os.path.join(detected_dir, f'frame_{second:05d}.png')
            shutil.copy(frame_filename, detected_filename)
            # Optionally, stop after first detection
            # Uncomment the next line to stop at first detection
            # break

        # Update robot positions for next second
        for robot in robots:
            robot['x'] = (robot['x'] + robot['vx']) % width
            robot['y'] = (robot['y'] + robot['vy']) % height

def main():
    """
    Main function to execute the solution.
    """
    # Define the input file path
    # Adjust the path as necessary
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    # file_path = os.path.join(directory, 'input2.txt')

    # Read robots from input file
    robots = read_robots(file_path)
    print(f"Total robots parsed: {len(robots)}")
    for idx, robot in enumerate(robots, start=1):
        print(f"Robot {idx}: x={robot['x']}, y={robot['y']} | vx={robot['vx']}, vy={robot['vy']}")

    # Define grid size and simulation parameters
    width, height = 101, 103  # As per problem statement
    max_seconds = 10000  # Number of seconds to simulate

    # Define frames directory
    frames_dir = os.path.join(directory, 'frames')

    # Simulate robot movements, save frames, and detect clusters
    print("\nSimulating robot movements...")
    simulate_movements(robots, width, height, max_seconds, save_frames=True, frames_dir=frames_dir)
    print(f"Simulation completed for {max_seconds} seconds.")
    print(f"Frames saved in directory: {frames_dir}")

    # Inform the user about detected frames
    detected_dir = os.path.join(frames_dir, 'detected')
    if os.path.exists(detected_dir):
        detected_frames = os.listdir(detected_dir)
        if detected_frames:
            print(f"\nDetected potential Christmas tree in {len(detected_frames)} frames:")
            for frame in detected_frames:
                print(f" - {frame}")
        else:
            print("\nNo significant clusters detected.")
    else:
        print("\nNo clusters exceeded the threshold of 50 connected robots.")

if __name__ == "__main__":
    main()
