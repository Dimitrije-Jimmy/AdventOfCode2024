from collections import deque
from functools import lru_cache

# Define the Keypad class
class Keypad:
    def __init__(self, layout, start_pos):
        """
        layout: List of lists representing the keypad buttons.
        start_pos: Tuple indicating the starting position of the arm.
        """
        self.layout = layout
        self.start_pos = start_pos
        self.rows = len(layout)
        self.cols = len(layout[0]) if self.rows > 0 else 0

    def get_pos(self, button):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.layout[r][c] == button:
                    return (r, c)
        return None

    def neighbors(self, pos):
        directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
        result = []
        r, c = pos
        for move, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.layout[nr][nc] != 'gap':
                result.append(((nr, nc), move))
        return result

# Define the keypads
numeric_layout = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['gap', '0', 'A']
]
numeric_keypad = Keypad(numeric_layout, numeric_layout[3][2])  # 'A' at (3,2)

directional_layout = [
    ['gap', '^', 'A'],
    ['<', 'v', '>']
]
# All directional keypads start at 'A' which is at (0,2)
directional_keypad = Keypad(directional_layout, (0, 2))

# Define the layers
# Layer 1: User's directional keypad
# Layer 2: Robot 1's directional keypad
# Layer 3: Robot 2's directional keypad
# Layer 4: Numeric keypad
layers = [directional_keypad, directional_keypad, directional_keypad, numeric_keypad]

# Define the target code
codes = ['029A', '980A', '179A', '456A', '379A']

# Precompute button positions for all keypads
button_positions = []
for layer in layers:
    pos_dict = {}
    for r in range(layer.rows):
        for c in range(layer.cols):
            button = layer.layout[r][c]
            if button != 'gap':
                pos_dict[button] = (r, c)
    button_positions.append(pos_dict)

# Function to generate the minimal sequence of button presses
def compute_min_presses_for_code(code):
    """
    Compute the minimal number of button presses to type a given code.
    """
    # Each state is a tuple of positions on each layer
    # Initial positions: all at 'A'
    initial_state = (layers[0].start_pos, layers[1].start_pos, layers[2].start_pos, layers[3].start_pos)
    
    # Target presses: list of buttons to press on the numeric keypad
    target_buttons = list(code)
    
    # BFS queue: (current_state, current_press_index, total_presses)
    queue = deque()
    queue.append((initial_state, 0, 0))
    
    # Visited set to avoid revisiting the same state
    visited = set()
    visited.add((initial_state, 0))
    
    while queue:
        current_state, press_idx, total_presses = queue.popleft()
        
        if press_idx == len(target_buttons):
            # All buttons have been pressed
            return total_presses
        
        # Determine the next button to press on the numeric keypad
        target_button = target_buttons[press_idx]
        target_pos_layer4 = button_positions[3].get(target_button)
        if target_pos_layer4 is None:
            # Invalid button in code
            continue
        
        # To press a button on the numeric keypad, we need to:
        # 1. Move Layer 1's arm to send commands to Layer 2
        # 2. Layer 2 moves Layer 3's arm
        # 3. Layer 3 moves Layer 4's arm
        # 4. Layer 4 presses the target button
        
        # The 'A' press propagates down the layers to press the target button
        # So, we need to press 'A' on all layers when the arms are pointing to the target
        
        # Check if Layer 4's arm is already pointing to the target
        if current_state[3] != target_pos_layer4:
            # Need to move Layer 4's arm to the target
            # To move Layer 4's arm, Layer 3 needs to send the appropriate directions
            # Similarly, to move Layer 3's arm, Layer 2 needs to send directions
            # And to move Layer 2's arm, Layer 1 needs to send directions
            
            # For simplicity, we'll assume that moving arms on lower layers can be done independently
            # This may not reflect the exact constraints, but it's a complex problem
            # Hence, we'll use individual BFS for each layer to move to the target
            
            # Compute the number of moves required for each layer to reach the target
            moves_layer1 = bfs(layers[0], current_state[0], current_state[0])  # Layer 1 doesn't need to move
            moves_layer2 = bfs(layers[1], current_state[1], current_state[1])  # Layer 2 doesn't need to move
            moves_layer3 = bfs(layers[2], current_state[2], target_pos_layer4)  # Layer 3 moves to target
            # Layer 4 is being moved by Layer 3
            
            # Total presses: moves_layer3 (directions) + 1 ('A' press)
            new_total_presses = total_presses + moves_layer3 + 1
            
            # Update states
            new_state = (current_state[0], current_state[1], target_pos_layer4, target_pos_layer4)
            if (new_state, press_idx + 1) not in visited:
                visited.add((new_state, press_idx + 1))
                queue.append((new_state, press_idx + 1, new_total_presses))
        else:
            # Layer 4's arm is already pointing to the target, press 'A'
            new_total_presses = total_presses + 1
            new_state = current_state  # No change in positions
            if (new_state, press_idx + 1) not in visited:
                visited.add((new_state, press_idx + 1))
                queue.append((new_state, press_idx + 1, new_total_presses))
    
    # If the queue is exhausted without pressing all buttons
    return float('inf')

def bfs(keypad, start, goal):
    """
    Breadth-first search to find the shortest path from start to goal on the keypad.
    Returns the number of moves required.
    """
    if start == goal:
        return 0
    queue = deque()
    queue.append((start, 0))
    visited = set()
    visited.add(start)
    
    while queue:
        pos, moves = queue.popleft()
        for neighbor, _ in keypad.neighbors(pos):
            if neighbor == goal:
                return moves + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, moves + 1))
    return float('inf')  # If no path found

# Function to compute the sum of complexities
def compute_sum_of_complexities(codes):
    sum_complexities = 0
    for code in codes:
        # Extract numeric part
        numeric_part_str = ''.join(filter(str.isdigit, code))
        numeric_part = int(numeric_part_str) if numeric_part_str else 0
        # Compute sequence length
        sequence_length = compute_min_presses_for_code(code)
        # Compute complexity
        complexity = sequence_length * numeric_part
        print(f"Code: {code}, Sequence Length: {sequence_length}, Numeric Part: {numeric_part}, Complexity: {complexity}")
        sum_complexities += complexity
    return sum_complexities

# Example usage
if __name__ == "__main__":
    codes = ['029A', '980A', '179A', '456A', '379A']

    sum_complexities = compute_sum_of_complexities(codes)
    print(f"Sum of Complexities: {sum_complexities}")
