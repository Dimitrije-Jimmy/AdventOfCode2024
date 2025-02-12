#!/usr/bin/env python3

"""
Advent of Code 2024 - Day 21: Keypad Conundrum

We want to type codes (like 029A, 980A, etc.) on a numeric keypad, but
there are multiple robots (layers).  Each layer 'expands' the commands
from the layer below into a (potentially much longer) sequence of moves
and 'A' presses.

This solution uses a simple "L-shaped movement" heuristic function (GetPath)
that returns how we move from one character (src) to another (dst) with
up/down/left/right arrow presses.  Then at each 'A' press (which means
"activate" or "type" the current character), we apply the logic again
for the layer above, and so on.

We can build the final typed string either iteratively (ExpandIterative),
recursively (ExpandRecursive), or only compute the final string LENGTH
via a memoized recursion (SolveMemoized), which is necessary for large
numbers of layers (like 25) because the final string can become huge.
"""

import sys
from functools import cache

################################################################################
# 1) Keypads (numeric and directional) laid out in small grids
################################################################################

# The puzzle’s numeric keypad, 4 rows × 3 columns:
#   Row 0: '7','8','9'
#   Row 1: '4','5','6'
#   Row 2: '1','2','3'
#   Row 3: ' ','0','A'   (space is a gap)
#
# The puzzle’s directional keypad, 2 rows × 3 columns:
#   Row 0: ' ','^','A'
#   Row 1: '<','v','>'
#
# We'll store them in a 'keypads' list: keypads[0] => numeric, keypads[1] => directional.
keypads = [
    [
        '789',
        '456',
        '123',
        ' 0A',
    ],
    [
        ' ^A',
        '<v>',
    ],
]

################################################################################
# 2) The "secret sauce" movement function: GetPath(keypad_id, src, dst)
#
#    This function returns a short string of '^','v','<','>' that moves
#    from src to dst on the given keypad (0 = numeric, 1 = directional).
#
#    Instead of BFS or heavy computations, we do a small "L-shaped" logic:
#      - We measure row difference (dr) and column difference (dc).
#      - If there's a gap in the corner, we do horizontal-first or vertical-first
#        whichever is allowed.
#      - Then we have a small set of "empirically determined" rules for
#        whether to move horizontally first or vertically first. 
#
#    This is enough to produce minimal arrow-press paths for these small keypads.
################################################################################
def GetPath(keypad_id, src, dst):
    """
    Return a minimal arrow-movement (string) from src -> dst on the
    keypad indexed by keypad_id (0 => numeric, 1 => directional).
    """
    keypad = keypads[keypad_id]

    # 1) Find row,col of src and dst
    r1 = c1 = r2 = c2 = None
    for r, row_str in enumerate(keypad):
        for c, ch in enumerate(row_str):
            if ch == src:
                r1, c1 = r, c
            if ch == dst:
                r2, c2 = r, c

    # row difference (dr) > 0 => we need 'v', <0 => '^'
    # col difference (dc) > 0 => we need '>', <0 => '<'
    dr = r2 - r1
    dc = c2 - c1

    # Build the naive horizontal and vertical parts
    # e.g. if dc > 0 => '>' repeated dc times
    horiz = '<>'[dc > 0] * abs(dc)   # a small trick: [False, True] => [0,1]
    verti = '^v'[dr > 0] * abs(dr)

    # If either difference is zero, it's easy
    if dr == 0:
        return horiz  # no vertical needed
    if dc == 0:
        return verti  # no horizontal needed

    # If there's a gap in the corner, we must do the other order
    # (since we can't move onto a space).
    #  e.g. if keypad[r2][c1] == ' ' => can't do vertical-first
    #       if keypad[r1][c2] == ' ' => can't do horizontal-first
    if keypad[r2][c1] == ' ':
        # can't go vertical first, so do horizontal then vertical
        return horiz + verti
    if keypad[r1][c2] == ' ':
        # can't go horizontal first, do vertical then horizontal
        return verti + horiz

    # Otherwise, apply the "empirically determined" rules:
    #  - If dr < 0 and dc < 0 => we do horiz+verti
    #  - If dr < 0 and dc > 0 => we do verti+horiz
    #  etc. The code picks whichever was found to be minimal in trials.
    if dr < 0 and dc < 0:
        return horiz + verti  # prefer "<v" over "v<"
    if dr < 0 and dc > 0:
        return verti + horiz  # prefer "v>" over ">v"
    if dr > 0 and dc < 0:
        return horiz + verti  # prefer "<v" over "v<"
    if dr > 0 and dc > 0:
        return verti + horiz  # prefer "v>" over ">v"

################################################################################
# 3) Next, we define ways to "expand" a code into the final typed string
#    by layering it N times. Each layer replaces each character with the moves
#    needed to produce that character, plus an 'A' press.
#
#    If robots=2, that means 2 directional layers on top of numeric, for a total
#    of 3 layers. So we do multiple expansions.
################################################################################

def ExpandIterative(code, robots):
    """
    Expand 'code' up to 'robots+1' layers (0 means numeric layer,
    1 and up means directional). 
    We start from 'A' each time, and for each character in the
    code/string, we do GetPath(...) + 'A'.
    Then that resulting string becomes the next layer's "code."

    Eventually we return the final big string. 
    """
    s = code
    for layer in range(robots + 1):
        # layer=0 => numeric (keypad_id=0), layer>0 => directional (keypad_id=1).
        keypad_id = 1 if layer > 0 else 0
        result = []
        last = 'A'  # start each layer from 'A'
        for ch in s:
            path = GetPath(keypad_id, last, ch)
            result.append(path)
            result.append('A')  # press 'A' to activate
            last = ch
        s = "".join(result)
    return s

