from collections import deque
import sys

# Define the numeric keypad layout
numeric_keypad = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
    '0': (1, 3), 'A': (2, 3)
}

# Reverse mapping from coordinates to keys for numeric keypad
numeric_coord_to_key = {v: k for k, v in numeric_keypad.items()}

# Define the directional keypad layout
directional_keypad = {
    '^': (0, 0), 'A': (1, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
}

# Reverse mapping from coordinates to keys for directional keypad
directional_coord_to_key = {v: k for k, v in directional_keypad.items()}

def bfs(start_key, keypad, coord_to_key):
    """
    Performs BFS to find the shortest number of directional button presses
    required to move from start_key to all other keys on the given keypad.
    
    Args:
    - start_key (str): Starting key.
    - keypad (dict): Mapping of keys to their (x, y) coordinates.
    - coord_to_key (dict): Mapping from coordinates to keys.
    
    Returns:
    - dict: Mapping from target keys to minimal number of directional presses.
    """
    visited = set()
    queue = deque()
    distances = {}
    
    start_pos = keypad[start_key]
    queue.append((start_pos, 0))
    visited.add(start_pos)
    
    # Define movement directions with priority: '<', '^', 'v', '>'
    movement_order = ['<', '^', 'v', '>']
    movement_map = {
        '<': (-1, 0),
        '^': (0, -1),
        'v': (0, 1),
        '>': (1, 0)
    }
    
    while queue:
        (x, y), steps = queue.popleft()
        current_key = coord_to_key.get((x, y))
        if current_key:
            distances[current_key] = steps
        for move in movement_order:
            dx, dy = movement_map[move]
            nx, ny = x + dx, y + dy
            if (nx, ny) in coord_to_key:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))
    
    return distances

# Precompute shortest paths for numeric keypad
numeric_shortest_paths = {}
for key in numeric_keypad:
    numeric_shortest_paths[key] = bfs(key, numeric_keypad, numeric_coord_to_key)

# Precompute shortest paths for directional keypad
directional_shortest_paths = {}
for key in directional_keypad:
    directional_shortest_paths[key] = bfs(key, directional_keypad, directional_coord_to_key)

