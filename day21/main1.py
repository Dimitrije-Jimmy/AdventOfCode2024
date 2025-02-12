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

from collections import deque

def bfs_type_on_numeric_keypad(code, keypad_adjacency, start_button='A'):
    """
    Finds the shortest sequence of ^,v,<,>A to type the given `code` on the numeric keypad.
    
    :param code: e.g. "029A"
    :param keypad_adjacency: dict mapping button_label -> { '^': neighbor, 'v': neighbor, ... }
    :param start_button: which button the arm is initially aimed at (usually 'A')
    :return: a string of moves (like "<A^A>^^AvvvA") that types the code.
    """
    # State = (button_aimed, index_in_code)
    # We'll do BFS over this state space, storing the path taken in a queue.

    initial_state = (start_button, 0)  # The arm is on 'A', 0 code chars typed
    visited = set([initial_state])
    queue = deque()
    queue.append((initial_state, ""))  # (state, path_string)

    while queue:
        (current_button, code_index), path = queue.popleft()

        # Check if we've typed the entire code
        if code_index == len(code):
            # We have typed all code characters successfully
            return path

        # 1) Try moving arm (up, down, left, right)
        for move_cmd in ['^','v','<','>']:
            neighbor = keypad_adjacency[current_button].get(move_cmd, None)
            if neighbor is not None:
                # We can move to neighbor
                next_state = (neighbor, code_index)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + move_cmd))
        
        # 2) Try pressing 'A' to type the current button, 
        #    but only if this button matches the next char in `code`
        next_char_needed = code[code_index]
        if current_button == next_char_needed:
            next_state = (current_button, code_index + 1)
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + 'A'))

    # If BFS exhausts without returning, no solution found (shouldn't happen if the code is valid)
    return None

directional_keypad_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None}
}

def bfs_type_string_on_directional_keypad(target_string, keypad_adjacency, start_button='A'):
    """
    Finds the shortest sequence of '^','v','<','>','A' such that pressing 'A'
    will produce each character in `target_string` in order.
    
    :param target_string: e.g. "<A^A>^^AvvvA"
    :param keypad_adjacency: adjacency dict for the directional keypad
    :param start_button: which button the arm is initially aiming at (usually 'A')
    :return: a string of moves (like "v<<A>>^A<A>...") that produces `target_string`.
    """
    from collections import deque

    initial_state = (start_button, 0)  # (aimed_button, index_in_target_string)
    visited = set([initial_state])
    queue = deque()
    queue.append((initial_state, ""))

    while queue:
        (current_button, target_index), path = queue.popleft()

        # If we've produced the entire target_string, success
        if target_index == len(target_string):
            return path

        next_needed_char = target_string[target_index]

        # Try moving arm
        for move_cmd in ['^','v','<','>']:
            neighbor = keypad_adjacency[current_button].get(move_cmd, None)
            if neighbor is not None:
                next_state = (neighbor, target_index)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + move_cmd))

        # Try pressing 'A' if the current button is the needed char
        if current_button == next_needed_char:
            next_state = (current_button, target_index + 1)
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + 'A'))

    return None


def produce_final_sequence_for_code(code):
    print(f"Code: {code}")
    # Step 1: L1_seq = BFS on numeric keypad
    L1_seq = bfs_type_on_numeric_keypad(code, numeric_keypad_adjacency, start_button='A')
    print(f"L1_seq: {L1_seq}")

    # Step 2: L2_seq = BFS on directional keypad to produce L1_seq
    L2_seq = bfs_type_string_on_directional_keypad(L1_seq, directional_keypad_adjacency, start_button='A')
    print(f"L2_seq: {L2_seq}")

    # Step 3: L3_seq = BFS on directional keypad (third layer) to produce L2_seq
    L3_seq = bfs_type_string_on_directional_keypad(L2_seq, directional_keypad_adjacency, start_button='A')
    print(f"L3_seq: {L3_seq}")

    # The string you type yourself is L3_seq
    return L3_seq

def complexity(code, sequence):
    sez = [i.lstrip('0').rstrip('A') for i in code]
    sez_num = int(''.join(sez))
    return sez_num*len(sequence)

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')

    codes = read_codes(file_path)
    print(codes)

    total_complexity = 0
    for c in codes:
        seq = produce_final_sequence_for_code(c)
        # length of the typed sequence
        seq_len = len(seq)
        # numeric part ignoring leading zeros and removing trailing 'A'
        numeric_part = int(c[:-1])  # c[:-1] strips the last 'A', e.g. "029"
        # compute complexity
        comp = seq_len * numeric_part
        total_complexity += comp
    print(total_complexity)

if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()

    # 029A
    """
    <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    <A^A>^^AvvvA
    029A
    L1_seq: <A^A^^>AvvvA
    L2_seq: v<<A>^>A<A>A<AAv>A^Av<AAA^>A
    L3_seq: v<A<AA>^>AvA^<Av>A^Av<<A>^>AvA^Av<<A>^>AAv<A>A^A<A>Av<A<A>^>AAA<Av>A^A
    """

"""
029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A, our result: v<A<AA>^>AvA^<Av>A^Av<<A>^>AvA^Av<<A>^>AAv<A>A^A<A>Av<A<A>^>AAA<Av>A^A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A, our result: v<<A>^>AAAvA^Av<A<AA>^>AvA^<Av>A^Av<A<A>^>AAvA^Av<<A>^>Av<<A>^>AvA^<Av>A^Av<A^>A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A, our result: v<<A>^>Av<A<A>^>AAvA^<Av>A^Av<<A>^>AAvA^Av<A^>AA<A>Av<A<A>^>AAA<Av>A^A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A, our result: v<<A>^>AAv<A<A>^>AAvA^<Av>A^Av<A^>A<A>Av<A^>A<A>Av<A<A>^>AA<Av>A^A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A, our result: v<<A>^>AvA^Av<<A>^>AAv<A<A>^>AAvA^<Av>A^Av<A^>AA<A>Av<A<A>^>AAA<Av>A^A
"""