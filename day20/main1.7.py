import os
import heapq
from collections import defaultdict, deque
import math

def read_grid(file_path):
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
    width, height = len(grid[0]), len(grid)
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    visited = set()
    queue = deque([(start[0], start[1], 0)])
    while queue:
        x,y,dist = queue.popleft()
        if (x,y) == end:
            return dist
        if (x,y) in visited:
            continue
        visited.add((x,y))
        for dx,dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] in ('.','S','E'):
                    queue.append((nx, ny, dist+1))
    return math.inf

def heuristic(x, y, end):
    # Manhattan distance heuristic
    return abs(x - end[0]) + abs(y - end[1])

def a_star_one_cheat(grid, start, end, base_cost, min_savings=100):
    width, height = len(grid[0]), len(grid)
    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    # State: (cost, x, y, cheat_used, cheat_ended, c_sx, c_sy, c_ex, c_ey)
    # We'll store priority as cost + heuristic
    start_state = (0, start[0], start[1], False, False, None, None, None, None)
    pq = []
    heapq.heappush(pq, (0+heuristic(start[0], start[1], end), start_state))

    visited = set()
    cheat_scenarios = {}
    processed = 0
    best_solution = math.inf

    while pq:
        _, state = heapq.heappop(pq)
        cost, x, y, cheat_used, cheat_ended, c_sx, c_sy, c_ex, c_ey = state
        processed += 1
        if processed % 100000 == 0:
            print(f"Processed {processed} states, current best solution: {best_solution}")

        key = (x, y, cheat_used, cheat_ended, c_sx, c_sy, c_ex, c_ey)
        if key in visited:
            continue
        visited.add(key)

        if (x,y) == end:
            if cheat_used and cheat_ended and c_sx is not None and c_sy is not None and c_ex is not None and c_ey is not None and cost < base_cost:
                time_saved = base_cost - cost
                if time_saved < best_solution:
                    best_solution = time_saved
                scenario_key = ((c_sx,c_sy),(c_ex,c_ey))
                if scenario_key not in cheat_scenarios or cheat_scenarios[scenario_key] < time_saved:
                    cheat_scenarios[scenario_key] = time_saved
            continue

        # Pruning: If current cost already exceeds best_solution by a large margin, skip
        # (Not always beneficial, but can help if a solution is found early)
        if best_solution != math.inf and cost - base_cost > best_solution:
            continue

        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            ch = grid[ny][nx]
            new_cost = cost+1

            # Similar logic as before
            if ch in ('.','S','E'):
                if cheat_used and not cheat_ended:
                    ns = (new_cost, nx, ny, True, True, c_sx, c_sy, nx, ny)
                else:
                    ns = (new_cost, nx, ny, cheat_used, cheat_ended, c_sx, c_sy, c_ex, c_ey)
                heapq.heappush(pq, (new_cost+heuristic(nx, ny, end), ns))
            else:
                # Wall
                if cheat_ended:
                    continue
                if not cheat_used:
                    # Use cheat here
                    ns = (new_cost, nx, ny, True, False, x, y, None, None)
                    heapq.heappush(pq, (new_cost+heuristic(nx, ny, end), ns))
                else:
                    # Already used cheat
                    continue

    count_100 = sum(1 for v in cheat_scenarios.values() if v >= min_savings)
    return cheat_scenarios, count_100

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    grid, start, end = read_grid(file_path)

    time_without_cheat = bfs_no_cheat(grid, start, end)
    print(f"Time without cheats: {time_without_cheat}")

    cheat_scenarios, count_100 = a_star_one_cheat(grid, start, end, time_without_cheat, 100)

    savings_count = defaultdict(int)
    for ts in cheat_scenarios.values():
        savings_count[ts] += 1

    print("All Cheats by Time Saved:")
    for tsv in sorted(savings_count.keys()):
        print(f"Time saved: {tsv}, Count: {savings_count[tsv]}")

    print(f"\nNumber of cheats that save at least 100 picoseconds: {count_100}")

if __name__ == "__main__":
    main()
