import os
from collections import deque
import sys

def read_codes(file_path):
    """Reads codes from a file, each code on a separate line."""
    codes = []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.strip()
            if row:
                codes.append(row)
    return codes

# Define the numeric keypad adjacency
numeric_keypad_adjacency = {
    '7': {'^': None, 'v': '4', '<': None, '>': '8'},
    '8': {'^': None, 'v': '5', '<': '7', '>': '9'},
    '9': {'^': None, 'v': '6', '<': '8', '>': None},
    '4': {'^': '7', 'v': '1', '<': None, '>': '5'},
    '5': {'^': '8', 'v': '2', '<': '4', '>': '6'},
    '6': {'^': '9', 'v': '3', '<': '5', '>': None},
    '1': {'^': '4', 'v': None, '<': None, '>': '2'},
    '2': {'^': '5', 'v': None, '<': '1', '>': '3'},
    '3': {'^': '6', 'v': 'A', '<': '2', '>': None},
    '0': {'^': '2', 'v': None, '<': None, '>': 'A'},
    'A': {'^': '3', 'v': None, '<': '0', '>': None}
}

# Define the directional keypad adjacency
directional_keypad_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None}
}

def bfs_type_on_numeric_keypad_all_min_solutions(code, keypad_adjacency, start_button='A'):
    """
    Returns a list of ALL shortest sequences that type the given `code` on the numeric keypad.
    Each sequence consists of '^', 'v', '<', '>', and 'A' characters.
    """
    initial_state = (start_button, 0)  # (current_button, index_in_code)
    queue = deque()
    queue.append((initial_state, ""))
    visited = set()
    visited.add(initial_state)
    solutions = []
    found = False

    while queue and not found:
        level_size = len(queue)
        level_solutions = []
        for _ in range(level_size):
            (curr_btn, idx), path = queue.popleft()

            if idx == len(code):
                level_solutions.append(path)
                found = True
                continue  # Do not expand further from this state

            # Move commands
            for move_cmd in ['^','v','<','>']:
                neighbor = keypad_adjacency[curr_btn].get(move_cmd)
                if neighbor is not None:
                    next_state = (neighbor, idx)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, path + move_cmd))

            # Press 'A' if the current button matches the needed character
            needed_char = code[idx]
            if curr_btn == needed_char:
                next_state = (curr_btn, idx + 1)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + 'A'))

        if level_solutions:
            solutions.extend(level_solutions)
            break  # Found all minimal solutions at this BFS depth

    return solutions

def bfs_type_string_on_directional_keypad_all_min_solutions(target_string, keypad_adjacency, start_button='A'):
    """
    Returns a list of ALL shortest sequences that produce the `target_string` on the directional keypad.
    Each sequence consists of '^', 'v', '<', '>', and 'A' characters.
    """
    initial_state = (start_button, 0)  # (current_button, index_in_target_string)
    queue = deque()
    queue.append((initial_state, ""))
    visited = set()
    visited.add(initial_state)
    solutions = []
    found = False

    while queue and not found:
        level_size = len(queue)
        level_solutions = []
        for _ in range(level_size):
            (curr_btn, idx), path = queue.popleft()

            if idx == len(target_string):
                level_solutions.append(path)
                found = True
                continue  # Do not expand further from this state

            # Move commands
            for move_cmd in ['^','v','<','>']:
                neighbor = keypad_adjacency[curr_btn].get(move_cmd)
                if neighbor is not None:
                    next_state = (neighbor, idx)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, path + move_cmd))

            # Press 'A' if the current button matches the needed character
            needed_char = target_string[idx]
            if curr_btn == needed_char:
                next_state = (curr_btn, idx + 1)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + 'A'))

        if level_solutions:
            solutions.extend(level_solutions)
            break  # Found all minimal solutions at this BFS depth

    return solutions

def produce_all_minimal_L3_for_code(code):
    """
    For a given code, produce all minimal L3 sequences by:
    1. Finding all minimal L1 sequences on the numeric keypad.
    2. For each L1 sequence, finding all minimal L2 sequences on the directional keypad.
    3. For each L2 sequence, finding all minimal L3 sequences on the directional keypad.
    4. Collect all L3 sequences and return those with the minimal length.
    """
    # Step 1: All minimal L1 solutions (numeric keypad)
    L1_solutions = bfs_type_on_numeric_keypad_all_min_solutions(
        code, numeric_keypad_adjacency, start_button='A'
    )
    if not L1_solutions:
        print(f"No L1 solutions found for code: {code}")
        return []

    # Step 2: All minimal L2 solutions for each L1 solution
    all_L2_solutions = []
    for l1_seq in L1_solutions:
        L2_solutions = bfs_type_string_on_directional_keypad_all_min_solutions(
            l1_seq, directional_keypad_adjacency, start_button='A'
        )
        if not L2_solutions:
            print(f"No L2 solutions found for L1 sequence: {l1_seq}")
            continue
        all_L2_solutions.extend(L2_solutions)

    if not all_L2_solutions:
        print(f"No L2 solutions found for code: {code}")
        return []

    # Step 3: All minimal L3 solutions for each L2 solution
    all_L3_solutions = []
    for l2_seq in all_L2_solutions:
        L3_solutions = bfs_type_string_on_directional_keypad_all_min_solutions(
            l2_seq, directional_keypad_adjacency, start_button='A'
        )
        if not L3_solutions:
            print(f"No L3 solutions found for L2 sequence: {l2_seq}")
            continue
        all_L3_solutions.extend(L3_solutions)

    if not all_L3_solutions:
        print(f"No L3 solutions found for code: {code}")
        return []

    # Step 4: Find the minimal length among all L3 solutions
    min_len = min(len(seq) for seq in all_L3_solutions)
    best_L3_solutions = [seq for seq in all_L3_solutions if len(seq) == min_len]

    return best_L3_solutions

def complexity(code, sequence):
    """
    Calculates the complexity of a code based on the sequence length and numeric part.
    """
    numeric_part = int(code[:-1])  # Remove the trailing 'A'
    return numeric_part * len(sequence)

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    # Adjust the filename as needed
    file_path = os.path.join(directory, 'input.txt')  # Replace 'input.txt' with your actual input file
    file_path = os.path.join(directory, 'input2.txt')  # Replace 'input.txt' with your actual input file

    # Read codes from the input file
    codes = read_codes(file_path)
    print("Codes to type:", codes)
    print()

    total_complexity = 0
    for code in codes:
        print(f"Processing Code: {code}")
        # Produce all minimal L3 sequences for the code
        all_L3 = produce_all_minimal_L3_for_code(code)
        if not all_L3:
            print(f"  No valid sequences found for code: {code}")
            continue

        # Find the minimal length among all L3 sequences
        min_length = min(len(seq) for seq in all_L3)
        # Collect all sequences that have this minimal length
        minimal_L3_sequences = [seq for seq in all_L3 if len(seq) == min_length]

        # For debugging, you can print all minimal sequences
        # print(f"  Minimal L3 sequences (length={min_length}):")
        # for seq in minimal_L3_sequences:
        #     print(f"    {seq}")

        # Select one minimal sequence (e.g., the first one)
        chosen_L3 = minimal_L3_sequences[0]
        comp = complexity(code, chosen_L3)
        total_complexity += comp

        print(f"  Minimal L3 length = {min_length}, Complexity = {comp}")
        print(f"  Example minimal L3 sequence: {chosen_L3}")
        print()

    print(f"Total complexity = {total_complexity}")

if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()
