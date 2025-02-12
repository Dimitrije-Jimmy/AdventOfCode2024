from collections import deque
from functools import lru_cache

# Define the adjacency for the numeric keypad
numeric_keypad_adjacency = {
    '7': {'^': None, 'v': '4', '<': None, '>': '8'},
    '8': {'^': None, 'v': '5', '<': '7', '>': '9'},
    '9': {'^': None, 'v': '6', '<': '8', '>': None},
    '4': {'^': '7', 'v': '1', '<': None, '>': '5'},
    '5': {'^': '8', 'v': '2', '<': '4', '>': '6'},
    '6': {'^': '9', 'v': '3', '<': '5', '>': None},
    '1': {'^': '4', 'v': None, '<': None, '>': '2'},
    '2': {'^': '5', 'v': '0', '<': '1', '>': '3'},
    '3': {'^': '6', 'v': 'A', '<': '2', '>': None},
    '0': {'^': '2', 'v': None, '<': None, '>': 'A'},
    'A': {'^': '3', 'v': None, '<': '0', '>': None}
}

# Define the adjacency for the directional keypad
directional_keypad_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None}
}

# Define movement directions
directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

def create_mappings(layout):
    """
    Creates button-to-position and position-to-button mappings.
    
    Parameters:
    - layout: List of lists representing the keypad buttons.
    
    Returns:
    - button_to_pos: Dict mapping button names to (row, col) tuples.
    - pos_to_button: Dict mapping (row, col) tuples to button names.
    """
    button_to_pos = {}
    pos_to_button = {}
    for r, row in enumerate(layout):
        for c, button in enumerate(row):
            if button != 'gap':
                button_to_pos[button] = (r, c)
                pos_to_button[(r, c)] = button
    return button_to_pos, pos_to_button

# Create mappings for numeric keypad
numeric_button_to_pos, numeric_pos_to_button = create_mappings([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['gap', '0', 'A']
])

# Create mappings for directional keypad
directional_button_to_pos, directional_pos_to_button = create_mappings([
    ['gap', '^', 'A'],
    ['<', 'v', '>']
])

def move(current_button, direction, keypad_layout, button_to_pos):
    """
    Moves the arm in the specified direction on the given keypad.
    
    Parameters:
    - current_button: Current button name (str).
    - direction: Direction to move ('^', 'v', '<', '>').
    - keypad_layout: Dict mapping (row, col) to button names.
    - button_to_pos: Dict mapping button names to (row, col).
    
    Returns:
    - new_button: The button name after moving. If move is invalid, returns current_button.
    """
    dr, dc = directions[direction]
    current_pos = button_to_pos[current_button]
    new_r = current_pos[0] + dr
    new_c = current_pos[1] + dc
    if (new_r, new_c) in keypad_layout:
        return keypad_layout[(new_r, new_c)]
    else:
        return current_button  # If move is invalid, stay in place

def find_shortest_path(start, target, keypad):
    """
    Performs BFS to find the shortest number of directional moves from start to target.
    
    Parameters:
    - start: Starting button name (str).
    - target: Target button name (str).
    - keypad: Adjacency dictionary for the keypad.
    
    Returns:
    - steps: Number of steps to reach target. Returns float('inf') if unreachable.
    """
    queue = deque([(start, 0)])
    seen = {start}
    
    while queue:
        pos, steps = queue.popleft()
        if pos == target:
            return steps
        for direction, next_pos in keypad[pos].items():
            if next_pos and next_pos not in seen:
                seen.add(next_pos)
                queue.append((next_pos, steps + 1))
    return float('inf')  # If no path found

@lru_cache(maxsize=None)
def find_min_moves(code, start='A', depth=0):
    """
    Recursively finds the minimum number of button presses required to type the code.
    
    Parameters:
    - code: The code string to type (e.g., '029A').
    - start: The starting button on the current layer (default is 'A').
    - depth: The current layer depth (0 to 3).
    
    Returns:
    - Total number of button presses required to type the code from the current state.
    """
    if not code:
        return 0
    
    # Define layer mapping: depth 0-3 correspond to Layers 1-4
    if depth == 3:
        keypad = numeric_keypad_adjacency
        button_to_pos = numeric_button_to_pos
        pos_to_button = numeric_pos_to_button
    elif depth < 3:
        keypad = directional_keypad_adjacency
        button_to_pos = directional_button_to_pos
        pos_to_button = directional_pos_to_button
    else:
        # Invalid depth
        return float('inf')
    
    target = code[0]
    
    # If we're at the Numeric Keypad layer
    if depth == 3 and target in numeric_keypad_adjacency:
        # Find path to target on Numeric Keypad
        moves = find_shortest_path(start, target, keypad)
        if moves == float('inf'):
            return float('inf')
        # +1 for pressing 'A' to activate
        return moves + 1 + find_min_moves(code[1:], 'A', 0)
    
    # For Directional Keypads (Layers 1-3)
    elif depth < 3:
        # Find path to the direction needed to send to next layer
        # Assuming that to send a direction, we need to move to that direction
        # Then press 'A' to send it
        moves = find_shortest_path(start, target, keypad)
        if moves == float('inf'):
            return float('inf')
        # +1 for pressing 'A' to activate and send direction to next layer
        return moves + 1 + find_min_moves(code, 'A', depth + 1)
    
    else:
        # If depth is out of bounds
        return float('inf')

def calculate_complexity(code):
    """
    Calculates the complexity of a single code.
    
    Parameters:
    - code: The code string to type (e.g., '029A').
    
    Returns:
    - Complexity value (numeric part * sequence length).
    """
    numeric_part_str = ''.join(filter(str.isdigit, code))
    numeric_part = int(numeric_part_str) if numeric_part_str else 0
    moves = find_min_moves(code)
    return numeric_part * moves if moves != float('inf') else float('inf')

def solve_puzzle(codes):
    """
    Solves the puzzle by calculating the sum of complexities for all provided codes.
    
    Parameters:
    - codes: A list of code strings to type.
    
    Returns:
    - The total sum of complexities.
    """
    total_complexity = 0
    for code in codes:
        complexity = calculate_complexity(code)
        if complexity == float('inf'):
            print(f"Code: {code}, Sequence Length: inf, Numeric Part: {''.join(filter(str.isdigit, code))}, Complexity: inf")
        else:
            sequence_length = complexity // int(''.join(filter(str.isdigit, code)) or 1)
            print(f"Code: {code}, Sequence Length: {sequence_length}, Numeric Part: {''.join(filter(str.isdigit, code))}, Complexity: {complexity}")
        total_complexity += complexity
    return total_complexity

# Example usage
if __name__ == "__main__":
    example_codes = ['029A', '980A', '179A', '456A', '379A']
    result = solve_puzzle(example_codes)
    print(f"Total complexity: {result}")
