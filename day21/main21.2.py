import sys
from collections import deque

#
# 1) DEFINE KEYPAD LAYOUTS AS GRIDS
#
#    We'll store each keypad as:
#       keypad_layout[key] = (row, col)
#    plus a matrix of valid cells (or None if it's a gap).
#

# Numeric keypad (rows top to bottom, columns left to right):
#     (r=0)  7   8   9
#     (r=1)  4   5   6
#     (r=2)  1   2   3
#     (r=3)  (gap)  0   A
#
numeric_layout = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2)
}

# We'll build a small 4x3 matrix of valid cells.  We'll mark gaps as None.
numeric_matrix = [[None]*3 for _ in range(4)]
# fill with something like the key letter
for k,(r,c) in numeric_layout.items():
    numeric_matrix[r][c] = k

# Directional keypad:
#   row=0:   [gap]  '^'  'A'
#   row=1:   '<'    'v'  '>'
#
directional_layout = {
                '^': (0,1), 'A': (0,2),
    '<': (1,0), 'v': (1,1), '>': (1,2)
}
directional_matrix = [[None]*3 for _ in range(2)]
for k,(r,c) in directional_layout.items():
    directional_matrix[r][c] = k


def neighbors_direction(r, c, matrix):
    """Return (move_cmd, nr, nc) for each valid up/down/left/right from (r,c)."""
    # up (^)
    if r > 0 and matrix[r-1][c] is not None:
        yield '^', (r-1, c)
    # down (v)
    if r+1 < len(matrix) and matrix[r+1][c] is not None:
        yield 'v', (r+1, c)
    # left (<)
    if c > 0 and matrix[r][c-1] is not None:
        yield '<', (r, c-1)
    # right (>)
    if c+1 < len(matrix[0]) and matrix[r][c+1] is not None:
        yield '>', (r, c+1)


#
# 2) A BFS that finds a minimal path of '^','v','<','>' from one button to another,
#    ignoring 'A' (we never "press" them, just move).  We'll memoize for each keypad separately.
#

memo_move_paths = {}  # (keypad_id, start_button, end_button) -> string of moves

def find_move_path(keypad_id, start, end):
    """
    Return a minimal sequence of '^','v','<','>' that moves from `start` to `end`
    on the given keypad_id ('numeric' or 'dir'), ignoring gaps.
    """
    if start == end:
        return ""

    key = (keypad_id, start, end)
    if key in memo_move_paths:
        return memo_move_paths[key]

    if keypad_id == 'numeric':
        layout = numeric_layout
        matrix = numeric_matrix
    else:
        layout = directional_layout
        matrix = directional_matrix

    if start not in layout or end not in layout:
        # Shouldn't happen unless invalid button
        memo_move_paths[key] = None
        return None

    start_rc = layout[start]
    end_rc   = layout[end]

    # BFS on the grid from start_rc to end_rc
    queue = deque()
    queue.append((start_rc, ""))  # ( (row,col), path_string_so_far )
    visited = set([start_rc])

    while queue:
        (r,c), path = queue.popleft()
        if (r,c) == end_rc:
            # Found a minimal path
            memo_move_paths[key] = path
            return path

        for move_cmd, (nr,nc) in neighbors_direction(r, c, matrix):
            if (nr,nc) not in visited:
                visited.add((nr,nc))
                queue.append(((nr,nc), path + move_cmd))

    # If unreachable (shouldn’t happen on these keypads if both start & end valid)
    memo_move_paths[key] = None
    return None


#
# 3) "Typing" a string on a keypad:
#    - We start at 'A' on that keypad
#    - For each character CH we want to produce:
#        * Move from current button to CH using find_move_path()
#        * Press 'A'
#      That yields a final string of moves+presses.
#
#    We'll memoize the entire typed result for (keypad_id, string).
#

memo_type_string = {}  # (keypad_id, string_to_type) -> typed_sequence

