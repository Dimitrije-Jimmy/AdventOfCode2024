from functools import lru_cache

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
    if start == target:
        return 0
        
    visited = {start}
    queue = [(start, 0)]
    
    while queue:
        pos, steps = queue.pop(0)
        for direction in ['^', 'v', '<', '>']:
            if pos in keypad and direction in keypad[pos]:
                next_pos = keypad[pos][direction]
                if next_pos and next_pos not in visited:
                    if next_pos == target:
                        return steps + 1
                    visited.add(next_pos)
                    queue.append((next_pos, steps + 1))
    return float('inf')

@lru_cache(maxsize=None)
def find_min_presses(target, current='A', depth=0):
    if not target:
        return 0
    
    current_keypad = directional_keypad_adjacency if depth > 0 else numeric_keypad_adjacency
    next_digit = target[0]
    steps = find_shortest_path(current, next_digit, current_keypad)
    
    if steps == float('inf'):
        return float('inf')
        
    return steps + 1 + find_min_presses(target[1:], next_digit, depth + 1)

def calculate_complexity(code):
    numeric_value = int(''.join(filter(str.isdigit, code)))
    presses = find_min_presses(code)
    return numeric_value * presses

def solve_puzzle(codes):
    return sum(calculate_complexity(code) for code in codes)

example_codes = ['029A', '980A', '179A', '456A', '379A']
result = solve_puzzle(example_codes)
print(f"Total complexity: {result}")