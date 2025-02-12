import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import animation
from collections import deque

def read_map(file_path):
    with open(file_path, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]
    return grid

def find_start(grid):
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 'S':
                return row_idx, col_idx
    return None

def bfs_with_visualization(grid, start_row, start_col, target_distance):
    rows = len(grid)
    cols = len(grid[0])
    queue = deque()
    queue.append((start_row, start_col, 0))  # row, col, steps
    positions_at_steps = {}  # Key: steps, Value: set of positions
    visited = set()  # Keep track of (row, col, steps)

    while queue:
        row, col, steps = queue.popleft()

        if steps > target_distance:
            continue  # Exceeded the target steps

        # Record the position at the current step
        if steps not in positions_at_steps:
            positions_at_steps[steps] = set()
        positions_at_steps[steps].add((row, col))

        # Possible moves: up, down, left, right
        for delta_row, delta_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + delta_row
            new_col = col + delta_col

            # Check bounds
            if 0 <= new_row < rows and 0 <= new_col < cols:
                cell = grid[new_row][new_col]
                if cell == '.' or cell == 'S':
                    next_step = steps + 1
                    state = (new_row, new_col, next_step)
                    if state not in visited:
                        visited.add(state)
                        queue.append((new_row, new_col, next_step))

    return positions_at_steps

def animate_paths(grid, positions_at_steps, target_distance):
    rows = len(grid)
    cols = len(grid[0])

    # Initialize the grid for animation
    grid_visual = np.full((rows, cols), -2, dtype=int)  # Initialize with -2 (unreached garden plots)

    # Initialize the grid with rocks and starting position
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            if cell == '#':
                grid_visual[row, col] = -1  # Rocks
            elif cell == '.':
                grid_visual[row, col] = 0   # Garden plots
            elif cell == 'S':
                grid_visual[row, col] = 1  # Starting position

    # Create a color map using a built-in colormap
    cmap = plt.cm.viridis
    cmap.set_under('black')  # For rocks
    cmap.set_under('white')  # For garden plots
    cmap.set_over('yellow')  # For starting position

    # Define the normalization
    norm = colors.Normalize(vmin=0, vmax=target_distance)

    fig, ax = plt.subplots(figsize=(cols / 2, rows / 2))
    im = ax.imshow(grid_visual, cmap=cmap, norm=norm)
    ax.set_title(f"Elf's Reachable Positions in {target_distance} Steps")
    ax.axis('off')

    # Animation function
    def update(step):
        # For each step, update the grid_visual with positions reached at that step
        if step in positions_at_steps:
            for position in positions_at_steps[step]:
                row, col = position
                grid_visual[row, col] = step
        im.set_array(grid_visual)
        ax.set_title(f"Elf's Reachable Positions - Step {step}/{target_distance}")
        return [im]

    ani = animation.FuncAnimation(
        fig, update, frames=range(target_distance + 1), blit=False, interval=500, repeat=False
    )

    plt.show()

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    file_path = directory+'input.txt'

    grid = read_map(file_path)
    start_pos = find_start(grid)
    if start_pos is None:
        print("Starting position 'S' not found in the map.")
        return
    start_row, start_col = start_pos
    target_distance = 64  # Change to 64 for your actual puzzle

    positions_at_steps = bfs_with_visualization(grid, start_row, start_col, target_distance)
    reachable_positions = len(positions_at_steps.get(target_distance, []))
    print(f"Number of garden plots reachable in exactly {target_distance} steps: {reachable_positions}")

    # Animate the paths
    animate_paths(grid, positions_at_steps, target_distance)

if __name__ == "__main__":
    main()