def type_string_on_keypad(keypad_id, string_to_type):
    """
    Return a minimal sequence of '^','v','<','>','A' that:
      - starts with the keypad's arm on 'A',
      - produces the entire `string_to_type` in order,
      - ends with the arm on the last typed character.
    """
    key = (keypad_id, string_to_type)
    if key in memo_type_string:
        return memo_type_string[key]

    if keypad_id == 'numeric':
        valid_set = set(numeric_layout.keys())
    else:
        # 'dir' or whatever
        valid_set = set(directional_layout.keys())

    # Validate: every character must be in that keypad
    for ch in string_to_type:
        if ch not in valid_set:
            raise ValueError(
                f"Trying to type {ch} on keypad {keypad_id}, but {ch} is not on that keypad!"
            )

    # Start from 'A'
    current = 'A'
    result_parts = []

    for ch in string_to_type:
        move_path = find_move_path(keypad_id, current, ch)
        if move_path is None:
            raise ValueError(
                f"Impossible to move from {current} to {ch} on keypad {keypad_id} without crossing a gap!"
            )
        # Add the movement, then an 'A' press
        result_parts.append(move_path)
        result_parts.append('A')
        current = ch

    typed_seq = "".join(result_parts)
    memo_type_string[key] = typed_seq
    return typed_seq


#
# 4) Building the layered sequence:
#    - The bottom layer is always the numeric keypad, where we want to type something like "980A".
#    - Then each layer above that is a directional keypad that "types" the sequence from the layer below.
#    - If we have L total layers (including numeric as layer #0), that means we have L-1 directional layers on top.
#    - We can go up to 20 layers if desired.
#

def build_layered_sequence(numeric_code, num_layers):
    """
    Return the final typed sequence on the *topmost* keypad if we have `num_layers` in total.

    - layer 0 = numeric keypad (just do 'type_string_on_keypad("numeric", numeric_code)')
    - layer 1 = 1 directional keypad controlling the numeric
    - layer 2 = 2 directional keypads controlling the numeric, etc.

    Example: if num_layers=3 (like the AoC puzzle):
      - L1 = type numeric_code on numeric keypad
      - L2 = type L1 on directional keypad
      - L3 = type L2 on directional keypad
      => result is L3.
    """
    # 0) Always produce the "lowest" code on numeric keypad
    typed_on_numeric = type_string_on_keypad("numeric", numeric_code)

    # 1) Then each additional layer is typed on a directional keypad
    current_string = typed_on_numeric
    for _ in range(num_layers - 1):
        # produce that string on a directional keypad
        typed_on_dir = type_string_on_keypad("dir", current_string)
        current_string = typed_on_dir

    # The final "top" sequence is what we actually press at layer = num_layers
    return current_string


#
# 5) Complexity Calculation
#

def complexity(numeric_code, final_sequence):
    """
    puzzle complexity = (integer value of numeric_code[:-1]) * len(final_sequence)
    e.g. "980A" -> 980 * len(final_sequence)
    """
    num_part = int(numeric_code[:-1])  # remove trailing 'A'
    return num_part * len(final_sequence)


#
# Example "main":
#
def main():
    # Suppose we want to do EXACTLY 3 layers (like the AoC day 21 puzzle).
    # code_list = ["029A", "980A", "179A", "456A", "379A"]
    # Or let’s say we read them from command line or something.
    code_list = ["029A", "980A", "179A", "456A", "379A"]
    code_list = ["319A", "670A", "349A", "964A", "586A"]
    num_layers = 3

    total = 0
    for code in code_list:
        top_sequence = build_layered_sequence(code, num_layers)
        seq_len = len(top_sequence)
        comp = complexity(code, top_sequence)
        total += comp

        print(f"Code {code} with {num_layers} layers:")
        print(f"  Final typed length = {seq_len}")
        print(f"  Complexity = {comp}")
        print(f"  Example final sequence: {top_sequence}\n")

    print(f"Overall total complexity = {total}")


if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()
