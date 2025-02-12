#!/usr/bin/env python3

import sys
from collections import deque

#
# Numeric keypad adjacency (layer #1)
# If adjacency[x][move] = None, that means it’s a gap => panic => skip
#
numeric_adjacency = {
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
    'A': {'^': '3', 'v': None, '<': '0', '>': None},
}

#
# Directional keypad adjacency (layer #2 and #3)
# The puzzle says the directional keypad is 2 rows:
#   top:    [gap,  '^', 'A']
#   bottom: ['<',  'v', '>']
#
directional_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None},
}


def single_bfs(code):
    """
    Single BFS over 3 layers:
      - topmost: your keypad (layer #3, directional)
      - middle:  layer #2, directional
      - bottom:  layer #1, numeric

    State = (pos3, pos2, pos1, typed_count)

    typed_count goes from 0 .. len(code).

    We'll find all minimal solutions that finish typed_count == len(code).
    Return (min_dist, list_of_solutions) where each solution is the sequence of '^','v','<','>','A' that *you* press at layer #3.
    """

    # All arms initially at 'A'
    start_pos3 = 'A'
    start_pos2 = 'A'
    start_pos1 = 'A'
    start_typed = 0

    start_state = (start_pos3, start_pos2, start_pos1, start_typed)
    dist = {start_state: 0}
    paths = {start_state: [""]}  # store *all* minimal path strings for each state

    queue = deque([start_state])
    solutions = []
    found_dist = None

    while queue:
        state = queue.popleft()
        (pos3, pos2, pos1, typed_so_far) = state
        d = dist[state]

        # If we've discovered solutions at BFS layer 'found_dist', skip deeper
        if found_dist is not None and d > found_dist:
            continue

        # If code is fully typed
        if typed_so_far == len(code):
            # all paths for this state are minimal
            solutions.extend(paths[state])
            if found_dist is None:
                found_dist = d
            continue

        # Expand all possible top-level presses '^','v','<','>','A'
        for press3 in ['<','^','v','>','A']:
            new_pos3 = pos3
            new_pos2 = pos2
            new_pos1 = pos1
            new_typed = typed_so_far

            # If press3 is a move on layer#3
            if press3 in ['^','v','<','>']:
                nxt3 = directional_adjacency[pos3].get(press3)
                if nxt3 is None:
                    # gap => skip
                    continue
                new_pos3 = nxt3
            else:
                # press3 == 'A' => we "activate" the button pos3 => exactly one press on layer#2
                press2 = pos3
                if press2 in ['^','v','<','>']:
                    nxt2 = directional_adjacency[pos2].get(press2)
                    if nxt2 is None:
                        continue
                    new_pos2 = nxt2
                else:
                    # press2 == 'A' => "activate" pos2 => exactly one press on layer#1 (numeric)
                    press1 = pos2
                    if press1 in ['^','v','<','>']:
                        nxt1 = numeric_adjacency[pos1].get(press1)
                        if nxt1 is None:
                            continue
                        new_pos1 = nxt1
                    else:
                        # press1 == 'A' => type a character on numeric layer
                        # we succeed if pos1 == code[new_typed]
                        if pos1 == code[new_typed]:
                            new_typed += 1
                        else:
                            # mismatch => skip
                            continue

            new_state = (new_pos3, new_pos2, new_pos1, new_typed)
            nd = d + 1

            if new_state not in dist:
                dist[new_state] = nd
                paths[new_state] = []
                for oldp in paths[state]:
                    paths[new_state].append(oldp + press3)
                queue.append(new_state)
            elif dist[new_state] == nd:
                # Another equally minimal approach => append these solutions
                for oldp in paths[state]:
                    paths[new_state].append(oldp + press3)

    if not solutions:
        return None, []
    return found_dist, solutions


def numeric_part(code_str):
    """
    code_str like '029A' => numeric_part = 29
    """
    return int(code_str[:-1])


def main():
    codes = ["029A", "980A", "179A", "456A", "379A"]

    total = 0
    for c in codes:
        dist_val, sols = single_bfs(c)
        if dist_val is None:
            print(f"No solution found for code {c}!")
            continue

        # Among all minimal solutions, pick the shortest length in 'sols' (should all be dist_val anyway).
        # The BFS ensures every final solution in 'sols' has length = dist_val.
        # But let's just confirm:
        lens = [len(s) for s in sols]
        min_len = min(lens)
        # We'll pick the first minimal-len solution as an example:
        example_sol = next(s for s in sols if len(s) == min_len)

        # Complexity = numeric_part * min_len
        comp = numeric_part(c) * min_len
        total += comp

        print(f"Code {c} => minimal length = {min_len}, complexity = {comp}")
        print(f"   Example minimal solution = {example_sol}\n")

    print(f"Total complexity of all codes = {total}")


if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()
