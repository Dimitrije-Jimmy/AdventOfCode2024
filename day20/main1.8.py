from collections import deque
import math
import os

def read_grid(file_path):
    grid = []
    start = end = None
    with open(file_path,'r') as f:
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
            print(f"Visited {visited_count} cells in BFS from {start}")
        for dx,dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] in ('.','S','E'):
                    if dist[nx][ny] > d+1:
                        dist[nx][ny] = d+1
                        q.append((nx,ny))
    return dist

def try_cheats(grid, distFromStart, distFromEnd, distWithoutCheat):
    width, height = len(grid[0]), len(grid)
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    
    cheat_scenarios = {}
    visited_count = 0

    for y in range(height):
        for x in range(width):
            if distFromStart[x][y] == math.inf:
                continue  # not reachable without cheat
            base_dist = distFromStart[x][y]

            # If even from here going directly without cheat can't do better, skip.
            if base_dist >= distWithoutCheat:
                continue

            visited_count += 1
            if visited_count % 100000 == 0:
                print(f"Checked {visited_count} cells for cheat opportunities")

            # Try a single cheat step:
            for dx, dy in directions:
                # Step into a wall?
                wx, wy = x+dx, y+dy
                if 0 <= wx < width and 0 <= wy < height and grid[wy][wx] == '#':
                    # After stepping into the wall, we must step out onto track in the same direction:
                    tx, ty = wx+dx, wy+dy
                    if 0 <= tx < width and 0 <= ty < height and grid[ty][tx] in ('.','E'): 
                        # cost = base_dist + 2 (one step into wall, one step onto track)
                        total_cost = base_dist + 2 + distFromEnd[tx][ty]
                        if total_cost < distWithoutCheat:
                            time_saved = distWithoutCheat - total_cost
                            scenario_key = ((x,y),(tx,ty))
                            if scenario_key not in cheat_scenarios or cheat_scenarios[scenario_key] < time_saved:
                                cheat_scenarios[scenario_key] = time_saved

                # If you want to consider 2-step cheat (two walls), you'd extend further:
                # w2x, w2y = wx+dx, wy+dy (a second wall cell), then a track cell after that
                # Check similarly and if valid, total_cost = base_dist + 3, etc.

    return cheat_scenarios

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    grid, start, end = read_grid(file_path)

    print("Running BFS from start...")
    distFromStart = bfs_no_cheat(grid, start)
    print("Running BFS from end...")
    distFromEnd = bfs_no_cheat(grid, end)

    distWithoutCheat = distFromStart[end[0]][end[1]]
    print(f"Time without cheats: {distWithoutCheat}")

    print("Trying cheat scenarios...")
    cheat_scenarios = try_cheats(grid, distFromStart, distFromEnd, distWithoutCheat)

    from collections import defaultdict
    savings_count = defaultdict(int)
    for ts in cheat_scenarios.values():
        savings_count[ts] += 1

    print("All Cheats by Time Saved:")
    for tsv in sorted(savings_count.keys()):
        print(f"Time saved: {tsv}, Count: {savings_count[tsv]}")

    count_100 = sum(1 for v in cheat_scenarios.values() if v>=100)
    print(f"\nNumber of cheats that save at least 100 picoseconds: {count_100}")

if __name__ == "__main__":
    main()
