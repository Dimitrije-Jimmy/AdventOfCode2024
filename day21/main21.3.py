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


# Adjacencies for numeric keypad (robot #1):
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

# Adjacencies for directional keypads (robot #2, #3):
directional_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None},
}


def single_bfs_all_minimal(code):
    """
    One BFS to simulate 3 layers:
      - topmost: your keypad (robot #3)  -> pos3
      - middle : the second keypad       -> pos2
      - bottom : numeric keypad         -> pos1
    code is e.g. "980A" that we want to fully type.

    Returns: (min_dist, list_of_all_minimal_sequences),
      where each sequence is the ^,v,<,>,A presses *you* do on robot #3's keypad.
    """

    start_pos3 = 'A'   # top robot's arm starts on 'A'
    start_pos2 = 'A'   # middle robot's arm starts on 'A'
    start_pos1 = 'A'   # bottom (numeric) robot's arm starts on 'A'
    start_typed = 0

    start_state = (start_pos3, start_pos2, start_pos1, start_typed)
    dist = {start_state: 0}
    paths = {start_state: [""]}   # all minimal ways to reach that state

    queue = deque([start_state])
    solutions = []
    found_dist = None

    while queue:
        state = queue.popleft()
        (pos3, pos2, pos1, typed_so_far) = state
        d = dist[state]

        # If we've already found solutions at BFS layer found_dist,
        # skip deeper states
        if found_dist is not None and d > found_dist:
            continue

        # If code is fully typed
        if typed_so_far == len(code):
            # all paths for this state are minimal
            solutions.extend(paths[state])
            if found_dist is None:
                found_dist = d
            continue

        # Expand by pressing one of '^','v','<','>','A' on top keypad
        for press3 in ['^','v','<','>','A']:
            new_pos3 = pos3
            new_pos2 = pos2
            new_pos1 = pos1
            new_typed = typed_so_far

            # 1) If press3 is a move, move pos3
            if press3 in ['^','v','<','>']:
                neighbor3 = directional_adjacency[pos3].get(press3)
                if neighbor3 is None:
                    # Gap => skip
                    continue
                new_pos3 = neighbor3

            else:
                # press3 == 'A' => "activate" the button at pos3 => exactly 1 press on robot #2
                press2 = pos3
                if press2 in ['^','v','<','>']:
                    # move pos2
                    neighbor2 = directional_adjacency[pos2].get(press2)
                    if neighbor2 is None:
                        continue
                    new_pos2 = neighbor2
                else:
                    # press2 == 'A' => "activate" pos2 => exactly 1 press on numeric keypad
                    press1 = pos2
                    if press1 in ['^','v','<','>']:
                        # move pos1
                        neighbor1 = numeric_adjacency[pos1].get(press1)
                        if neighbor1 is None:
                            continue
                        new_pos1 = neighbor1
                    else:
                        # press1 == 'A' => type a character on numeric keypad
                        # if pos1 == code[new_typed], typed_so_far += 1
                        if pos1 == code[new_typed]:
                            new_typed += 1
                        else:
                            # mismatch => skip
                            continue

            new_state = (new_pos3, new_pos2, new_pos1, new_typed)
            nd = d + 1

            # Insert into BFS if new or same-dist
            if new_state not in dist:
                dist[new_state] = nd
                paths[new_state] = []
                for old_path in paths[state]:
                    paths[new_state].append(old_path + press3)
                queue.append(new_state)
            elif dist[new_state] == nd:
                # Another equally minimal approach to new_state
                for old_path in paths[state]:
                    paths[new_state].append(old_path + press3)

    if not solutions:
        return None, []

    return found_dist, solutions


def numeric_part(code):
    return int(code[:-1])  # remove trailing 'A'

def complexity(code, sequence):
    return numeric_part(code) * len(sequence)


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
    file_path = os.path.join(directory, 'input2.txt')  # Update path to input file

    # Read codes from the input file
    codes = read_codes(file_path)
    print("Codes to type:", codes)
    print()

    total_complexity = 0
    for code in codes:
        print(f"Processing Code: {code}")
        # Produce all minimal L3 sequences for the code
        dist, sols = single_bfs_all_minimal(code)
        if not sols:
            print(f"  No valid sequences found for code: {code}")
            continue

        # Find the minimal length among all L3 solutions
        min_length = min(len(seq) for seq in sols)
        best_L3_solutions = [seq for seq in sols if len(seq) == min_length]
        print(min_length == dist)

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

    # 208974 <-- the answer is waay too high apparently
    # 200000 <-- the answer is waayy too low figured
    # 224274 <-- the answer is too high but very close!
    # 220000 <-- the answer