from collections import defaultdict
from functools import lru_cache

def create_keypad_maps():
    # Numeric keypad mapping
    numeric = {
        '7': [(0,0)], '8': [(0,1)], '9': [(0,2)],
        '4': [(1,0)], '5': [(1,1)], '6': [(1,2)],
        '1': [(2,0)], '2': [(2,1)], '3': [(2,2)],
        '0': [(3,1)], 'A': [(3,2)]
    }
    
    # Directional keypad mapping
    directional = {
        '^': [(0,1)], 'A': [(0,2)],
        '<': [(1,0)], 'v': [(1,1)], '>': [(1,2)]
    }
    
    return numeric, directional

@lru_cache(maxsize=None)
def find_min_presses(target, current_pos='A', depth=0, keypad_type='numeric'):
    if not target:
        return 0
    
    numeric, directional = create_keypad_maps()
    current_keypad = numeric if keypad_type == 'numeric' else directional
    
    # Get current target digit and remaining digits
    digit = target[0]
    remaining = target[1:]
    
    # Calculate moves needed to reach target digit
    current_coords = current_keypad[current_pos][0]
    target_coords = current_keypad[digit][0]
    
    # Calculate basic moves needed (vertical and horizontal)
    moves = abs(target_coords[0] - current_coords[0]) + abs(target_coords[1] - current_coords[1])
    
    # Add activation press
    total_presses = moves + 1
    
    # Recursively calculate remaining presses
    if remaining:
        next_keypad = 'directional' if depth > 0 else 'numeric'
        total_presses += find_min_presses(remaining, digit, depth + 1, next_keypad)
    
    return total_presses

def calculate_complexity(code):
    # Strip leading zeros and get numeric part
    numeric_part = int(''.join(filter(str.isdigit, code)))
    # Get minimal button presses
    presses = find_min_presses(code)
    return presses * numeric_part

def solve_puzzle(codes):
    total_complexity = 0
    for code in codes:
        complexity = calculate_complexity(code)
        total_complexity += complexity
    return total_complexity

# Test with example codes
example_codes = ['029A', '980A', '179A', '456A', '379A']
result = solve_puzzle(example_codes)
print(f"Total complexity: {result}")  # Should print 126384