import os
from collections import deque
from functools import lru_cache
import sys

def create_button_mapping(keypad):
    mapping = {}
    for r, row in enumerate(keypad):
        for c, key in enumerate(row):
            if key is not None:
                mapping[key] = (r, c)
    return mapping

# Define the keypads
numpad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
]

directional_keypad = [
    [None, '^', 'A'],
    ['<', 'v', '>']
]

# Create mappings
numpad_mapping = create_button_mapping(numpad)
directional_mapping = create_button_mapping(directional_keypad)

def bfs_shortest_sequence(keypad_mapping, keypad, start, target):
    if start == target:
        return ''
    
    start_pos = keypad_mapping[start]
    target_pos = keypad_mapping[target]
    
    rows = len(keypad)
    cols = len(keypad[0])
    
    # Define moves: (delta_row, delta_col, button_press)
    moves = [
        (-1, 0, '^'),  # Up
        (1, 0, 'v'),   # Down
        (0, -1, '<'),  # Left
        (0, 1, '>')     # Right
    ]
    
    visited = set()
    queue = deque()
    queue.append((start_pos, ''))
    visited.add(start_pos)
    
    while queue:
        current_pos, path = queue.popleft()
        for dr, dc, button in moves:
            new_r = current_pos[0] + dr
            new_c = current_pos[1] + dc
            if 0 <= new_r < rows and 0 <= new_c < cols:
                if keypad[new_r][new_c] is not None:
                    new_pos = (new_r, new_c)
                    if new_pos == target_pos:
                        return path + button
                    if new_pos not in visited:
                        visited.add(new_pos)
                        queue.append((new_pos, path + button))
    return None  # No path found

@lru_cache(maxsize=None)
def get_sequence_numeric(start, target):
    return bfs_shortest_sequence(numpad_mapping, numpad, start, target)

@lru_cache(maxsize=None)
def get_sequence_directional(start, target):
    return bfs_shortest_sequence(directional_mapping, directional_keypad, start, target)

def produce_final_sequence_for_code(code):
    """
    Given a code (e.g., '029A'), produces the shortest sequence of button presses
    on your directional keypad to cause the robot in front of the door to type the code.
    """
    # Initialize the starting positions
    your_start = 'A'        # Your directional keypad starts at 'A'
    robot1_start = 'A'      # Robot1's directional keypad starts at 'A'
    robot2_start = 'A'      # Robot2's directional keypad starts at 'A'
    numeric_start = 'A'     # Numeric keypad starts at 'A'
    
    total_sequence = ''
    
    # Iterate over each character in the code
    for char in code:
        if char == 'A':
            # To press 'A', send 'A' through all three layers
            seq = 'A' * 3  # 'A' for your keypad, robot1, robot2
            total_sequence += seq
            # After pressing 'A', the arm remains at 'A'
            continue
        
        # For numeric characters, build the sequence through all layers
        
        # Step 1: Determine the sequence on the numeric keypad to press 'char' from 'A'
        seq_numeric_move = get_sequence_numeric(numeric_start, char)
        if seq_numeric_move is None:
            raise ValueError(f"No path from {numeric_start} to {char} on numeric keypad.")
        seq_numeric = seq_numeric_move + 'A'  # 'A' to press the button
        
        # Step 2: This sequence needs to be sent to robot1 via robot2
        # Each character in seq_numeric is a button press on robot1's keypad
        # For each button in seq_numeric, find the sequence on robot1's keypad
        seq_robot1 = ''
        current_robot1_pos = robot1_start
        for btn in seq_numeric:
            if btn not in directional_mapping:
                raise ValueError(f"Invalid button '{btn}' on directional keypad.")
            move_seq = get_sequence_directional(current_robot1_pos, btn)
            if move_seq is None:
                raise ValueError(f"No path from {current_robot1_pos} to {btn} on directional keypad.")
            seq_robot1 += move_seq + 'A'  # 'A' to send the button press
            current_robot1_pos = btn  # Update the current position
        
        # Step 3: Send seq_robot1 to robot2 via your directional keypad
        seq_robot2 = ''
        current_robot2_pos = robot2_start
        for btn in seq_robot1:
            if btn not in directional_mapping:
                raise ValueError(f"Invalid button '{btn}' on directional keypad.")
            move_seq = get_sequence_directional(current_robot2_pos, btn)
            if move_seq is None:
                raise ValueError(f"No path from {current_robot2_pos} to {btn} on directional keypad.")
            seq_robot2 += move_seq + 'A'  # 'A' to send the button press
            current_robot2_pos = btn  # Update the current position
        
        # Append the sequence for this character
        total_sequence += seq_robot2
    
    return total_sequence

def compute_complexity(code, sequence):
    # Extract numeric part by removing 'A's and leading zeros
    numeric_part_str = ''.join(filter(str.isdigit, code))
    numeric_part = int(numeric_part_str) if numeric_part_str else 0
    # Compute complexity
    return len(sequence) * numeric_part

def read_codes(file_path):
    codes = []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.strip()
            if row:
                codes.append(row)
    return codes

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')  # Ensure 'input.txt' exists with the codes
    file_path = os.path.join(directory, 'input2.txt')  # Ensure 'input.txt' exists with the codes
    
    codes = read_codes(file_path)
    print("Codes to process:", codes)
    
    total_complexity = 0
    for c in codes:
        try:
            seq = produce_final_sequence_for_code(c)
            # Compute complexity
            comp = compute_complexity(c, seq)
            print(f"Code: {c}, Sequence Length: {len(seq)}, Numeric Part: {''.join(filter(str.isdigit, c))}, Complexity: {comp}")
            total_complexity += comp
        except ValueError as ve:
            print(f"Error processing code {c}: {ve}")
    
    print("Total Complexity:", total_complexity)

if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()
