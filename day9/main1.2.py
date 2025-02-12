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
        #grid = [line.strip() for line in f if line.strip()]
        data = f.read()
        print(type(data))
    return data


def iterate(data):
    refactored_data = ''
    index = 0
    for i in range(len(data)):
        multiplier = int(data[i])
        if i % 2 == 0:
            #for j in range(int(data[i])):
            #    refactored_data += j
            refactored_data += str(index) * multiplier
            index += 1
        else:
           refactored_data += '.' * multiplier 
    
    return refactored_data

def move(data):
    """
    Compact the disk map by moving file blocks left to fill the free spaces.

    Args:
        data (str): The disk map as a string.

    Returns:
        str: The compacted disk map.
    """
    # Convert the string to a list for in-place modification
    disk = list(data)
    write_idx = 0  # The position to write the next file block

    # Iterate through the disk and compact files
    for read_idx in range(len(disk)):
        if disk[read_idx] != '.':  # If it's a file block
            disk[write_idx] = disk[read_idx]
            if write_idx != read_idx:  # Only overwrite if necessary
                disk[read_idx] = '.'
            write_idx += 1

    return ''.join(disk)  # Convert back to a string


def checksum(data):
    """
    Calculate the checksum of the compacted disk map.

    Args:
        data (str): The compacted disk map as a string.

    Returns:
        int: The checksum value.
    """
    total = 0
    for i, char in enumerate(data):
        if char != '.':  # Ignore free space
            total += i * int(char)
    return total


def main():
    import os
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(directory, 'input.txt')  # Ensure your input file is named 'input.txt'
    #file_path = os.path.join(directory, 'input2.txt')  # Ensure your input file is named 'input.txt'
    
    # Read and process the data
    data = read_grid(file_path)
    print("Initial data:", data)
    
    # Expand the disk map
    data_expanded = iterate(data)
    print("Expanded disk map:", data_expanded)
    
    # Compact the disk map
    while '.' in data_expanded:  # Repeat until all free spaces are filled
        data_expanded = move(data_expanded)
        print("After move:", data_expanded)
    
    # Calculate the checksum
    result = checksum(data_expanded)
    print("Checksum:", result)


# Example usage with your input
if __name__ == "__main__":
    main()
