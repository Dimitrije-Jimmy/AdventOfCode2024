import os
import heapq
from collections import defaultdict, deque

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
    
    State:
    (cost, x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, c_ex, c_ey)

    - cheat_used: True if we've started passing through walls.
    - cheat_steps: how many wall steps taken (1 or 2).
    - cheat_ended: True if we've stepped back onto track after using cheat steps.
    - c_sx, c_sy: cheat start position (where cheat is activated, just before the first wall step).
    - c_ex, c_ey: cheat end position (the track cell where we end the cheat).

    We only record scenarios that:
    - have cheat_used = True
    - cheat_steps > 0
    - cheat_ended = True
    - cost < base_cost (positive time saving)
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0,1), (1,0), (0,-1), (-1,0)]

    start_state = (0, start[0], start[1], False, False, 0, None, None, None, None)
    visited = set()
    pq = []
    heapq.heappush(pq, start_state)

    # ( (c_sx, c_sy), (c_ex, c_ey) ) -> best time_saved
    cheat_scenarios = {}

    while pq:
        cost, x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, c_ex, c_ey = heapq.heappop(pq)

        state = (x, y, cheat_used, cheat_ended, cheat_steps, c_sx, c_sy, c_ex, c_ey)
        if state in visited:
            continue
        visited.add(state)

        if (x, y) == end:
            # Check if this is a valid cheat scenario with time saving
            if cheat_used and cheat_ended and cheat_steps > 0 and cost < base_cost and c_sx is not None and c_sy is not None and c_ex is not None and c_ey is not None:
                time_saved = base_cost - cost
                scenario_key = ((c_sx, c_sy), (c_ex, c_ey))
                # Record only if it's better than previously known time_saved
                if scenario_key not in cheat_scenarios or cheat_scenarios[scenario_key] < time_saved:
                    cheat_scenarios[scenario_key] = time_saved
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
                if not cheat_used:
                    # Start cheat with this step (first cheat step)
                    # cheat_start = current cell (x, y)
                    new_state = (new_cost, nx, ny, True, False, 1, x, y, None, None)
                    heapq.heappush(pq, new_state)
                else:
                    # Already in cheat mode
                    if cheat_steps == 1:
                        # Can take second cheat step
                        new_state = (new_cost, nx, ny, True, False, 2, c_sx, c_sy, None, None)
                        heapq.heappush(pq, new_state)
                    # If cheat_steps == 2, no more wall steps are allowed.

    # Now we have all cheat scenarios in cheat_scenarios
    # Count how many have time_saved >= min_savings
    count = sum(1 for v in cheat_scenarios.values() if v >= min_savings)

    return cheat_scenarios, count

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')
    grid, start, end = read_grid(file_path)

    # Find shortest time without cheats
    time_without_cheat = bfs_no_cheat(grid, start, end)
    print(f"Time without cheats: {time_without_cheat}")

    # Find cheats with savings
    cheat_scenarios, count_100 = dijkstra_with_cheats(grid, start, end, time_without_cheat, min_savings=1)

    # Print the results
    savings_count = defaultdict(int)
    for time_saved in cheat_scenarios.values():
        savings_count[time_saved] += 1

    print("All Cheats by Time Saved:")
    for ts in sorted(savings_count.keys()):
        print(f"Time saved: {ts}, Count: {savings_count[ts]}")

    print(f"\nNumber of cheats that save at least 100 picoseconds: {count_100}")

if __name__ == "__main__":
    main()
