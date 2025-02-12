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

def bfs_all_min_sequences(start_button, target_string, keypad_adjacency):
    """
    General BFS to find all minimal sequences that produce the target_string on the keypad.
    :param start_button: Starting button ('A' by default)
    :param target_string: String to produce (e.g., "029A")
    :param keypad_adjacency: Adjacency dict for the keypad
    :return: List of all minimal sequences
    """
    initial_state = (start_button, 0)  # (current_button, index_in_target)
    queue = deque()
    queue.append((initial_state, ""))
    dist = {initial_state: 0}
    solutions = []
    found_distance = None

    while queue:
        (curr_btn, idx), path = queue[0]  # Peek front
        current_dist = len(path)

        # If solutions have been found at a certain distance and current_dist exceeds it, stop
        #if found_distance is not None and current_dist > found_distance:
        #    break

        (curr_btn, idx), path = queue.popleft()

        # If the target string has been fully produced
        if idx == len(target_string):
            solutions.append(path)
            if found_distance is None:
                found_distance = current_dist
            continue  # Do not expand further from this state

        # If we've found solutions and are at the same distance, continue to collect
        if found_distance is not None and current_dist == found_distance:
            continue  # Do not expand further from this state

        # Expand all possible moves: '^', 'v', '<', '>'
        for move_cmd in ['<', '^', 'v', '>']:
            neighbor = keypad_adjacency[curr_btn].get(move_cmd)
            if neighbor is not None:
                next_state = (neighbor, idx)
                new_path = path + move_cmd
                new_dist = len(new_path)

                if next_state not in dist or new_dist < dist[next_state]:
                    dist[next_state] = new_dist
                    queue.append((next_state, new_path))
                elif new_dist == dist[next_state]:
                    queue.append((next_state, new_path))  # Another minimal path

        # Attempt to press 'A' if the current button matches the next character to type
        if idx < len(target_string) and curr_btn == target_string[idx]:
            next_state = (curr_btn, idx + 1)
            new_path = path + 'A'
            new_dist = len(new_path)

            if next_state not in dist or new_dist < dist[next_state]:
                dist[next_state] = new_dist
                queue.append((next_state, new_path))
            elif new_dist == dist[next_state]:
                queue.append((next_state, new_path))  # Another minimal path

    return solutions

def produce_all_minimal_L3_for_code(code):
    """
    For a given code, produce all minimal L3 sequences by:
    1. Finding all minimal L1 sequences on the numeric keypad.
    2. For each L1 sequence, finding all minimal L2 sequences on the first directional keypad.
    3. For each L2 sequence, finding all minimal L3 sequences on the second directional keypad.
    4. Collect all L3 sequences and return those with the minimal length.
    """
    # Step 1: All minimal L1 solutions (typing the code on numeric keypad)
    L1_solutions = bfs_all_min_sequences(
        start_button='A',
        target_string=code,
        keypad_adjacency=numeric_keypad_adjacency
    )
    if not L1_solutions:
        print(f"  No L1 solutions found for code: {code}")
        return []

    # Step 2: All minimal L2 solutions (typing L1 sequence on first directional keypad)
    all_L2_solutions = []
    for l1_seq in L1_solutions:
        L2_solutions = bfs_all_min_sequences(
            start_button='A',
            target_string=l1_seq,
            keypad_adjacency=directional_keypad_adjacency
        )
        if not L2_solutions:
            print(f"    No L2 solutions found for L1 sequence: {l1_seq}")
            continue
        all_L2_solutions.extend(L2_solutions)

    if not all_L2_solutions:
        print(f"  No L2 solutions found for code: {code}")
        return []

    # Step 3: All minimal L3 solutions (typing L2 sequence on second directional keypad)
    all_L3_solutions = []
    for l2_seq in all_L2_solutions:
        L3_solutions = bfs_all_min_sequences(
            start_button='A',
            target_string=l2_seq,
            keypad_adjacency=directional_keypad_adjacency
        )
        if not L3_solutions:
            print(f"    No L3 solutions found for L2 sequence: {l2_seq}")
            continue
        all_L3_solutions.extend(L3_solutions)

    if not all_L3_solutions:
        print(f"  No L3 solutions found for code: {code}")
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
    # Replace 'input.txt' with your actual input file if different
    file_path = os.path.join(directory, 'input.txt')  
    #file_path = os.path.join(directory, 'input2.txt')  

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

        # Find the minimal length among all L3 solutions
        min_length = min(len(seq) for seq in all_L3)
        best_L3_solutions = [seq for seq in all_L3 if len(seq) == min_length]

        print(f"  Found {len(best_L3_solutions)} minimal L3 solutions with length {min_length}:")
        # Uncomment the following lines to see all minimal sequences
        # for seq in best_L3_solutions:
        #     print(f"    L3_seq: {seq}")

        # Select one minimal sequence (e.g., the first one)
        chosen_L3 = best_L3_solutions[0]
        comp = complexity(code, chosen_L3)
        total_complexity += comp

        print(f"  Minimal L3 length = {min_length}, Complexity = {comp}")
        print(f"  Example minimal L3 sequence: {chosen_L3}")
        print()

    print(f"Total complexity = {total_complexity}")

if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()
