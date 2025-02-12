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
    Returns a list of ALL shortest sequences that type the given `code` on the numeric keypad.
    Using BFS with a dist dict so we allow multiple same-length ways to each state.
    """

    # A 'state' is (button_aimed, index_in_code)
    # 'path' is the sequence of '^','v','<','>','A' typed so far
    initial_state = (start_button, 0)

    # dist[state] = the BFS-layer or distance (length of path) at which we discovered 'state'
    dist = {}
    dist[initial_state] = 0

    # We'll store the queue of (state, path_so_far). 
    # 'distance' is implicitly len(path_so_far).
    queue = deque()
    queue.append((initial_state, ""))

    # So that we can do a layered BFS, we track if we found any solutions at this distance.
    solutions = []
    found_distance = None  # the BFS distance at which we first find a solution

    while queue:
        (current_button, idx), path = queue[0]  # peek at front
        current_dist = len(path)  # BFS distance for the front item

        # If we already found solutions at distance found_distance
        # and the current item is at a bigger distance => we can break
        if found_distance is not None and current_dist > found_distance:
            break

        (current_button, idx), path = queue.popleft()

        # If we've typed the entire code
        if idx == len(code):
            # Record this path as a valid shortest solution
            solutions.append(path)
            if found_distance is None:
                found_distance = current_dist
            # We continue popping from the queue as long as items have distance == found_distance
            # but do NOT expand further from here.
            continue

        # Expand neighbors only if we haven't found solutions or we are still at the same BFS distance
        if found_distance is not None and current_dist == found_distance:
            # We are currently in the solution layer. We do NOT expand further BFS from solutions.
            continue

        # Try movements '^','v','<','>'
        for move_cmd in ['^','v','<','>']:
            neighbor = keypad_adjacency[current_button].get(move_cmd)
            if neighbor is not None:
                next_state = (neighbor, idx)
                new_path = path + move_cmd
                new_dist = len(new_path)
                
                # If we haven't visited next_state, or we found a new same-distance path
                # to next_state, we push it in queue
                if next_state not in dist or new_dist < dist[next_state]:
                    dist[next_state] = new_dist
                    queue.append((next_state, new_path))
                elif next_state in dist and new_dist == dist[next_state]:
                    # same BFS distance => it's a distinct minimal path
                    queue.append((next_state, new_path))

        # Try pressing 'A' if current_button == the next needed char
        needed_char = code[idx]
        if current_button == needed_char:
            next_state = (current_button, idx + 1)
            new_path = path + 'A'
            new_dist = len(new_path)

            if next_state not in dist or new_dist < dist[next_state]:
                dist[next_state] = new_dist
                queue.append((next_state, new_path))
            elif next_state in dist and new_dist == dist[next_state]:
                queue.append((next_state, new_path))

    return solutions

def bfs_type_string_on_directional_keypad_all_min_solutions(target_string, keypad_adjacency, start_button='A'):
    """
    Returns a list of ALL shortest sequences of '^','v','<','>','A' 
    that produce `target_string`. 
    Also uses a dist dict so we can find multiple same-length solutions to the same state.
    """

    from collections import deque

    # state = (button_aimed, index_in_target_string)
    initial_state = (start_button, 0)
    dist = {}
    dist[initial_state] = 0

    queue = deque()
    queue.append((initial_state, ""))

    solutions = []
    found_distance = None

    while queue:
        (current_button, idx), path = queue[0]
        current_dist = len(path)
        if found_distance is not None and current_dist > found_distance:
            break

        (current_button, idx), path = queue.popleft()

        # If idx == len(target_string), we typed everything
        if idx == len(target_string):
            solutions.append(path)
            if found_distance is None:
                found_distance = current_dist
            continue

        if found_distance is not None and current_dist == found_distance:
            # we won't expand from complete solutions
            continue

        # 1) Move commands
        for move_cmd in ['^','v','<','>']:
            neighbor = keypad_adjacency[current_button].get(move_cmd)
            if neighbor is not None:
                next_state = (neighbor, idx)
                new_path = path + move_cmd
                new_dist = len(new_path)
                if next_state not in dist or new_dist < dist[next_state]:
                    dist[next_state] = new_dist
                    queue.append((next_state, new_path))
                elif next_state in dist and new_dist == dist[next_state]:
                    queue.append((next_state, new_path))

        # 2) Press 'A' if needed
        needed_char = target_string[idx]
        if current_button == needed_char:
            next_state = (current_button, idx+1)
            new_path = path + 'A'
            new_dist = len(new_path)
            if next_state not in dist or new_dist < dist[next_state]:
                dist[next_state] = new_dist
                queue.append((next_state, new_path))
            elif next_state in dist and new_dist == dist[next_state]:
                queue.append((next_state, new_path))

    return solutions


def produce_all_minimal_L3_for_code(code):
    # 1) All minimal L1 solutions (typing `code` on numeric keypad)
    L1_solutions = bfs_type_on_numeric_keypad_all_min_solutions(
        code, numeric_keypad_adjacency, start_button='A'
    )
    if not L1_solutions:
        return []

    # 2) For each L1 solution, gather all minimal L2 solutions
    all_L2_solutions = []
    for seq_l1 in L1_solutions:
        sub_l2 = bfs_type_string_on_directional_keypad_all_min_solutions(
            seq_l1, directional_keypad_adjacency, start_button='A'
        )
        all_L2_solutions.extend(sub_l2)

    if not all_L2_solutions:
        return []

    # 3) For each L2 solution, gather all minimal L3 solutions
    all_L3_solutions = []
    for seq_l2 in all_L2_solutions:
        sub_l3 = bfs_type_string_on_directional_keypad_all_min_solutions(
            seq_l2, directional_keypad_adjacency, start_button='A'
        )
        all_L3_solutions.extend(sub_l3)

    if not all_L3_solutions:
        return []

    # among all L3 solutions, pick the truly minimal length
    min_len = min(len(s) for s in all_L3_solutions)
    best_L3_solutions = [s for s in all_L3_solutions if len(s) == min_len]
    return best_L3_solutions


def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, "input.txt")
    file_path = os.path.join(directory, "input2.txt")

    codes = read_codes(file_path)
    print("Codes to type:", codes)

    total_complexity = 0
    for code in codes:
        print(f"Code: {code}")
        possible_L3 = produce_all_minimal_L3_for_code(code)
        if not possible_L3:
            print("No solutions found for code:", code)
            continue

        # all solutions in possible_L3 have the same length => pick any, or pick min lexicographically:
        final_seq = min(possible_L3, key=lambda x: x)  # pick lexicographically smallest
        final_len = len(final_seq)

        numeric_part = int(code[:-1])  # e.g. "029A" -> "029" -> 29
        comp = final_len * numeric_part
        total_complexity += comp

        print(f"Code: {code}, minimal L3 length={final_len}, complexity={comp}")
        print("  Example minimal L3 seq:", final_seq)

    print("Total complexity =", total_complexity)



if __name__ == "__main__": main()
