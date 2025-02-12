import os
from collections import deque
import sys
import heapq
from functools import lru_cache

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

# Precompute all possible button positions for both keypads
all_keypads = {
    'numeric': numeric_keypad_adjacency,
    'directional': directional_keypad_adjacency
}

def get_adjacency(keypad_type):
    """Returns the adjacency mapping based on keypad type."""
    return all_keypads[keypad_type]

@lru_cache(maxsize=None)
def a_star_search(start_button, target_string, keypad_type):
    """
    A* search to find the minimal sequence to produce the target_string on the keypad.
    :param start_button: Starting button (e.g., 'A')
    :param target_string: String to produce (e.g., "029A")
    :param keypad_type: 'numeric' or 'directional'
    :return: List of all minimal sequences
    """
    adjacency = get_adjacency(keypad_type)
    
    # Heuristic function: number of remaining characters
    def heuristic(idx):
        return len(target_string) - idx

    # Priority queue: (estimated_total_cost, current_cost, current_button, idx, path)
    heap = []
    heapq.heappush(heap, (heuristic(0), 0, start_button, 0, ""))

    # To store the minimal sequences
    solutions = []
    found_cost = None

    # Visited states: (current_button, idx) -> cost
    visited = {}

    while heap:
        est_total, current_cost, current_btn, idx, path = heapq.heappop(heap)

        # If we've already found a better path to this state, skip
        if (current_btn, idx) in visited and visited[(current_btn, idx)] < current_cost:
            continue

        # If target is complete
        if idx == len(target_string):
            if found_cost is None:
                found_cost = current_cost
            if current_cost == found_cost:
                solutions.append(path)
            continue

        # If a solution has been found and current_cost exceeds, stop
        if found_cost is not None and current_cost > found_cost:
            break

        # Move commands in priority order: '<', '^', 'v', '>'
        for move_cmd in ['<', '^', 'v', '>']:
            neighbor = adjacency[current_btn].get(move_cmd)
            if neighbor is not None:
                next_state = (neighbor, idx)
                new_path = path + move_cmd
                new_cost = current_cost + 1
                est = new_cost + heuristic(idx)
                if (neighbor, idx) not in visited or new_cost < visited[(neighbor, idx)]:
                    visited[(neighbor, idx)] = new_cost
                    heapq.heappush(heap, (est, new_cost, neighbor, idx, new_path))

        # Attempt to press 'A' if the current button matches the next character to type
        if idx < len(target_string) and current_btn == target_string[idx]:
            next_state = (current_btn, idx + 1)
            new_path = path + 'A'
            new_cost = current_cost + 1
            est = new_cost + heuristic(idx + 1)
            if (current_btn, idx + 1) not in visited or new_cost < visited[(current_btn, idx + 1)]:
                visited[(current_btn, idx + 1)] = new_cost
                heapq.heappush(heap, (est, new_cost, current_btn, idx + 1, new_path))

    return solutions

def produce_all_minimal_sequences(code):
    """
    For a given code, produce all minimal sequences by:
    1. Typing the code on the numeric keypad.
    2. Typing the L1 sequence on the first directional keypad.
    3. Typing the L2 sequence on the second directional keypad.
    :param code: The code string (e.g., "029A")
    :return: List of minimal L3 sequences
    """
    # Step 1: Find all minimal L1 sequences (typing the code on the numeric keypad)
    L1_solutions = a_star_search('A', code, 'numeric')
    if not L1_solutions:
        print(f"No L1 solutions found for code: {code}")
        return []

    # Step 2: Find all minimal L2 sequences (typing L1 sequences on the first directional keypad)
    all_L2_solutions = set()
    for l1_seq in L1_solutions:
        L2_solutions = a_star_search('A', l1_seq, 'directional')
        if not L2_solutions:
            print(f"No L2 solutions found for L1 sequence: {l1_seq}")
            continue
        all_L2_solutions.update(L2_solutions)

    if not all_L2_solutions:
        print(f"No L2 solutions found for code: {code}")
        return []

    # Step 3: Find all minimal L3 sequences (typing L2 sequences on the second directional keypad)
    all_L3_solutions = set()
    for l2_seq in all_L2_solutions:
        L3_solutions = a_star_search('A', l2_seq, 'directional')
        if not L3_solutions:
            print(f"No L3 solutions found for L2 sequence: {l2_seq}")
            continue
        all_L3_solutions.update(L3_solutions)

    if not all_L3_solutions:
        print(f"No L3 solutions found for code: {code}")
        return []

    # Step 4: Determine the minimal length among all L3 solutions
    min_length = min(len(seq) for seq in all_L3_solutions)
    best_L3_solutions = [seq for seq in all_L3_solutions if len(seq) == min_length]

    return best_L3_solutions

def complexity(code, sequence):
    """
    Calculates the complexity of a code based on the sequence length and numeric part.
    """
    numeric_part = int(code.rstrip('A'))  # Remove the trailing 'A'
    return numeric_part * len(sequence)

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    # Replace 'input.txt' with your actual input file if different
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')

    # Read codes from the input file
    codes = read_codes(file_path)
    print("Codes to type:", codes)
    print()

    total_complexity = 0
    for code in codes:
        print(f"Processing Code: {code}")
        # Produce all minimal L3 sequences for the code
        all_L3 = produce_all_minimal_sequences(code)
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
