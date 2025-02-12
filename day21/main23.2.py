#!/usr/bin/env python3

from typing import List, Dict, Tuple

###############################################################################
# 1) Keypad layouts
###############################################################################

numeric_keypad = [
    "789",  # row=0
    "456",  # row=1
    "123",  # row=2
    " 0A",  # row=3
]

directional_keypad = [
    " ^A",  # row=0
    "<v>",  # row=1
]

###############################################################################
# 2) Functions to find positions, check gaps, and build an "optimal" L-shaped path
###############################################################################

def find_position(keypad: List[str], char: str) -> Tuple[int, int]:
    for r, row_str in enumerate(keypad):
        for c, ch in enumerate(row_str):
            if ch == char:
                return (r, c)
    raise ValueError(f"Character {char!r} not found on keypad.")

def is_gap(keypad: List[str], r: int, c: int) -> bool:
    """Return True if (r,c) is out of range or is a ' ' space (gap)."""
    if r < 0 or r >= len(keypad):
        return True
    row_str = keypad[r]
    if c < 0 or c >= len(row_str):
        return True
    return (row_str[c] == ' ')

def optimal_path(src: str, dst: str, keypad: List[str]) -> str:
    """
    Returns an "optimal" L-shaped path of '^','v','<','>' from src -> dst
    using your custom heuristic:
      - Check if you're going left (dc < 0).
      - Possibly check if you "would cross a gap" horizontally first vs. vertically first.
      - Then move either vertical->horizontal or horizontal->vertical accordingly.
    """

    # 1. Find positions
    r1, c1 = find_position(keypad, src)
    r2, c2 = find_position(keypad, dst)

    dr = r2 - r1  # positive => 'v', negative => '^'
    dc = c2 - c1  # positive => '>', negative => '<'

    going_left = (dc < 0)

    # Check if "corner cell" might be a gap if we do horizontal-first or vertical-first
    def would_cross_gap_vert_first() -> bool:
        # Move vertically first => (r2,c1), then horizontally to (r2,c2)
        # If (r2,c1) or (r2,c2) is a gap, we say True
        if is_gap(keypad, r2, c1):
            return True
        if is_gap(keypad, r2, c2):
            return True
        return False

    def would_cross_gap_horiz_first() -> bool:
        # Move horizontally first => (r1,c2), then vertically => (r2,c2)
        if is_gap(keypad, r1, c2):
            return True
        if is_gap(keypad, r2, c2):
            return True
        return False

    on_gap_vert_first = would_cross_gap_vert_first()
    on_gap_horiz_first = would_cross_gap_horiz_first()

    # "If goingLeft != on_gap" => do vertical first, else horizontal first.
    # We'll interpret "on_gap" to be whether horizontal-first approach crosses a gap.
    on_gap = on_gap_horiz_first
    do_vertical_first = (going_left != on_gap)

    # Build the path
    moves = []

    def add_vertical(d: int):
        if d > 0:
            moves.append('v' * d)
        elif d < 0:
            moves.append('^' * (-d))

    def add_horizontal(d: int):
        if d > 0:
            moves.append('>' * d)
        elif d < 0:
            moves.append('<' * (-d))

    if do_vertical_first:
        add_vertical(dr)
        add_horizontal(dc)
    else:
        add_horizontal(dc)
        add_vertical(dr)

    return "".join(moves)

###############################################################################
# 3) Precompute all arrow-paths for every (src, dst) on each keypad
###############################################################################

def get_all_buttons(keypad: List[str]) -> List[str]:
    """
    Return all non-gap characters on the keypad (like '7','8','9','A', etc.).
    """
    chars = []
    for row_str in keypad:
        for ch in row_str:
            if ch != ' ':
                chars.append(ch)
    return chars

def build_precomputed_paths(keypad: List[str]) -> Dict[Tuple[str, str], str]:
    """
    For every pair (src, dst) in this keypad, compute the "optimal_path(src, dst, keypad)"
    using your L-shaped logic, and store in a dict:
        precomputed[(src, dst)] = arrow_moves_string
    """
    buttons = get_all_buttons(keypad)
    precomputed = {}
    for src in buttons:
        for dst in buttons:
            path_str = optimal_path(src, dst, keypad)
            precomputed[(src, dst)] = path_str
    return precomputed

# Build them:
numeric_paths = build_precomputed_paths(numeric_keypad)
directional_paths = build_precomputed_paths(directional_keypad)

###############################################################################
# 4) "Type a string" on a given keypad using the precomputed arrow paths
###############################################################################

def type_string_on_keypad(
    keypad_name: str,
    precomputed: Dict[Tuple[str, str], str],
    string_to_type: str
) -> str:
    """
    Produce a minimal arrow-press sequence (plus 'A' activations) to type `string_to_type`
    on the keypad with adjacency given by `precomputed`.

    We assume the robot arm starts on 'A' (like the puzzle states).
    For each character c in string_to_type:
      - move from current to c (using precomputed path)
      - press 'A'
      - update current = c

    Returns a string of '^','v','<','>','A'.
    """
    result = []
    current = 'A'  # start at 'A'

    for ch in string_to_type:
        # 1) arrow moves from current -> ch
        path_moves = precomputed[(current, ch)]
        result.append(path_moves)
        # 2) press 'A' to "activate"
        result.append('A')
        current = ch

    return "".join(result)

###############################################################################
# 5) Example: layering numeric, then one directional keypad
###############################################################################

def produce_layered_sequence(code: str) -> str:
    """
    Example with exactly one layer of directional keypad controlling the numeric keypad:
      - L1: We want to type `code` on numeric.  So the sequence L1 = type_string_on_keypad(numeric_paths, code).
      - L2: We produce L1's sequence on the directional keypad. That final result is what *we* physically type.
    """
    # L1: type the code on numeric
    L1_seq = type_string_on_keypad("numeric", numeric_paths, code)

    # L2: type L1_seq on directional
    L2_seq = type_string_on_keypad("directional", directional_paths, L1_seq)
    L3_seq = type_string_on_keypad("directional", directional_paths, L2_seq)
    return L3_seq

###############################################################################
# 6) Putting it all together for 029A, 980A, etc.
###############################################################################

def main():
    codes = ["029A", "980A", "179A", "456A", "379A"]

    total_complexity = 0
    for c in codes:
        # We'll do exactly 1 directional layer above numeric here
        # If you want 2 directional layers, do produce_layered_sequence() again with L2_seq, etc.
        final_seq = produce_layered_sequence(c)

        # The puzzle's "complexity" = numeric_part(code) * length_of_final_seq
        numeric_part = int(c[:-1])  # remove trailing 'A'
        length_seq = len(final_seq)
        comp = numeric_part * length_seq
        total_complexity += comp

        print(f"Code {c}:")
        print(f"  Final sequence length = {length_seq}")
        print(f"  Complexity = {comp}")
        print(f"  Example final sequence: {final_seq}")
        print()

    print(f"TOTAL COMPLEXITY = {total_complexity}")


if __name__ == "__main__":
    main()
