from functools import lru_cache
from collections import deque

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

def find_shortest_path(start, target, keypad):
    """
    Performs BFS to find the shortest number of directional moves from start to target.
    Returns the number of steps required.
    """
    if start == target:
        return 0

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
    return float('inf')  # Return infinity if no path is found

@lru_cache(maxsize=None)
def find_min_moves(code, start='A', depth=0):
    """
    Recursively finds the minimum number of button presses required to type the code.
    
    Parameters:
    - code: The code string to type (e.g., '029A').
    - start: The starting button on the current layer (default is 'A').
    - depth: The current layer depth (0 to 3).
    
    Returns:
    - The total number of button presses required to type the code from the current state.
    """
    if not code:
        return 0

    # Adjust keypad selection based on layer depth
    if depth == 3:
        keypad = numeric_keypad_adjacency
    elif depth < 3:
        keypad = directional_keypad_adjacency
    else:
        # Invalid depth, return infinity to indicate no valid path
        return float('inf')

    target = code[0]

    # Check if we're at the Numeric Keypad layer
    if depth == 3 and target in numeric_keypad_adjacency:
        # Move to target on Numeric Keypad and press 'A'
        moves = find_shortest_path(start, target, keypad) + 1  # +1 for pressing 'A'
        # After pressing, reset to starting position for the next press
        return moves + find_min_moves(code[1:], 'A', 0)
    
    # For Directional Keypads (Layers 0,1,2)
    elif depth < 3:
        # Move to target direction on current directional keypad and press 'A'
        moves = find_shortest_path(start, target, keypad) + 1  # +1 for pressing 'A'
        # Proceed to the next layer
        return moves + find_min_moves(code, 'A', depth + 1)
    
    else:
        # If depth is out of bounds, return infinity
        return float('inf')

def calculate_complexity(code):
    """
    Calculates the complexity of a single code.
    
    Parameters:
    - code: The code string to type (e.g., '029A').
    
    Returns:
    - The complexity value (numeric part * sequence length).
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
            print(f"Code: {code}, Sequence Length: {complexity // int(''.join(filter(str.isdigit, code)) or 1)}, Numeric Part: {''.join(filter(str.isdigit, code))}, Complexity: {complexity}")
        total_complexity += complexity
    return total_complexity

# Example usage
if __name__ == "__main__":
    example_codes = ['029A', '980A', '179A', '456A', '379A']
    result = solve_puzzle(example_codes)
    print(f"Total complexity: {result}")
