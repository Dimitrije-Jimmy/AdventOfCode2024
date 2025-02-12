from collections import deque

#
# 1) Define adjacency for the numeric keypad
#
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
    'A': {'^': '3', 'v': None, '<': '0', '>': None},
}

#
# 2) Define adjacency for the directional keypad
#
directional_keypad_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None},
}


#
# A. Memoized BFS for minimal "move path" from one button to another.
#    (Ignoring presses of 'A', we only build a path of '^','v','<','>' to move from start->end.)
#

memo_move_paths = {}  # (keypad_id, start, end) -> string of '^','v','<','>'

def find_shortest_move_path(keypad_adjacency, keypad_id, start_button, end_button):
    """
    Returns one shortest path (as a string of '^','v','<','>') to move from start_button
    to end_button using the given keypad_adjacency, ignoring any transitions that are None.
    Uses BFS. Memoized to avoid repeating BFS for the same pair.
    """
    if (keypad_id, start_button, end_button) in memo_move_paths:
        return memo_move_paths[(keypad_id, start_button, end_button)]

    if start_button == end_button:
        memo_move_paths[(keypad_id, start_button, end_button)] = ""
        return ""

    # BFS to find the minimal sequence of '^','v','<','>'
    queue = deque()
    queue.append((start_button, ""))  # (current_button, path_so_far)
    visited = set([start_button])

    while queue:
        curr_btn, path = queue.popleft()

        for move_cmd in ['^','v','<','>']:
            nxt = keypad_adjacency[curr_btn].get(move_cmd)
            if nxt is None:
                continue
            if nxt == end_button:
                # Found a path
                final_path = path + move_cmd
                memo_move_paths[(keypad_id, start_button, end_button)] = final_path
                return final_path
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + move_cmd))

    # If somehow unreachable (should not happen in these keypads), return None or ""
    memo_move_paths[(keypad_id, start_button, end_button)] = None
    return None


#
# B. "Type" a string on a given keypad:
#
def type_string_on_keypad(keypad_id, keypad_adjacency, target_string):
    """
    Starting from button 'A' on this keypad (the robot's arm),
    produce a minimal sequence of '^','v','<','>','A' that ends up having
    "typed" (activated) each character from target_string in order.

    - If the keypad is numeric, then each "character" in target_string is something like '0','2','9','A'.
      We move from the current position to that button, then press 'A'.
    - If the keypad is directional, then each "character" is one of '^','v','<','>','A'. We move from
      the current position to that *button*, then press 'A' to "activate" that button.

    Return the full sequence of button presses.
    """
    result = []
    current_pos = 'A'  # start aiming at 'A'

    for ch in target_string:
        # 1) Move from current_pos to ch
        move_path = find_shortest_move_path(keypad_adjacency, keypad_id, current_pos, ch)
        if move_path is None:
            # It's impossible or crosses a gap
            raise ValueError(f"Cannot reach {ch} from {current_pos} on keypad {keypad_id}")
        result.append(move_path)
        # 2) Press 'A' to activate that button
        result.append('A')
        # 3) Now the arm is pointing at ch
        current_pos = ch

    return "".join(result)


#
# C. Putting it all together for a single code like "029A":
#    L1 = minimal way to type "029A" on numeric keypad
#    L2 = minimal way (on directional #1) to produce L1
#    L3 = minimal way (on directional #2, i.e. "your" keypad) to produce L2
#

def produce_L3_for_code(code):
    # L1: type the numeric code on numeric keypad (start from numeric 'A')
    L1 = type_string_on_keypad(
        keypad_id="numeric",
        keypad_adjacency=numeric_keypad_adjacency,
        target_string=code
    )
    # L2: produce L1's sequence on *first* directional keypad
    L2 = type_string_on_keypad(
        keypad_id="dir1",
        keypad_adjacency=directional_keypad_adjacency,
        target_string=L1
    )
    # L3: produce L2's sequence on *second* directional keypad (the one you use)
    L3 = type_string_on_keypad(
        keypad_id="dir2",
        keypad_adjacency=directional_keypad_adjacency,
        target_string=L2
    )
    return L3

def code_complexity(code, l3_sequence):
    """
    Complexity = (integer numeric part of code) * length_of_l3_sequence
    Example: for 029A, numeric part is 29, multiplied by len(sequence).
    """
    # code is like "980A", so code[:-1] == "980"
    numeric_part = int(code[:-1])  # remove trailing 'A'
    return numeric_part * len(l3_sequence)

def main():
    codes = ["029A", "980A", "179A", "456A", "379A"]
    total = 0
    for c in codes:
        l3 = produce_L3_for_code(c)
        comp = code_complexity(c, l3)
        total += comp
        print(f"{c} => L3 length = {len(l3)}, complexity = {comp}")
        print(f"  Example L3 = {l3}\n")

    print(f"Total complexity = {total}")

if __name__ == "__main__":
    main()