def SolveIterative(code, robots):
    """
    Return the length of the final expanded string after 'robots' layers.
    """
    final_str = ExpandIterative(code, robots)
    return len(final_str)

################################################################################
# 4) A recursive version that does the same expansions as ExpandIterative
################################################################################

def ExpandRecursive(s, layer, robots):
    """
    Recursively expand the string 's' at layer 'layer'. If layer > robots,
    we are done. Otherwise, each character c in s is replaced by:
       GetPath(..., last, c) + 'A' 
    plus we call ExpandRecursive again for the next layer.
    """
    if layer > robots:
        return s  # no more expansions

    keypad_id = 1 if layer > 0 else 0
    last = 'A'
    out = []
    for ch in s:
        # "Expand" the path from last->ch on this layer
        path = GetPath(keypad_id, last, ch)
        # but then we also recursively expand that path+'A' at layer+1
        # so we do ExpandRecursive(...) on path+'A', *not* just append them
        # directly.  That might produce the same expansions.
        out.append(ExpandRecursive(path + 'A', layer + 1, robots))
        last = ch
    return "".join(out)

def SolveRecursive(code, robots):
    """
    Return the length of ExpandRecursive(code, 0, robots).
    """
    final_str = ExpandRecursive(code, 0, robots)
    return len(final_str)

################################################################################
# 5) The crucial optimization for huge number of layers: SolveMemoized()
#    We only compute the final string's LENGTH, not the string itself.
#
#    This is because for 25 robots, the final string is astronomically large.
#    But we can do a recursion that sums lengths. By storing partial results
#    in a cache, we avoid redundant expansions.
################################################################################

def SolveMemoized(code, robots):
    """
    Return the length of the final expanded string after robots expansions,
    but never build that string in memory. We only track lengths.

    We define an inner function Calc(s, layer) that returns how long the
    expansion of s is at layer. If layer > robots, we just return len(s).
    Otherwise, we break down s into characters, expand each one, and sum.

    We store (s, layer) in a cache so that if we see the same partial
    string again, we skip re-expanding it.
    """

    @cache
    def Calc(s, layer):
        # if we're beyond the top layer, just return len(s)
        if layer > robots:
            return len(s)

        keypad_id = 1 if layer > 0 else 0
        last = 'A'
        total_len = 0
        for ch in s:
            # expansions for path + 'A'
            path = GetPath(keypad_id, last, ch)
            expanded_str = path + 'A'
            # recursively get length of expanding that string at layer+1
            total_len += Calc(expanded_str, layer + 1)
            last = ch

        return total_len

    return Calc(code, 0)

################################################################################
# 6) Finally, we define a Solve(...) function that, given a solution approach
#    (SolveIterative, SolveRecursive, or SolveMemoized) plus a list of codes,
#    and a number of robots, computes the puzzle's final sum of complexities.
#
#    The puzzle states "complexity = numeric_part * final_sequence_length".
#    So if code is "029A", numeric_part=29, final_sequence_length might be 68.
#    Then add that up for all codes.
################################################################################

def Solve(solve_func, codes, robots):
    """
    For each code in 'codes', we compute solve_func(code, robots).
    Multiply that length by the numeric part (int(code.rstrip('A'))),
    and sum them all. Return that big sum.
    """
    total = 0
    for code in codes:
        # The puzzle says the numeric part is code[:-1].
        # e.g. '029A' => '029' => int => 29
        num_part = int(code.rstrip('A'))
        length = solve_func(code, robots)
        total += num_part * length
    return total


################################################################################
# 7) We test with the sample codes from the puzzle statement.
#    They mention 5 codes: 029A, 980A, 179A, 456A, 379A => sum=126384 with 2 robots
#    We also test a bigger layering (25 robots).
################################################################################

# Puzzle sample codes
sample_codes = ['029A', '980A', '179A', '456A', '379A']

# Double-check the results:
print("solving iterative")
assert Solve(SolveIterative, sample_codes, 2) == 126384
print("solving recursive")
assert Solve(SolveRecursive, sample_codes, 2) == 126384
print("solving memoized")
assert Solve(SolveMemoized,  sample_codes, 2) == 126384
# For 25 robots, the result is huge, but SolveMemoized can handle it quickly:
print("solving part two")
assert Solve(SolveMemoized,  sample_codes, 25) == 154115708116294

################################################################################
# 8) Solve the "real" input from stdin
#    We'll parse the codes, then print answers for robots=2 and robots=25.
################################################################################

def main():
    # Read codes from standard input (one per line)
    #codes = sys.stdin.read().splitlines()
    codes = ['029A', '980A', '179A', '456A', '379A']
    codes = ['319A', '670A', '349A', '964A', '586A']

    # Solve for 2 robots (the puzzle example scenario)
    ans_2 = Solve(SolveMemoized, codes, 2)
    print(ans_2)

    # Solve for 25 robots (some extended challenge scenario)
    ans_25 = Solve(SolveMemoized, codes, 25)
    print(ans_25)


if __name__ == "__main__":
    main()
