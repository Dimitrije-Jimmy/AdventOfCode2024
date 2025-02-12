#!/usr/bin/env python3

"""
Implementing the heuristic for generating an optimal path between two buttons
(src -> dst) by deciding whether to move vertically or horizontally first.
"""

from typing import List, Tuple

# Example keypad layouts:

# Numeric keypad (4 rows, 3 columns):
#   row=0: [ '7', '8', '9' ]
#   row=1: [ '4', '5', '6' ]
#   row=2: [ '1', '2', '3' ]
#   row=3: [ ' ', '0', 'A' ]
numeric_keypad = [
    "789",
    "456",
    "123",
    " 0A",
]

# Directional keypad (2 rows, 3 columns):
#   row=0: [ ' ', '^', 'A' ]
#   row=1: [ '<', 'v', '>' ]
directional_keypad = [
    " ^A",
    "<v>",
]

def find_position(keypad: List[str], char: str) -> Tuple[int, int]:
    """
    Given a keypad (list of strings) and a character, return (row, col)
    where that character appears. If not found, raises ValueError.
    """
    for r, row_str in enumerate(keypad):
        for c, ch in enumerate(row_str):
            if ch == char:
                return (r, c)
    raise ValueError(f"Character {char!r} not found on keypad.")

def is_gap(keypad: List[str], r: int, c: int) -> bool:
    """
    Check if (r,c) is a 'gap' on this keypad. For example, ' ' (space).
    """
    if r < 0 or r >= len(keypad):
        return True
    row_str = keypad[r]
    if c < 0 or c >= len(row_str):
        return True
    return (row_str[c] == ' ')

def optimal_path(src: str, dst: str, keypad: List[str]) -> str:
    """
    Return an "optimal" L-shaped path of '^','v','<','>' from src -> dst
    using the heuristic:
      - Determine if you're going left (dc < 0).
      - Determine if you'd cross a gap corner if you move horizontally first
        vs. vertically first.
      - Then do either vertical-then-horizontal or horizontal-then-vertical
        so as to avoid the gap or respect the logic "if goingLeft != onGap"
        => vertical first, else horizontal first (for example).

    Adjust the condition to match your puzzle's discovered "best order".
    """
    # 1. Find positions
    r1, c1 = find_position(keypad, src)
    r2, c2 = find_position(keypad, dst)

    dr = r2 - r1  # positive => need 'v', negative => need '^'
    dc = c2 - c1  # positive => need '>', negative => need '<'

    going_left = (dc < 0)

    # Check if "corner cell" might be a gap if we move horizontally first or vertically first.
    # We'll define a small helper:
    def would_cross_gap_vert_first() -> bool:
        """
        Suppose we move vertically first from (r1,c1) -> (r2,c1),
        then horizontally (r2,c1) -> (r2,c2).  Check if we cross a gap corner.
        """
        # As soon as we move vertically to (r2, c1), if that spot is a gap => problem
        if is_gap(keypad, r2, c1):
            return True
        # Then eventually we move horizontally to (r2,c2). If that crosses a gap in a
        # step-by-step manner, we'd have to check each column in between. For simplicity,
        # let's just check that final. A more thorough approach might check each intermediate cell.
        # For a small keypad, that’s often enough to see if we end on a gap corner.
        return is_gap(keypad, r2, c2)

    def would_cross_gap_horiz_first() -> bool:
        """
        Suppose we move horizontally first (r1,c1) -> (r1,c2),
        then vertically (r1,c2) -> (r2,c2).  Check corners similarly.
        """
        if is_gap(keypad, r1, c2):
            return True
        return is_gap(keypad, r2, c2)

    on_gap_vert_first = would_cross_gap_vert_first()
    on_gap_horiz_first = would_cross_gap_horiz_first()

    # We'll adopt the logic from your snippet:
    #   "default to moving vertically UNLESS goingLeft != onGap"
    # but "onGap" we interpret as "would cross a gap if we do horizontal first".
    # So let's define onGap = on_gap_horiz_first, for instance:
    on_gap = on_gap_horiz_first

    # Now choose:
    # if goingLeft != on_gap => do vertical first
    # else => horizontal first
    do_vertical_first = (going_left != on_gap)

    path_parts = []

    def add_vertical_moves(d: int):
        if d > 0:
            path_parts.append('v' * d)
        elif d < 0:
            path_parts.append('^' * (-d))

    def add_horizontal_moves(d: int):
        if d > 0:
            path_parts.append('>' * d)
        elif d < 0:
            path_parts.append('<' * (-d))

    if do_vertical_first:
        add_vertical_moves(dr)
        add_horizontal_moves(dc)
    else:
        add_horizontal_moves(dc)
        add_vertical_moves(dr)

    return "".join(path_parts)

# -------------------------------------------------------------------------
# Demo usage:
# -------------------------------------------------------------------------

if __name__ == "__main__":
    # Just a few examples
    # E.g. moving from 'A' (bottom-right) to '0' (bottom row, middle)
    kp = numeric_keypad
    print("A -> 0:", optimal_path('A','0', kp))

    # For the directional keypad, let's see how to go from '^' to '>'
    kd = directional_keypad
    print("^ -> >:", optimal_path('^','>', kd))

    # or '>' to 'v'
    print("> -> v:", optimal_path('>','v', kd))

    # etc.
