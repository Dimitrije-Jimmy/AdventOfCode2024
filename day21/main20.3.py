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

from collections import deque

def bfs_all_min_sequences(
    start_button: str,
    target_string: str,
    keypad_adjacency: dict
):
    """
    Returns a list of ALL minimal sequences of '^', 'v', '<', '>', 'A' needed
    so that starting at 'start_button', we produce the entire target_string
    (by pressing 'A' when aimed at the correct character).
    
    :param start_button: The button we're initially pointing at (e.g. 'A').
    :param target_string: The string we want to produce (e.g. "029A").
    :param keypad_adjacency: A dict mapping button -> {move_cmd -> neighbor_button}.
    :return: List of all minimal sequences (strings).
    """

    # Each state is (current_button, how_many_characters_of_target_have_been_typed)
    start_state = (start_button, 0)

    # dist[state] = BFS layer index (the length of the path from start -> state)
    dist = {start_state: 0}

    # paths[state] = all minimal‐distance path strings from start -> state
    paths = {start_state: [""]}

    # The queue will hold states in ascending order of distance (typical BFS).
    queue = deque([start_state])

    # We'll collect all solutions in this list once we reach index == len(target_string).
    solutions = []

    # Once we discover solutions at distance d, we only gather solutions at that same d,
    # but do not explore states of distance d+1.  We’ll store that minimal distance here:
    found_solution_distance = None

    while queue:
        state = queue.popleft()
        (current_btn, idx) = state
        current_dist = dist[state]

        # If we've already found solutions at some BFS depth,
        # and our current state is deeper, skip it entirely.
        if found_solution_distance is not None and current_dist > found_solution_distance:
            continue

        # If this state is already "done" (we typed the entire string),
        # we gather those solutions into `solutions` and do NOT expand further.
        if idx == len(target_string):
            # All paths that got here are already minimal (because BFS).
            solutions.extend(paths[state])
            # Mark the BFS distance if we haven't.
            if found_solution_distance is None:
                found_solution_distance = current_dist
            # Do not expand this state further.
            continue

        # Otherwise, expand neighbors.

        # 1) Try moving the arm: '^', 'v', '<', '>' if valid neighbor
        for move_cmd in ['<', '^', 'v', '>']:
            neighbor_btn = keypad_adjacency[current_btn].get(move_cmd)
            if neighbor_btn is None:
                continue  # The adjacency says we can't go in that direction

            neighbor_state = (neighbor_btn, idx)
            next_dist = current_dist + 1

            # If we've never visited neighbor_state, or we found another
            # minimal path of the same distance, record it.
            if neighbor_state not in dist:
                dist[neighbor_state] = next_dist
                paths[neighbor_state] = [
                    path_str + move_cmd for path_str in paths[state]
                ]
                queue.append(neighbor_state)

            elif dist[neighbor_state] == next_dist:
                # We found another equally short way to get there,
                # so we add these new path variants as well.
                for path_str in paths[state]:
                    paths[neighbor_state].append(path_str + move_cmd)

        # 2) Try pressing 'A' — only valid if the current_btn
        #    is the next character in the target string.
        if target_string[idx] == current_btn:
            neighbor_state = (current_btn, idx + 1)
            next_dist = current_dist + 1

            if neighbor_state not in dist:
                dist[neighbor_state] = next_dist
                paths[neighbor_state] = [
                    path_str + 'A' for path_str in paths[state]
                ]
                queue.append(neighbor_state)

            elif dist[neighbor_state] == next_dist:
                for path_str in paths[state]:
                    paths[neighbor_state].append(path_str + 'A')

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
    file_path = os.path.join(directory, 'input.txt')  # Update path to input file
    #file_path = os.path.join(directory, 'input2.txt')  # Update path to input file

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
