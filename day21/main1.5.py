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
    Return a list of ALL distinct shortest sequences that type `code` on the numeric keypad.
    BFS with dist dict, collecting all paths that complete the code in the minimal BFS layer.
    """

    initial_state = (start_button, 0)  # (current_button, index_in_code)
    dist = {initial_state: 0}         # dist[state] = BFS distance (length of path)
    queue = deque([(initial_state, "")])
    
    solutions = []
    found_layer_distance = None

    while queue:
        (curr_btn, idx), path = queue[0]  # Look at front
        current_dist = len(path)
        if found_layer_distance is not None and current_dist > found_layer_distance:
            # We already found solutions at a smaller BFS distance, so we can stop
            break

        (curr_btn, idx), path = queue.popleft()

        # If we typed all chars
        if idx == len(code):
            # This path is a valid minimal solution
            solutions.append(path)
            if found_layer_distance is None:
                found_layer_distance = current_dist
            # Do NOT expand from a solution state
            continue

        # If we're exactly at the solution BFS distance, do not expand further
        if found_layer_distance is not None and current_dist == found_layer_distance:
            continue

        # Expand neighbors
        for move_cmd in ['^','v','<','>']:
            neighbor = keypad_adjacency[curr_btn].get(move_cmd)
            if neighbor is not None:
                next_state = (neighbor, idx)
                new_path = path + move_cmd
                new_dist = len(new_path)
                
                old_dist = dist.get(next_state, None)
                if old_dist is None or new_dist < old_dist:
                    dist[next_state] = new_dist
                    queue.append((next_state, new_path))
                elif old_dist is not None and new_dist == old_dist:
                    # Another distinct path to same state at same BFS distance
                    queue.append((next_state, new_path))

        # Try pressing 'A' if curr_btn matches next needed char
        needed_char = code[idx]
        if curr_btn == needed_char:
            next_state = (curr_btn, idx+1)
            new_path = path + 'A'
            new_dist = len(new_path)
            old_dist = dist.get(next_state, None)
            if old_dist is None or new_dist < old_dist:
                dist[next_state] = new_dist
                queue.append((next_state, new_path))
            elif old_dist is not None and new_dist == old_dist:
                queue.append((next_state, new_path))

    return solutions


def bfs_type_string_on_directional_keypad_all_min_solutions(target_string, keypad_adjacency, start_button='A'):
    """
    Return a list of ALL distinct shortest sequences that produce `target_string`
    on the directional keypad.
    """

    initial_state = (start_button, 0)  # (button_aimed_at, index_in_target_string)
    dist = {initial_state: 0}
    queue = deque([(initial_state, "")])

    solutions = []
    found_layer_distance = None

    while queue:
        (curr_btn, idx), path = queue[0]
        current_dist = len(path)
        if found_layer_distance is not None and current_dist > found_layer_distance:
            break

        (curr_btn, idx), path = queue.popleft()

        # If we've produced the entire string
        if idx == len(target_string):
            solutions.append(path)
            if found_layer_distance is None:
                found_layer_distance = current_dist
            continue

        if found_layer_distance is not None and current_dist == found_layer_distance:
            continue

        # Move commands
        for move_cmd in ['^','v','<','>']:
            neighbor = keypad_adjacency[curr_btn].get(move_cmd)
            if neighbor is not None:
                next_state = (neighbor, idx)
                new_path = path + move_cmd
                new_dist = len(new_path)

                old_dist = dist.get(next_state, None)
                if old_dist is None or new_dist < old_dist:
                    dist[next_state] = new_dist
                    queue.append((next_state, new_path))
                elif old_dist is not None and new_dist == old_dist:
                    queue.append((next_state, new_path))

        # Press 'A' if needed
        needed_char = target_string[idx]
        if curr_btn == needed_char:
            next_state = (curr_btn, idx+1)
            new_path = path + 'A'
            new_dist = len(new_path)

            old_dist = dist.get(next_state, None)
            if old_dist is None or new_dist < old_dist:
                dist[next_state] = new_dist
                queue.append((next_state, new_path))
            elif old_dist is not None and new_dist == old_dist:
                queue.append((next_state, new_path))

    return solutions



def produce_all_minimal_L3_for_code(code):
    """
    1) All minimal L1 solutions using numeric BFS
    2) For each L1 solution, all minimal L2 solutions using directional BFS
    3) For each L2 solution, all minimal L3 solutions using directional BFS
    4) Return all truly minimal L3 sequences
    """
    # Step 1: All minimal L1
    L1_solutions = bfs_type_on_numeric_keypad_all_min_solutions(
        code, numeric_keypad_adjacency, start_button='A'
    )
    if not L1_solutions:
        return []

    # Step 2: For each L1, gather minimal L2
    all_L2 = []
    for sol in L1_solutions:
        subL2 = bfs_type_string_on_directional_keypad_all_min_solutions(
            sol, directional_keypad_adjacency, start_button='A'
        )
        all_L2.extend(subL2)
    if not all_L2:
        return []

    # Step 3: For each L2, gather minimal L3
    all_L3 = []
    for sol2 in all_L2:
        subL3 = bfs_type_string_on_directional_keypad_all_min_solutions(
            sol2, directional_keypad_adjacency, start_button='A'
        )
        all_L3.extend(subL3)
    if not all_L3:
        return []

    # Among them, pick only those with minimal length
    min_len = min(len(x) for x in all_L3)
    best = [x for x in all_L3 if len(x) == min_len]
    return best



def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')

    codes = read_codes(file_path)
    print("Codes to type:", codes)

    total_complexity = 0
    for code in codes:
        all_L3 = produce_all_minimal_L3_for_code(code)
        if not all_L3:
            print(f"No solutions for {code}?!")
            continue

        # All L3 solutions in all_L3 are minimal length, but might differ. 
        # Pick lexicographically smallest, or just pick the first:
        final_seq = min(all_L3, key=lambda s: s)
        final_len = len(final_seq)
        numeric_part = int(code[:-1])  # e.g. "029A" -> "029" -> 29

        comp = final_len * numeric_part
        total_complexity += comp

        print(f"Code: {code}, minimal L3 length={final_len}, complexity={comp}")
        print("  Example minimal L3 seq:", final_seq)

    print("Total complexity =", total_complexity)

if __name__ == "__main__": main()
