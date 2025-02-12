import os
import heapq
from collections import deque, defaultdict

def read_grid(file_path):
    """
    Reads the racetrack grid from the input file.
    Returns a 2D grid and the coordinates of S and E.
    """
    grid = []
    start = end = None
    with open(file_path, 'r') as f:
        for y, line in enumerate(f):
            row = list(line.rstrip('\n'))
            grid.append(row)
            if 'S' in row:
                start = (row.index('S'), y)
            if 'E' in row:
                end = (row.index('E'), y)
    return grid, start, end

def bfs_no_cheat(grid, start, end):
    """
    Simple BFS to find shortest path without using any cheat.
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    visited = set()
    queue = deque([(start[0], start[1], 0)])
    while queue:
        x, y, dist = queue.popleft()
        if (x, y) == end:
            return dist
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] in ('.','S','E'):
                    queue.append((nx, ny, dist+1))
    return float('inf')

def dijkstra_with_cheats(grid, start, end, base_cost, min_savings=100):
    """
    Use a modified Dijkstra's algorithm to consider all paths that use up to 2 cheat steps.
    The cheat rules:
      - Exactly once, you may pass through up to 2 wall cells ('#').
      - After using these 1 or 2 cheat steps, you must land on a track cell to end the cheat.
      - Once the cheat is ended, you cannot cheat again.
    
    We keep track of:
      (x, y, cheat_used (bool), cheat_ended (bool), cheat_steps (0 to 2), cheat_start)
    
    cheat_start is recorded when we first step onto a wall cell using the cheat.
    When the cheat ends (by stepping onto a track cell after cheat steps), we record cheat_end.
    Each successful path that reaches the end with a used cheat scenario is recorded.
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0,1), (1,0), (0,-1), (-1,0)]

    # Priority queue for Dijkstra: (cost, x, y, cheat_used, cheat_ended, cheat_steps, cheat_start_x, cheat_start_y)
    # We do not store cheat_end in the state. We will determine cheat_end when cheat_ends.
    # We'll store visited states to avoid infinite loops.
    visited = set()
    heap = []
    # Initial state: no cheat used or ended, no cheat steps, no cheat_start
    heapq.heappush(heap, (0, start[0], start[1], False, False, 0, None, None))

    # Dictionary to store counts: map time_saved -> count, but we also need to separate by cheat scenario.
    # We'll store scenarios by (cheat_start, cheat_end, time_saved).
    # The problem states that cheats are uniquely identified by their start and end positions.
    # We'll keep a dictionary keyed by (cheat_start, cheat_end, time_saved) or better: (cheat_start, cheat_end) -> best time_saved
    # If multiple paths yield the same (cheat_start, cheat_end) but different costs, we only record the best time_saved.
    found_cheats = {}  # ((cx, cy), (ex, ey)) -> best_time_saved

    while heap:
        cost, x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy = heapq.heappop(heap)

        state = (x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy)
        if state in visited:
            continue
        visited.add(state)

        if (x, y) == end:
            # If we ended at the end:
            # If cheat was used and ended properly, record this cheat
            if cheat_used and cheat_ended:
                time_saved = base_cost - cost
                cheat_start_pos = (c_sx, c_sy)
                # We know the cheat_end pos is where cheat ended. We must deduce where cheat ended:
                # Cheat ended the moment we stepped onto a track cell after using cheat steps.
                # To identify cheat_end, we need to track when cheat ended.
                # This is a challenge: we didn't store cheat_end directly. 
                # Let's revise logic to store cheat_end:
                # Once cheat ends, we know the current position is the cheat_end.
                # We must store cheat_end state. We'll store cheat_end directly in the state as well.
                # Let's do that now: We'll add cheat_end_x, cheat_end_y to the state.

                # For simplicity, let's modify the approach: we will store cheat_end_x, cheat_end_y once we end the cheat.

                # However, we didn't do that yet. Let's fix this now:
                # Instead of re-running everything, let's just note that we must have recorded cheat_end
                # at the moment we ended the cheat. We'll revise the code below after this block.

                # Temporarily, no cheat_end recorded -> skip.
                # We'll fix after rewriting transitions.
                pass
            continue

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue

            cell = grid[ny][nx]
            new_cost = cost + 1

            if cell in ('.', 'S', 'E'):
                # Track cell
                # If currently in the middle of a cheat (cheat_used == True and cheat_steps>0) and not ended:
                # stepping on a track cell ends the cheat.
                if cheat_used and not cheat_ended and cheat_steps > 0:
                    # Cheat ends here. Record cheat_end as (nx, ny).
                    # We'll push a state with cheat_ended=True and store cheat_end.
                    new_state = (nx, ny, cheat_used, True, cheat_steps, c_sx, c_sy, nx, ny)
                else:
                    new_state = (nx, ny, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, None, None)

                # But we need to store cheat_end_x and cheat_end_y in state for final identification.
                # Let's change the state definition to always have cheat_end_x and cheat_end_y as well:
                # State now: (cost, x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, c_ex, c_ey)
                # Initially, c_ex, c_ey = None, None

            else:
                # Wall cell
                # If cheat_ended is True, we cannot pass through a wall anymore.
                if cheat_ended:
                    continue
                # If we have not used the cheat yet, we can start now.
                if not cheat_used:
                    # Start cheat with this step
                    # cheat_start is the current cell (x, y) before moving into the wall
                    # cheat_steps = 1
                    new_state = (nx, ny, True, False, 1, x, y, None, None)
                else:
                    # Already used cheat
                    if cheat_steps == 0:
                        # Means we used cheat before but never took a wall step? That shouldn't happen, cheat_steps>0 means we took a step.
                        # If cheat_used=True and cheat_steps=0, it means we started cheat but never took a step? Not possible by our logic.
                        continue
                    elif cheat_steps == 1:
                        # Take second cheat step
                        # cheat_steps=2 now
                        new_state = (nx, ny, True, False, 2, c_sx, c_sy, None, None)
                    else:
                        # cheat_steps=2 means we can't go through another wall
                        continue

            # Push new state to heap
            # Wait, we updated the state definition midway. Let's finalize the state structure consistently.
            # Let's define a single consistent state structure now:

    # Revised final code below with correct state handling.

