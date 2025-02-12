from itertools import combinations
from collections import deque

# Define the numeric keypad layout
keypad = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
    '0': (1, 3), 'A': (2, 3)
}

# Reverse mapping from coordinates to keys
coord_to_key = {v: k for k, v in keypad.items()}

def bfs(start, end, keypad):
    """
    Performs BFS to find the minimal number of directional button presses
    to move from start key to end key on the numeric keypad.
    
    Args:
    - start (str): Starting key.
    - end (str): Destination key.
    - keypad (dict): Mapping of keys to their (x, y) coordinates.
    
    Returns:
    - int: Minimal number of directional button presses.
    """
    if start == end:
        return 0  # No movement needed

    visited = set()
    queue = deque()
    
    # Start from the starting key
    queue.append((keypad[start], 0))
    visited.add(keypad[start])
    
    # Define movement directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (dx, dy)
    
    while queue:
        (x, y), steps = queue.popleft()
        
        # Explore all possible directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in coord_to_key:
                if (nx, ny) == keypad[end]:
                    return steps + 1  # Reached destination
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))
    return float('inf')  # Destination not reachable

def compute_sequence_length(code, keypad):
    """
    Computes the minimal number of button presses on the directional keypad
    to type the given code on the numeric keypad.
    
    Args:
    - code (str): The code to type (e.g., '029A').
    - keypad (dict): Mapping of keys to their (x, y) coordinates.
    
    Returns:
    - int: Total number of button presses required.
    """
    total_presses = 0
    current_position = 'A'  # Starting at 'A'
    
    for char in code:
        # Find minimal movement steps from current_position to char
        moves = bfs(current_position, char, keypad)
        if moves == float('inf'):
            print(f"Cannot reach {char} from {current_position}")
            return float('inf')
        # Each move corresponds to one button press
        total_presses += moves
        # Press 'A' to activate (one button press)
        total_presses += 1
        # Update current position
        current_position = char
    return total_presses

def main():
    """
    Main function to execute the solution.
    """
    import os
    
    # Define the input file name
    input_file = 'input.txt'  # Replace with your actual input file name
    input_file = 'input2.txt'  # Replace with your actual input file name
    
    # Determine the script's directory to locate the input file
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, input_file)
    
    # Check if the input file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{input_file}' does not exist in the directory '{directory}'.")
        return
    
    # Read the network map from the file (assuming it's a list of codes)
    # For this problem, the input seems to be the list of codes, not connections.
    # Thus, read the five codes from the file.
    
    with open(file_path, 'r') as file:
        codes = [line.strip() for line in file if line.strip()]
    
    # Validate that there are exactly five codes
    if len(codes) != 5:
        print(f"Error: Expected 5 codes, but found {len(codes)} in '{input_file}'.")
        return
    
    # Compute complexities
    total_complexity = 0
    for code in codes:
        # Extract numeric part (ignore leading zeros)
        numeric_part = ''.join(filter(str.isdigit, code))
        numeric_value = int(numeric_part) if numeric_part else 0
        # Compute sequence length
        sequence_length = compute_sequence_length(code, keypad)
        if sequence_length == float('inf'):
            print(f"Code '{code}' cannot be typed due to unreachable keys.")
            continue
        # Compute complexity
        complexity = sequence_length * numeric_value
        print(f"Code: {code}, Sequence Length: {sequence_length}, Numeric Part: {numeric_value}, Complexity: {complexity}")
        total_complexity += complexity
    
    print(f"\nTotal sum of complexities: {total_complexity}")

if __name__ == "__main__":
    main()
