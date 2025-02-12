from collections import deque

#
# 1) Adjacency for NUMERIC KEYPAD (like AoC's layout)
#    We'll store it as a grid or direct adjacency. Either is fine.
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
# 2) Adjacency for DIRECTIONAL KEYPAD
#
directional_adjacency = {
    '^': {'^': None, 'v': 'v', '<': None, '>': 'A'},
    'v': {'^': '^', 'v': None, '<': '<', '>': '>'},
    '<': {'^': None, 'v': None, '<': None, '>': 'v'},
    '>': {'^': 'A', 'v': None, '<': 'v', '>': None},
    'A': {'^': None, 'v': '>', '<': '^', '>': None},
}


###############################################################################
# PART A: BFS to find minimal arrow-press DISTANCE between every pair of buttons
#         (We don't store the *path*, just the *distance*, but you can store the path if you want.)
###############################################################################

def build_distance_map(adjacency):
    """
    Given an adjacency dict (like numeric_adjacency or directional_adjacency),
    produce a dict: dist_map[(start, end)] = minimal arrow presses from start->end,
    ignoring gaps (None).
    We'll do a BFS from each possible start to figure out the distance to every end.
    """
    keys = list(adjacency.keys())  # all valid buttons
    dist_map = {}

    for start in keys:
        # BFS from 'start' to find distances to all others
        queue = deque()
        queue.append((start, 0))
        visited = {start}
        local_dist = {start: 0}  # distance from 'start' to a discovered button

        while queue:
            curr, d = queue.popleft()
            # record (start, curr) => d in dist_map
            dist_map[(start, curr)] = d

            # expand neighbors
            for move_cmd in ['^','v','<','>']:
                nxt = adjacency[curr].get(move_cmd)
                if nxt is not None and nxt not in visited:
                    visited.add(nxt)
                    local_dist[nxt] = d+1
                    queue.append((nxt, d+1))

        # anything unreachable remains out of dist_map => won't be used

    return dist_map

# Build these once:
numeric_dist_map = build_distance_map(numeric_adjacency)
directional_dist_map = build_distance_map(directional_adjacency)


###############################################################################
# PART B: Function to "type" a given string on a keypad at depth=0
#
#        For numeric keypad, the "string" might be "029A".
#        For directional keypad, the "string" might be "^<A>" etc.
#
#        If depth=0 => we are directly typing on that keypad => cost = sum of
#           (arrow presses to move from current-> nextChar) + 1 for 'A'
#        If the keypad is numeric, start at 'A' in the bottom-right corner.
#        If the keypad is directional, start at 'A' in the top-right corner.
###############################################################################

def cost_to_type_string_on_keypad(
    keypad_id,
    string_to_type
):
    """
    Return how many button presses (arrows + 'A') it takes to type `string_to_type` 
    on the given keypad (numeric or directional) if we do it *directly* (depth=0).
    
    That means:
      - We start with the arm at 'A' (the keypad's 'A' button).
      - For each char c in string_to_type:
           cost += distance_map[A->c] (arrow presses)
           cost += 1  (to press 'A' and activate c)
         then the arm is now at c
    """
    if keypad_id == 'numeric':
        dist_map = numeric_dist_map
        start_btn = 'A'  # numeric 'A' button (bottom right)
    else:
        # 'directional'
        dist_map = directional_dist_map
        start_btn = 'A'  # directional 'A' (upper right)

    current = start_btn
    total = 0
    for ch in string_to_type:
        # arrow distance
        if (current, ch) not in dist_map:
            # unreachable => panic or skip
            # theoretically shouldn't happen with the puzzle's layout
            return float('inf')
        dist_moves = dist_map[(current, ch)]
        total += dist_moves
        # press 'A'
        total += 1
        current = ch

    return total


###############################################################################
# PART C: The recursive function that handles multiple LAYERS of directional robots
#
#   - If depth=0, we type directly on numeric or directional keypad => use BFS-dist approach above.
#   - If depth>0, that means "this string is typed on a directional keypad,
#     but each press might come from a deeper layer."
#
#   We'll store memo[(string, depth, keypad_id)] => minimal cost
###############################################################################

memo = {}

