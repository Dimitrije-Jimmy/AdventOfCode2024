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

def dijkstra_with_one_cheat_step(grid, start, end, base_cost, min_savings=100):
    """
    Modified Dijkstra's algorithm that allows exactly one cheat step.
    Cheat steps:
      - cheat_used: True if we've taken a wall step
      - cheat_ended: True if we've returned to track after using the cheat
      - We only allow 1 cheat step total.

    State: (cost, x, y, cheat_used, cheat_ended, cheat_start_x, cheat_start_y, cheat_end_x, cheat_end_y)
    """
    width, height = len(grid[0]), len(grid)
    directions = [(0,1), (1,0), (0,-1), (-1,0)]

    start_state = (0, start[0], start[1], False, False, None, None, None, None)
    visited = set()
    pq = []
    heapq.heappush(pq, start_state)

    # ( (c_sx, c_sy), (c_ex, c_ey) ) -> best time_saved
    cheat_scenarios = {}

    while pq:
        cost, x, y, cheat_used, cheat_ended, c_sx, c_sy, c_ex, c_ey = heapq.heappop(pq)
        state = (x, y, cheat_used, cheat_ended, c_sx, c_sy, c_ex, c_ey)
        if state in visited:
            continue
        visited.add(state)

        if (x, y) == end:
            # Valid scenario?
            # We must have used the cheat (cheat_used = True), ended it (cheat_ended = True), and saved time.
            if cheat_used and cheat_ended and cost < base_cost and c_sx is not None and c_sy is not None and c_ex is not None and c_ey is not None:
                time_saved = base_cost - cost
                scenario_key = ((c_sx, c_sy), (c_ex, c_ey))
                if scenario_key not in cheat_scenarios or cheat_scenarios[scenario_key] < time_saved:
                    cheat_scenarios[scenario_key] = time_saved
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue

            cell = grid[ny][nx]
            new_cost = cost + 1

            if cell in ('.','S','E'):
                # Track cell
                if cheat_used and not cheat_ended:
                    # Ending cheat now
                    new_state = (new_cost, nx, ny, True, True, c_sx, c_sy, nx, ny)
                else:
                    new_state = (new_cost, nx, ny, cheat_used, cheat_ended, c_sx, c_sy, c_ex, c_ey)
                heapq.heappush(pq, new_state)
            else:
                # Wall cell
                if cheat_ended:
                    # Can't cheat anymore after ending
                    continue
                if not cheat_used:
                    # Use the single cheat step here
                    # cheat_start = current cell (x, y)
                    new_state = (new_cost, nx, ny, True, False, x, y, None, None)
                    heapq.heappush(pq, new_state)
                else:
                    # Already used cheat once, cannot do it again
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

    # Find shortest time without cheats
    time_without_cheat = bfs_no_cheat(grid, start, end)
    print(f"Time without cheats: {time_without_cheat}")

    # Try with one cheat step
    cheat_scenarios, count_100 = dijkstra_with_one_cheat_step(grid, start, end, time_without_cheat, min_savings=100)

    print("All Cheats by Time Saved:")
    savings_count = defaultdict(int)
    for time_saved in cheat_scenarios.values():
        savings_count[time_saved] += 1
    for ts in sorted(savings_count.keys()):
        print(f"Time saved: {ts}, Count: {savings_count[ts]}")

    print(f"\nNumber of cheats that save at least 100 picoseconds: {count_100}")

if __name__ == "__main__":
    main()
