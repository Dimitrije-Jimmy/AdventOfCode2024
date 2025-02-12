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
    Return a list of ALL shortest sequences that type the given `code` on the numeric keypad.
    BFS will collect all solutions in the first layer that reaches index_in_code == len(code).
    """
    from collections import deque
    
    initial_state = (start_button, 0)  # (button_aimed_at, index_in_code)
    visited = set([initial_state])
    queue_current = deque([(initial_state, "")])
    queue_next = deque()
    
    solutions = []
    found_any = False
    
    while queue_current and not found_any:
        while queue_current:
            (current_button, i), path = queue_current.popleft()
            
            # If we've typed all chars of code, record the solution
            if i == len(code):
                solutions.append(path)
                found_any = True
                continue
            
            # Otherwise, expand neighbors in same BFS layer
            for move_cmd in ['^','v','<','>']:
                neighbor = keypad_adjacency[current_button].get(move_cmd)
                if neighbor is not None:
                    next_state = (neighbor, i)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue_next.append((next_state, path + move_cmd))
            
            # If current_button matches next needed char, try pressing 'A'
            needed_char = code[i]
            if current_button == needed_char:
                next_state = (current_button, i+1)
                if next_state not in visited:
                    visited.add(next_state)
                    queue_next.append((next_state, path + 'A'))
        
        # If we found any solutions in this layer, we do NOT proceed deeper
        if found_any:
            break
        
        # Move to next BFS layer
        queue_current, queue_next = queue_next, queue_current
        queue_next.clear()
    
    return solutions


def bfs_type_string_on_directional_keypad_all_min_solutions(target_string, keypad_adjacency, start_button='A'):
    """
    Return a list of ALL shortest sequences that produce `target_string` on the directional keypad.
    BFS will collect all solutions of the first layer where idx == len(target_string).
    """
    from collections import deque
    
    initial_state = (start_button, 0)  # (button_aimed_at, index_in_target_string)
    visited = set([initial_state])
    queue_current = deque([(initial_state, "")])
    queue_next = deque()
    
    solutions = []
    found_any = False
    
    while queue_current and not found_any:
        while queue_current:
            (current_button, idx), path = queue_current.popleft()
            
            # If we've produced the entire target_string, record solution
            if idx == len(target_string):
                solutions.append(path)
                found_any = True
                continue
            
            # Otherwise, expand neighbors in same BFS layer
            for move_cmd in ['^','v','<','>']:
                neighbor = keypad_adjacency[current_button].get(move_cmd)
                if neighbor is not None:
                    nxt_st = (neighbor, idx)
                    if nxt_st not in visited:
                        visited.add(nxt_st)
                        queue_next.append((nxt_st, path + move_cmd))
            
            # If current_button is the needed char, press 'A'
            needed_char = target_string[idx]
            if current_button == needed_char:
                nxt_st = (current_button, idx+1)
                if nxt_st not in visited:
                    visited.add(nxt_st)
                    queue_next.append((nxt_st, path + 'A'))
        
        # If any solutions found in this BFS layer, stop searching deeper
        if found_any:
            break
        
        queue_current, queue_next = queue_next, queue_current
        queue_next.clear()
    
    return solutions


def produce_all_minimal_L3_for_code(code):
    """
    For the given code (like "029A"), produce *all* minimal L3 sequences by exploring:
      - BFS on numeric keypad (L1)
      - BFS on directional keypad (L2) for each L1
      - BFS on directional keypad (L3) for each L2
    Return a list of all minimal L3 sequences found.
    """
    # 1) L1 BFS => all minimal numeric solutions
    L1_solutions = bfs_type_on_numeric_keypad_all_min_solutions(
        code, numeric_keypad_adjacency, start_button='A'
    )
    if not L1_solutions:
        return []  # No solutions (shouldn't happen if code is valid)
    
    # 2) For each L1 solution, get all minimal L2 solutions
    all_L2_solutions = []
    for l1_seq in L1_solutions:
        L2_solutions = bfs_type_string_on_directional_keypad_all_min_solutions(
            l1_seq, directional_keypad_adjacency, start_button='A'
        )
        all_L2_solutions.extend(L2_solutions)
    
    if not all_L2_solutions:
        return []
    
    # 3) For each L2 solution, get all minimal L3 solutions
    all_L3_solutions = []
    for l2_seq in all_L2_solutions:
        L3_solutions = bfs_type_string_on_directional_keypad_all_min_solutions(
            l2_seq, directional_keypad_adjacency, start_button='A'
        )
        all_L3_solutions.extend(L3_solutions)
    
    if not all_L3_solutions:
        return []
    
    # Among all L3 solutions, we only want those with the truly minimal length
    min_len = min(len(seq) for seq in all_L3_solutions)
    best_L3 = [seq for seq in all_L3_solutions if len(seq) == min_len]
    return best_L3


def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')

    codes = read_codes(file_path)
    print("Codes to type:", codes)

    total_complexity = 0
    for code in codes:
        # produce *all* minimal L3 solutions
        all_min_L3 = produce_all_minimal_L3_for_code(code)
        if not all_min_L3:
            print(f"No solutions found for code {code}?!")
            continue
        
        # All have same length, but if you want a stable pick:
        final_seq = min(all_min_L3, key=lambda x: (len(x), x))
        final_len = len(final_seq)
        
        # numeric portion = int(code[:-1]) e.g. code="029A" => "029" => 29
        numeric_part = int(code[:-1])
        comp = final_len * numeric_part
        total_complexity += comp
        
        print(f"Code: {code}, minimal L3 length={final_len}, complexity={comp}")
        print("  Example minimal L3 sequence:", final_seq)

    print("Total complexity =", total_complexity)


if __name__ == "__main__": main()