def dijkstra_with_cheats_fixed(grid, start, end, base_cost, min_savings=100):
    width, height = len(grid[0]), len(grid)
    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    # State: (cost, x, y, cheat_used, cheat_ended, cheat_steps, cheat_start_x, cheat_start_y, cheat_end_x, cheat_end_y)
    # cheat_start_x/y is set when we first use the cheat on a wall cell.
    # cheat_end_x/y is set when cheat ends by stepping onto a track cell.
    # Initially, cheat_end_x/y = None, None until cheat ends.
    start_state = (0, start[0], start[1], False, False, 0, None, None, None, None)

    visited = set()
    pq = []
    heapq.heappush(pq, start_state)

    # Dictionary to store best results: ((cheat_start), (cheat_end), time_saved)
    # We'll store them in a dict keyed by (c_sx, c_sy, c_ex, c_ey, time_saved) or just store after done.
    # Actually, we only need counts of how many save at least X. 
    # But we also want to know all distinct time savings and counts.
    # Let's store: ( (c_sx, c_sy), (c_ex, c_ey), time_saved ) in a dictionary that keeps track of best time_saved.
    cheat_scenarios = {}

    while pq:
        cost, x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, c_ex, c_ey = heapq.heappop(pq)

        state = (x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, c_ex, c_ey)
        if state in visited:
            continue
        visited.add(state)

        if (x, y) == end:
            # Reached end
            if cheat_used and cheat_ended:
                # Valid cheat scenario
                time_saved = base_cost - cost
                start_pos = (c_sx, c_sy)
                end_pos = (c_ex, c_ey)
                if start_pos is not None and end_pos is not None:
                    # Record scenario
                    # If this scenario (start_pos, end_pos) was seen before, keep max time_saved
                    if (start_pos, end_pos) not in cheat_scenarios or cheat_scenarios[(start_pos, end_pos)] < time_saved:
                        cheat_scenarios[(start_pos, end_pos)] = time_saved
            continue

        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            cell = grid[ny][nx]
            new_cost = cost + 1

            if cell in ('.','S','E'):
                # Track cell
                if cheat_used and not cheat_ended and cheat_steps > 0:
                    # Ending cheat now
                    new_state = (new_cost, nx, ny, True, True, cheat_steps, c_sx, c_sy, nx, ny)
                else:
                    # No change in cheat status
                    new_state = (new_cost, nx, ny, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, c_ex, c_ey)
                heapq.heappush(pq, new_state)

            else:
                # Wall cell
                if cheat_ended:
                    # Can't cheat anymore
                    continue
                # If not used cheat yet
                if not cheat_used:
                    # Start cheat with this step (first cheat step)
                    # cheat_start = current cell (x, y) before we move
                    new_state = (new_cost, nx, ny, True, False, 1, x, y, None, None)
                    heapq.heappush(pq, new_state)
                else:
                    # Already in cheat mode
                    if cheat_steps == 1:
                        # Can take second cheat step
                        new_state = (new_cost, nx, ny, True, False, 2, c_sx, c_sy, None, None)
                        heapq.heappush(pq, new_state)
                    elif cheat_steps == 2:
                        # No more cheat steps allowed
                        continue
                    else:
                        # cheat_steps == 0 means cheat_used=True but no steps taken? Not possible in our logic.
                        continue

    # Now we have all cheat scenarios in cheat_scenarios.
    # We want to know how many cheats would save at least 100 picoseconds.
    # The puzzle also wants a distribution, but let's focus on what was asked:
    # "How many cheats would save you at least 100 picoseconds?"

    # Each scenario: (start_pos, end_pos) -> best_time_saved
    # Count how many have time_saved >= min_savings
    count = sum(1 for v in cheat_scenarios.values() if v >= min_savings)
    return cheat_scenarios, count


def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')  # Adjust as needed
    #file_path = os.path.join(directory, 'input2.txt')  # Adjust as needed
    grid, start, end = read_grid(file_path)

    # Find shortest time without cheats
    time_without_cheat = bfs_no_cheat(grid, start, end)
    print(f"Time without cheats: {time_without_cheat}")

    # Find cheats with savings
    cheat_scenarios, count_100 = dijkstra_with_cheats_fixed(grid, start, end, time_without_cheat, min_savings=100)

    # Print the results
    # Print all cheat savings sorted
    savings_count = defaultdict(int)
    for time_saved in cheat_scenarios.values():
        savings_count[time_saved] += 1

    print("All Cheats by Time Saved:")
    for ts in sorted(savings_count.keys()):
        print(f"Time saved: {ts}, Count: {savings_count[ts]}")

    print(f"\nNumber of cheats that save at least 100 picoseconds: {count_100}")

if __name__ == "__main__":
    main()
