from collections import deque, defaultdict
import math
import sys

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

def bfs_no_cheat(grid, start):
    width, height = len(grid[0]), len(grid)
    dist = [[math.inf]*height for _ in range(width)]
    dist[start[0]][start[1]] = 0
    q = deque([start])
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    visited_count = 0
    while q:
        x,y = q.popleft()
        d = dist[x][y]
        visited_count += 1
        if visited_count % 100000 == 0:
            print(f"BFS from {start}: visited {visited_count} cells")
        for dx,dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] in ('.','S','E'):
                    if dist[nx][ny] > d+1:
                        dist[nx][ny] = d+1
                        q.append((nx,ny))
    return dist

def find_cheats(grid, distFromStart, distFromEnd, distWithoutCheat, max_cheat=20, min_savings=100):
    width, height = len(grid[0]), len(grid)
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    cheat_scenarios = {}
    visited_cells = 0

    # We'll only start cheat searches from cells that are reachable and might give improvement
    candidates = [(x,y) for y in range(height) for x in range(width) if distFromStart[x][y] < math.inf and distFromStart[x][y]<distWithoutCheat]

    for i, (sx,sy) in enumerate(candidates):
        baseDist = distFromStart[sx][sy]
        # If even starting here we have no chance:
        # The best we can do is add steps and distFromEnd minimal is 0, if baseDist>=distWithoutCheat no point continuing
        # We already filtered that above.

        # BFS in cheat mode from (sx,sy)
        # State: (x,y,steps_used)
        # We'll store visited states for cheat BFS to avoid repeating
        visited = set()
        q = deque([(sx,sy,0)])
        visited.add((sx,sy,0))

        expansions = 0
        while q:
            x,y,steps = q.popleft()
            expansions += 1
            if expansions % 100000 == 0:
                print(f"Cheat BFS from ({sx},{sy}) processed {expansions} states")

            # If we're on track (not starting cell with steps=0) and steps>0, we can end cheat
            # grid[ny][nx] in ('.','E') means track
            if steps>0 and grid[y][x] in ('.','E'):
                total_cost = baseDist + steps + distFromEnd[x][y]
                if total_cost < distWithoutCheat:
                    time_saved = distWithoutCheat - total_cost
                    scenario_key = ((sx,sy),(x,y))
                    if scenario_key not in cheat_scenarios or cheat_scenarios[scenario_key]<time_saved:
                        cheat_scenarios[scenario_key]=time_saved

            if steps == max_cheat:
                continue  # Can't go further than 20 steps

            # Try expanding in all directions
            for dx,dy in directions:
                nx, ny = x+dx, y+dy
                if 0<=nx<width and 0<=ny<height:
                    # We can always step through walls or track in cheat mode
                    # The next step cost = steps+1
                    next_steps = steps+1
                    # Pruning: if even best case scenario not better, skip
                    # best_case_time = baseDist+next_steps+distFromEnd[nx][ny]
                    # if best_case_time >= distWithoutCheat, no improvement possible
                    # But we must be careful, we might find a better target further along.
                    # We'll still prune if best_case_time >= distWithoutCheat+some_margin. But let's keep it simple.

                    # Just basic pruning:
                    if distFromEnd[nx][ny]==math.inf and next_steps<max_cheat:
                        # If we have no path to end and still steps left, we might find another route. Let's not prune too aggressively here.
                        pass

                    state = (nx,ny,next_steps)
                    if state not in visited:
                        visited.add(state)
                        q.append(state)

    # Count how many cheats save at least min_savings
    count_min_savings = sum(1 for v in cheat_scenarios.values() if v>=min_savings)
    return cheat_scenarios, count_min_savings

def main():
    import os
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    grid, start, end = read_grid(file_path)

    print("Running BFS from start...")
    distFromStart = bfs_no_cheat(grid,start)
    print("Running BFS from end...")
    distFromEnd = bfs_no_cheat(grid,end)
    distWithoutCheat = distFromStart[end[0]][end[1]]
    print(f"Time without cheats: {distWithoutCheat}")

    # Try up to 20 cheat steps
    print("Finding cheats with up to 20 steps...")
    cheat_scenarios, count_100 = find_cheats(grid, distFromStart, distFromEnd, distWithoutCheat, max_cheat=20, min_savings=100)

    savings_count = defaultdict(int)
    for time_saved in cheat_scenarios.values():
        savings_count[time_saved]+=1

    print("All Cheats by Time Saved:")
    for tsv in sorted(savings_count.keys()):
        print(f"Time saved: {tsv}, Count: {savings_count[tsv]}")

    print(f"\nNumber of cheats that save at least 100 picoseconds: {count_100}")

if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    main()

