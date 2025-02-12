import numpy as np
import os

def read_grid(file_path):
    """
    Reads the grid from the input file and returns it as a list of strings.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list: A list of strings, where each string represents a row of the grid.
    """
    with open(file_path, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]
    return grid

def parse_grid(grid):
    """
    Parse the input grid into a list of antennas with their positions.

    Args:
        data (str): Input grid as a multiline string.

    Returns:
        dict: A dictionary where keys are frequencies, and values are lists of (x, y) positions.
    """
    antennas = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '.':
                if cell not in antennas:
                    antennas[cell] = []
                antennas[cell].append((x, y))
    print(antennas)
    return antennas

"""
def find_antinode_positions(antennas):
    """
    #Find all unique antinode positions created by antennas.

    #Args:
    #    antennas (dict): Dictionary of frequencies and their positions.

    #Returns:
    #    set: A set of unique antinode positions.
"""
    antinodes = set()

    for freq, positions in antennas.items():
        # Find all pairs of antennas with the same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Compute the differences in coordinates
                dx, dy = x2 - x1, y2 - y1

                # Check for alignment (horizontal, vertical, or diagonal)
                if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                    # Check the twice distance condition
                    mid_x, mid_y = x1 + dx // 2, y1 + dy // 2
                    if (x1 + dx // 2, y1 + dy // 2) in positions:
                        continue  # Ensure mid is antenna  
                        continue  
                    # Compute potential antinodes
                    antinode1 = (x1 - dx, y1 - dy)
                    antinode2 = (x2 + dx, y2 + dy)

                    # Add to the set of antinodes
                    antinodes.add(antinode1)
                    antinodes.add(antinode2)

    return antinodes
"""


def find_antinode_positions(antennas, grid):
    """
    Find all unique antinode positions created by antennas.

    Args:
        antennas (dict): Dictionary of frequencies and their positions.

    Returns:
        set: A set of unique antinode positions.
    """
    grid_width, grid_height = len(grid[0]), len(grid)

    antinodes = set()

    for freq, positions in antennas.items():
        # Find all pairs of antennas with the same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Calculate the alignment vector
                vector_x, vector_y = x2 - x1, y2 - y1

                # Compute the antinode positions
                antinode1 = (x1 - vector_x, y1 - vector_y)  # Outside the first antenna
                antinode2 = (x2 + vector_x, y2 + vector_y)  # Outside the second antenna

                # Check bounds and add to the set if valid
                if 0 <= antinode1[0] < grid_width and 0 <= antinode1[1] < grid_height:
                    antinodes.add(antinode1)
                if 0 <= antinode2[0] < grid_width and 0 <= antinode2[1] < grid_height:
                    antinodes.add(antinode2)

    return antinodes


def count_antinodes(data):
    """
    Count the total number of unique antinode locations.

    Args:
        data (str): Input grid as a multiline string.

    Returns:
        int: Total number of unique antinodes.
    """
    antennas = parse_grid(data)
    antinodes = find_antinode_positions(antennas, data)
    return len(antinodes)


def main():
    import os
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(directory, 'input.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    #file_path = os.path.join(directory, 'input2.txt')

    #with open(file_path, "r") as file:
    #    data = file.read()
    data = read_grid(file_path)

    result = count_antinodes(data)
    print(f"Total unique antinode locations: {result}")

# Example usage with your input
if __name__ == "__main__":
    main()