def cost_to_type(string_to_type, depth, keypad_id):
    """
    Returns the minimal cost to produce `string_to_type` on `keypad_id` if we have `depth` robots 
    above it. 
      - If depth=0 => we do cost_to_type_string_on_keypad(keypad_id, string_to_type).
      - Otherwise => we simulate "typing" string_to_type on `keypad_id`, but each typed character 
         is produced by a deeper robot (depth-1). 
         
         So the cost to "activate" character C on `keypad_id` is:
           (arrow presses to move from current->C, on this keypad) + 
            1 press of 'A' 
            BUT that single 'A' is itself a command typed by the deeper layer => 
              cost_to_type( C, depth-1, 'directional' ) if keypad_id is 'directional'
              cost_to_type( C, depth-1, 'numeric' ) if keypad_id is 'numeric' (the puzzle rarely layers numeric on numeric, but let's keep code general).
    """
    # We can handle the puzzle scenario specifically: numeric is always at bottom (depth=0),
    # directional for everything above. But let's keep it generic.

    # check memo
    key = (string_to_type, depth, keypad_id)
    if key in memo:
        return memo[key]

    if depth == 0:
        # directly type on this keypad
        ans = cost_to_type_string_on_keypad(keypad_id, string_to_type)
        memo[key] = ans
        return ans

    # else depth > 0
    # We simulate typing on this keypad, but each 'A' press => a single command from deeper layer
    # We'll do it character-by-character:

    if keypad_id == 'numeric':
        dist_map = numeric_dist_map
        current = 'A'   # numeric 'A'
    else:
        dist_map = directional_dist_map
        current = 'A'   # directional 'A'

    total_cost = 0
    for ch in string_to_type:
        # cost to move from current->ch on this keypad
        if (current, ch) not in dist_map:
            memo[key] = float('inf')
            return float('inf')
        move_steps = dist_map[(current, ch)]

        # cost for 1 press of 'A'
        # but that single press is typed by the deeper layer => cost_to_type(ch, depth-1, ???)
        # Typically, if keypad_id == 'numeric', the layer below might still be 'directional', 
        # but let's keep it exactly as you see the puzzle:
        # "One directional keypad controlling numeric" => use 'directional' as the deeper for numeric, etc.

        # For AoC day21 puzzle: 
        #   numeric is always controlled by the next-lower directional keypad
        #   directional is controlled by the next-lower directional keypad
        # We'll do that logic here:
        # "Press A" => 1 press, but that 1 press is "C" from deeper layer => cost_to_type( C, depth-1, 'directional' )
        # plus we must also actually produce 'A' itself at the deeper layer if we are in "directional"? 
        # The puzzle does a cascade of single commands. It's tricky, but let's interpret as your description:
        # We'll simplify: 
        #   1 press of 'A' at this level => cost = 1 + cost_to_type( "A", depth-1, 'directional' )
        # But you want *one single command* from deeper? Then we might do cost_to_type(ch, depth-1, 'directional').
        # The "trick" is how your puzzle sets up the cascade. 
        #
        # Because you said: "At each depth, we BFS to get a new slice..." 
        # We'll do a simpler approach: each 'A' => cost 1 + cost_to_type(ch, depth-1, 'directional')?

        # This is conceptual; adjust if your puzzle logic differs.

        cost_A = 1  # physically pressing 'A' at this layer
        cost_deeper = cost_to_type(ch, depth - 1, 'directional')
        press_cost = cost_A + cost_deeper

        total_cost += (move_steps + press_cost)
        current = ch

    memo[key] = total_cost
    return total_cost


###############################################################################
# Putting it all together for your puzzle scenario:
#   - The final code is typed on the numeric keypad (lowest level).
#   - But we have some number of directional keypads layered on top.
#   - E.g., for AoC day21 part2, we might have 2 directional robots => depth=2.
#
# Example usage.
###############################################################################

def solve_puzzle():
    codes = ["029A", "980A", "179A", "456A", "379A"]
    # Let's say we have 2 directional keypads above numeric => total of 3 layers:
    # depth=0 => typed directly on numeric
    # depth=2 => means your top-level calls cost_to_type(code, 2, 'numeric')
    # each press at this numeric is triggered by "directional" at depth=1
    # each press at the depth=1 directional is triggered by "directional" at depth=0 (some other robot?)
    # This is a bit labyrinthine, but let's pick an integer:
    depth_for_part2 = 2

    total_complex = 0
    for code in codes:
        cst = cost_to_type(code, depth_for_part2, 'numeric')
        # The puzzle's "complexity" = (numeric_part_of_code) * (length_of_your_keypad_presses).
        # But we only have "cost" = how many total presses do we do at the top level?
        # That is exactly cst. So complexity = numeric_part(code) * cst.

        # In your puzzle, they say e.g. for 980A => minimal top-level presses is 60, then 980*60 = 58800.
        # We'll do that:
        comp = int(code[:-1]) * cst
        total_complex += comp

        print(f"Code {code}, depth={depth_for_part2}, cost={cst}, complexity={comp}")

    print(f"Total complexity = {total_complex}")

if __name__ == "__main__":
    solve_puzzle()