def compute_minimal_sequence_length(code, numeric_shortest_paths, directional_shortest_paths):
    """
    Computes the minimal number of button presses across all layers to type the given code.
    
    Args:
    - code (str): The code to type (e.g., '029A').
    - numeric_shortest_paths (dict): Precomputed shortest paths for numeric keypad.
    - directional_shortest_paths (dict): Precomputed shortest paths for directional keypads.
    
    Returns:
    - int: Minimal total number of button presses required.
    """
    # State: (your_pos, robot2_pos, robot1_pos, index_in_code)
    # Initial state: all at 'A', index 0
    initial_state = ('A', 'A', 'A', 0)
    queue = deque()
    queue.append((initial_state, 0))  # ((state), total_presses)
    
    visited = set()
    visited.add(initial_state)
    
    # Define button press order priority: '<', '^', 'v', '>'
    button_order = ['<', '^', 'v', '>']
    
    while queue:
        (your_pos, robot2_pos, robot1_pos, idx), total_presses = queue.popleft()
        
        # If all characters have been pressed
        if idx == len(code):
            return total_presses
        
        # Possible button presses: '<', '^', 'v', '>', 'A'
        for button in button_order + ['A']:
            # Initialize new positions as current
            new_your_pos = your_pos
            new_robot2_pos = robot2_pos
            new_robot1_pos = robot1_pos
            new_idx = idx
            additional_presses = 0
            
            if button in ['<', '^', 'v', '>']:
                # Move your directional keypad
                movement_map = {
                    '<': (-1, 0),
                    '^': (0, -1),
                    'v': (0, 1),
                    '>': (1, 0)
                }
                dx, dy = movement_map[button]
                your_x, your_y = directional_keypad[your_pos]
                your_target_x, your_target_y = your_x + dx, your_y + dy
                # Check if the target position is valid
                if (your_target_x, your_target_y) in directional_shortest_paths['A']:
                    your_target_key = directional_coord_to_key.get((your_target_x, your_target_y))
                    if not your_target_key:
                        continue  # Invalid move, skip
                    new_your_pos = your_target_key
                else:
                    continue  # Invalid move, skip
                
                # Similarly, move Robot2's directional keypad
                robot2_x, robot2_y = directional_keypad[robot2_pos]
                robot2_target_x, robot2_target_y = robot2_x + dx, robot2_y + dy
                if (robot2_target_x, robot2_target_y) in directional_shortest_paths['A']:
                    robot2_target_key = directional_coord_to_key.get((robot2_target_x, robot2_target_y))
                    if not robot2_target_key:
                        continue  # Invalid move, skip
                    new_robot2_pos = robot2_target_key
                else:
                    continue  # Invalid move, skip
                
                # Similarly, move Robot1's directional keypad
                robot1_x, robot1_y = directional_keypad[robot1_pos]
                robot1_target_x, robot1_target_y = robot1_x + dx, robot1_y + dy
                if (robot1_target_x, robot1_target_y) in directional_shortest_paths['A']:
                    robot1_target_key = directional_coord_to_key.get((robot1_target_x, robot1_target_y))
                    if not robot1_target_key:
                        continue  # Invalid move, skip
                    new_robot1_pos = robot1_target_key
                else:
                    continue  # Invalid move, skip
                    
                # Each movement corresponds to 3 button presses (You, Robot2, Robot1)
                additional_presses = 3
            elif button == 'A':
                # Activate 'A' on your keypad
                # This sends 'A' to Robot2's and Robot1's keypads
                # Activate on Robot1's keypad: press the current numeric keypad button
                
                # Press 'A' on your keypad
                # Press 'A' on Robot2's keypad
                # Press 'A' on Robot1's keypad
                # Total presses: 3
                
                # Each 'A' press corresponds to 3 button presses
                additional_presses = 3
                
                # Check if Robot1's current position matches the target character
                if robot1_pos == code[idx]:
                    new_idx = idx + 1  # Pressed the correct character
                else:
                    # 'A' pressed on Robot1's keypad but not the desired character
                    # Invalid press, skip
                    continue
            
            # Form the new state
            new_state = (new_your_pos, new_robot2_pos, new_robot1_pos, new_idx)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, total_presses + additional_presses))
    
def read_codes(file_path):
    """Reads codes from a file, each code on a separate line."""
    codes = []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.strip()
            if row:
                codes.append(row)
    return codes

def compute_complexities(codes, numeric_shortest_paths, directional_shortest_paths):
    """
    Computes the sum of complexities for all codes.
    
    Args:
    - codes (list of str): List of codes to type.
    - numeric_shortest_paths (dict): Precomputed shortest paths for numeric keypad.
    - directional_shortest_paths (dict): Precomputed shortest paths for directional keypads.
    
    Returns:
    - int: Total sum of complexities.
    """
    total_complexity = 0
    for code in codes:
        sequence_length = compute_minimal_sequence_length(code, numeric_shortest_paths, directional_shortest_paths)
        if sequence_length == float('inf'):
            print(f"Code '{code}' cannot be typed due to unreachable keys.")
            continue
        # Extract numeric part (ignore leading zeros)
        numeric_part = ''.join(filter(str.isdigit, code))
        numeric_value = int(numeric_part) if numeric_part else 0
        complexity = sequence_length * numeric_value
        print(f"Code: {code}, Sequence Length: {sequence_length}, Numeric Part: {numeric_value}, Complexity: {complexity}")
        total_complexity += complexity
    return total_complexity

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
    
    # Read the codes from the file
    codes = read_codes(file_path)
    print("Codes to type:", codes)
    print()
    
    # Compute complexities
    total_complexity = compute_complexities(codes, numeric_shortest_paths, directional_shortest_paths)
    
    print(f"\nTotal sum of complexities: {total_complexity}")

if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()
