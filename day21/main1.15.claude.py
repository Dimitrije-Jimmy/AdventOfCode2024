from functools import lru_cache
from collections import deque

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

directional_keypad_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None}
}

def find_shortest_path(start, target, keypad):
    queue = deque([(start, 0)])
    seen = {start}
    
    while queue:
        pos, steps = queue.popleft()
        if pos == target:
            return steps
        for next_pos in keypad[pos].values():
            if next_pos and next_pos not in seen:
                seen.add(next_pos)
                queue.append((next_pos, steps + 1))
    return 0

@lru_cache(maxsize=None)
def find_min_moves(code, start='A', depth=0):
    if not code:
        return 0
        
    keypad = numeric_keypad_adjacency if depth == 0 else directional_keypad_adjacency
    target = code[0]
    
    # For robot layers after first, when target is numeric/alpha
    if depth > 0 and target in numeric_keypad_adjacency:
        # Move to target using directional pad
        moves = find_shortest_path(start, 'A', keypad) + 1  # +1 for activation
        return moves + find_min_moves(code, 'A', 0)
        
    # Normal case - find path to target in current keypad
    moves = find_shortest_path(start, target, keypad) + 1  # +1 for activation
    return moves + find_min_moves(code[1:], target, depth + 1)

def calculate_complexity(code):
    numeric_value = int(''.join(filter(str.isdigit, code)))
    moves = find_min_moves(code)
    return numeric_value * moves

def solve_puzzle(codes):
    return sum(calculate_complexity(code) for code in codes)

example_codes = ['029A', '980A', '179A', '456A', '379A']
result = solve_puzzle(example_codes)
print(f"Total complexity: {result}")