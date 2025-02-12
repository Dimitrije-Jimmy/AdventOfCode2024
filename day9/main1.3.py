import os

def read_grid(file_path):
    """
    Reads the disk map from the input file and returns it as a string.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: The disk map string.
    """
    with open(file_path, 'r') as f:
        data = f.read().strip()
    return data

def iterate(data):
    """
    Converts the compact disk map into a list representation with file IDs and free spaces.

    Args:
        data (str): The compact disk map string.

    Returns:
        list: A list representing the disk blocks with file IDs and free spaces.
    """
    refactored_data = []
    index = 0  # File ID starts at 0
    for i, char in enumerate(data):
        multiplier = int(char)
        if i % 2 == 0:
            # File blocks: append file ID as string
            refactored_data.extend([str(index)] * multiplier)
            index += 1
        else:
            # Free space blocks: append '.'
            refactored_data.extend(['.'] * multiplier)
    return refactored_data

def move(data):     # useless
    """
    Compacts the disk by moving all file blocks to the left, maintaining their order.

    Args:
        data (list): The list representing disk blocks.

    Returns:
        list: The compacted list with all file blocks moved to the left.
    """
    # Extract all file blocks (exclude free spaces)
    compacted = [block for block in data if block != '.']
    # Calculate the number of free spaces
    free_spaces = len(data) - len(compacted)
    # Append free spaces at the end
    compacted.extend(['.'] * free_spaces)
    return compacted

def move_step(data):
    """
    Performs a single move: moves the rightmost file block into the leftmost free space.

    Args:
        data (list): The list representing disk blocks.

    Returns:
        bool: True if a move was performed, False otherwise.
    """
    # Find the leftmost free space
    try:
        free_idx = data.index('.')
    except ValueError:
        # No free space
        return False

    # Find the rightmost file block to the right of the free space
    for i in range(len(data)-1, free_idx, -1):
        if data[i] != '.':
            # Move the block from i to free_idx
            data[free_idx] = data[i]
            data[i] = '.'
            return True

    # No file block found to move
    return False

def checksum(data):
    """
    Calculates the filesystem checksum.

    Args:
        data (list): The compacted list representing disk blocks.

    Returns:
        int: The checksum value.
    """
    total = 0
    for position, block in enumerate(data):
        if block != '.':
            total += position * int(block)
    return total

def main():
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Replace 'input2.txt' with your actual input file name
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    
    # Read the disk map from the input file
    data = read_grid(file_path)
    print(f"Original Disk Map: {data}")
    
    # Convert the disk map into a list with file IDs and free spaces
    data2 = iterate(data)
    print(f"Expanded Disk Blocks: {''.join(data2)}")
    
    # Perform step-by-step moves until no more moves can be made
    move_count = 0
    while move_step(data2):
        move_count += 1
        # Uncomment the following line to see each step (may slow down for large inputs)
        # print(f"After move {move_count}: {''.join(data2)}")
    
    print(f"Total Moves Performed: {move_count}")
    print(f"Compacted Disk Blocks: {''.join(data2)}")
    
    # Calculate the filesystem checksum
    result = checksum(data2)
    print(f"Filesystem Checksum: {result}")

if __name__ == "__main__":
    main()
