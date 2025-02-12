import os
from collections import deque, defaultdict
import math
import sys

def read_codes(file_path):
    codes = []
    with open(file_path, 'r') as f:
        for y, line in enumerate(f):
            row = line.rstrip('\n')
            codes.append(row)
    return codes

numpad = [[7, 8, 8],
          [4, 5, 6],
          [1, 2, 3],
          [None, 0, 'A']]

keypad = [[None, '^', 'A'],
          ['<', 'v', '>']]

directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]

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

directional_keypad_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None}
}

from collections import deque

def bfs_type_on_numeric_keypad_all_min_solutions(code, keypad_adjacency, start_button='A'):
    """
    Returns a list of ALL shortest sequences of ^,v,<,>A to type the given `code` on the numeric keypad.
    """
    # State = (button_aimed, index_in_code)
    initial_state = (start_button, 0)
    visited = set([initial_state])

    # We'll do BFS in layers:
    queue_current = deque()
    queue_next = deque()
    queue_current.append((initial_state, ""))

    found_solutions = []
    solution_found_this_layer = False

    while queue_current and not solution_found_this_layer:
        while queue_current:
            (current_button, code_index), path = queue_current.popleft()

            # If we've typed the entire code, record solution
            if code_index == len(code):
                found_solutions.append(path)
                solution_found_this_layer = True
                continue

            # If we haven't finished code, expand moves in the same BFS layer
            for move_cmd in ['^','v','<','>']:
                neighbor = keypad_adjacency[current_button].get(move_cmd, None)
                if neighbor is not None:
                    next_state = (neighbor, code_index)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue_next.append((next_state, path + move_cmd))

            # Try pressing 'A' if this button matches the next needed character
            needed_char = code[code_index]
            if current_button == needed_char:
                next_state = (current_button, code_index + 1)
                if next_state not in visited:
                    visited.add(next_state)
                    queue_next.append((next_state, path + 'A'))

        # If we found any solutions in this layer, we do NOT proceed to the next layer
        if solution_found_this_layer:
            break

        # Otherwise, continue BFS to the next layer
        queue_current, queue_next = queue_next, queue_current
        queue_next.clear()

    return found_solutions

def bfs_type_string_on_directional_keypad_all_min_solutions(target_string, keypad_adjacency, start_button='A'):
    """
    Returns a list of ALL shortest sequences of '^','v','<','>','A' such that each 'A'
    press produces the next needed character in `target_string`.
    """
    initial_state = (start_button, 0)  # (button_aimed, index_in_target_string)
    visited = set([initial_state])

    queue_current = deque()
    queue_next = deque()
    queue_current.append((initial_state, ""))

    found_solutions = []
    solution_found_this_layer = False

    while queue_current and not solution_found_this_layer:
        while queue_current:
            (current_button, idx), path = queue_current.popleft()

            # If we've produced the entire target_string, record solution
            if idx == len(target_string):
                found_solutions.append(path)
                solution_found_this_layer = True
                continue

            # Explore moves
            for move_cmd in ['^','v','<','>']:
                neighbor = keypad_adjacency[current_button].get(move_cmd, None)
                if neighbor is not None:
                    next_state = (neighbor, idx)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue_next.append((next_state, path + move_cmd))

            # Press 'A' if current_button == the needed char
            needed_char = target_string[idx]
            if current_button == needed_char:
                next_state = (current_button, idx + 1)
                if next_state not in visited:
                    visited.add(next_state)
                    queue_next.append((next_state, path + 'A'))

        if solution_found_this_layer:
            break

        queue_current, queue_next = queue_next, queue_current
        queue_next.clear()

    return found_solutions

def produce_final_sequences_for_code(code):
    """
    Return a list of all possible L3 sequences (at minimal total length),
    by exploring all minimal solutions in L1, L2, and L3 BFS layers.
    """

    # Step 1: L1_solutions = BFS on numeric keypad => all minimal solutions
    L1_solutions = bfs_type_on_numeric_keypad_all_min_solutions(
        code, numeric_keypad_adjacency, start_button='A'
    )
    # For debugging:
    print(f"L1_solutions (count={len(L1_solutions)}):")
    for seq in L1_solutions:
        print("  ", seq)

    all_L2_solutions = []
    # Step 2: For each L1 solution, BFS on directional keypad => all minimal solutions
    for L1_seq in L1_solutions:
        L2_solutions = bfs_type_string_on_directional_keypad_all_min_solutions(
            L1_seq, directional_keypad_adjacency, start_button='A'
        )
        all_L2_solutions.extend(L2_solutions)

    # We might have multiple L2 solutions, each minimal for that L1. But different L1 can yield the same length L2. 
    # Next step:
    all_L3_solutions = []
    for L2_seq in all_L2_solutions:
        L3_solutions = bfs_type_string_on_directional_keypad_all_min_solutions(
            L2_seq, directional_keypad_adjacency, start_button='A'
        )
        all_L3_solutions.extend(L3_solutions)

    # Now all_L3_solutions are minimal for their respective L2. But some might be longer or shorter than others 
    # if different L1 => L2 combos lead to different overall path length. So pick the truly minimal from all_L3_solutions.

    if not all_L3_solutions:
        # Should not happen if the code is valid, but just in case
        return []

    min_len = min(len(seq) for seq in all_L3_solutions)
    best_L3_solutions = [seq for seq in all_L3_solutions if len(seq) == min_len]

    return best_L3_solutions

def main():
    """Main function to execute the solution."""
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')

    codes = read_codes(file_path)
    print("Codes to type:", codes)

    total_complexity = 0
    for code in codes:
        all_l3 = produce_final_sequences_for_code(code)
        if not all_l3:
            print("No solutions for code:", code)
            continue

        # If you want the absolute minimal-l3 in lex order, for instance:
        #   minimal_seq = min(all_l3, key=lambda s: (len(s), s))
        # Otherwise, just pick the first:
        minimal_seq = min(all_l3, key=len)

        # Now compute complexity
        # numeric_part = int(code[:-1]) e.g. code="029A" => code[:-1]="029" => numeric_part=29
        numeric_part = int(code[:-1])  
        comp = numeric_part * len(minimal_seq)
        total_complexity += comp

        print(f"Code: {code}, minimal L3 length = {len(minimal_seq)} => complexity = {comp}")
        print("One minimal L3 seq:", minimal_seq)

    print("Total complexity =", total_complexity)

if __name__ == "__main__": main()
