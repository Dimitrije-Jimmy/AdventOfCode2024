import os
import heapq
from collections import defaultdict, deque

def read_input(file_path):
    grid = []
    start_pos = None
    end_pos = None

    with open(file_path, 'r') as f:
        for y, line in enumerate(f):
            line = line.rstrip('\n')
            row = list(line)
            grid.append(row)
            for x, char in enumerate(row):
                if char == 'S':
                    start_pos = (x, y)
                elif char == 'E':
                    end_pos = (x, y)

    if start_pos is None or end_pos is None:
        raise ValueError("Start (S) or End (E) position not found in the map.")

    return grid, start_pos, end_pos

DIRECTIONS = ['N', 'E', 'S', 'W']
DIR_VECTORS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}

def rotate(current_dir, turn):
    idx = DIRECTIONS.index(current_dir)
    if turn == 'CW':
        return DIRECTIONS[(idx + 1) % 4]
    elif turn == 'CCW':
        return DIRECTIONS[(idx - 1) % 4]
    else:
        raise ValueError("Invalid turn direction. Use 'CW' or 'CCW'.")

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def dijkstra(grid, start_pos, end_pos):
    """
    Run Dijkstra to find minimal costs from start to end.
    Return a dictionary dist: (x, y, dir) -> cost
    """
    initial_dir = 'E'
    dist = {}
    heap = []
    heapq.heappush(heap, (0, start_pos[0], start_pos[1], initial_dir))
    dist[(start_pos[0], start_pos[1], initial_dir)] = 0

    while heap:
        cost, x, y, direction = heapq.heappop(heap)
        if dist[(x, y, direction)] < cost:
            continue

        # If we reached the end, don't break - we want all minimal paths info
        # Just continue to ensure we have minimal dist info for all states.

        # Actions:
        # 1) Move Forward
        dx, dy = DIR_VECTORS[direction]
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            if grid[ny][nx] != '#':
                ncost = cost + 1
                nstate = (nx, ny, direction)
                if nstate not in dist or ncost < dist[nstate]:
                    dist[nstate] = ncost
                    heapq.heappush(heap, (ncost, nx, ny, direction))

        # 2) Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        nstate = (x, y, new_dir)
        ncost = cost + 1000
        if nstate not in dist or ncost < dist[nstate]:
            dist[nstate] = ncost
            heapq.heappush(heap, (ncost, x, y, new_dir))

        # 3) Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        nstate = (x, y, new_dir)
        ncost = cost + 1000
        if nstate not in dist or ncost < dist[nstate]:
            dist[nstate] = ncost
            heapq.heappush(heap, (ncost, x, y, new_dir))

    return dist

def build_minimal_path_graph(grid, dist, start_pos, end_pos):
    """
    Using the dist dictionary, build a graph of minimal edges only.
    Graph: state -> list of next_states that are on minimal paths.
    A state is (x, y, dir).
    """
    graph = defaultdict(list)
    # We know all states and costs from dist.
    # For each state, consider the possible next states:
    for (x, y, direction), cost in dist.items():
        # Move Forward
        dx, dy = DIR_VECTORS[direction]
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            if grid[ny][nx] != '#':
                ncost = cost + 1
                nstate = (nx, ny, direction)
                if nstate in dist and dist[nstate] == ncost:
                    graph[(x, y, direction)].append((nx, ny, direction))

        # Rotate CW
        new_dir = rotate(direction, 'CW')
        ncost = cost + 1000
        nstate = (x, y, new_dir)
        if nstate in dist and dist[nstate] == ncost:
            graph[(x, y, direction)].append(nstate)

        # Rotate CCW
        new_dir = rotate(direction, 'CCW')
        ncost = cost + 1000
        nstate = (x, y, new_dir)
        if nstate in dist and dist[nstate] == ncost:
            graph[(x, y, direction)].append(nstate)

    return graph

def find_all_minimal_path_tiles(grid, dist, graph, start_pos, end_pos):
    """
    Now we have dist and a minimal-path graph. We know the minimal cost to reach E.
    We want to find all tiles that are on any minimal path.

    Steps:
    - Identify the minimal cost to reach any state at E coordinates.
    - From the start state (Sx, Sy, 'E'), do a DFS or BFS through the minimal-path graph.
    - Only proceed along edges that are part of minimal paths (already ensured by graph).
    - Keep track of visited states to avoid loops.
    - Collect all (x, y) tiles visited along the way that eventually lead to the end with minimal cost.

    Because we built graph only with minimal-path edges, any path that leads to E is minimal.
    We'll do a search that only explores states that can reach the end at minimal cost.

    To ensure we only count states that can lead to E with minimal cost, we can prune states that don't eventually reach E. But since we built the graph from all minimal edges, all endpoints that can't reach E won't matter. We'll still store them, but let's do a small check:

    Actually, we know the minimal graph includes only minimal transitions. However, some states might not lead to E. If we want to be certain, we could do a reachability check from E in the minimal graph (reversed) to prune unreachable states. But the user requested no backward searches. We'll rely on the assumption that only states connected to E remain in the minimal graph. If some states don't reach E, they won't affect collecting all minimal path tiles that do reach E, as we can stop exploring paths that don't lead to E if desired.

    Let's implement a final filtering step: We'll find the minimal cost to E from dist. Then any state whose dist != minimal cost at E must not be considered a final endpoint.
    We'll just explore from start and add all visited nodes. If we want to strictly only include tiles on actual paths that reach E, we can prune states that don't have a route to E. But that would require reverse checks.

    Without a backward check, we rely on the minimal graph edges. The minimal graph edges definition ensures only edges that lead toward minimal solutions. If no solution at the end, no minimal cost states at E. If minimal states at E are known, these edges form a DAG from start to E. We'll trust this.

    We'll do a DFS from (Sx, Sy, 'E') and whenever we reach any E-state, we know we found a minimal path. We'll collect all visited tiles in these successful traversals. Actually, to handle multiple paths, let's do a DFS and mark visited states. We'll record all tiles visited on paths that actually can reach E. To ensure we only record tiles on paths that reach E, let's do a top-down approach:

    Approach:
    - First, find all states at E with minimal cost. Distinguish minimal_end_cost.
    - Filter the graph to remove states that cannot lead to E with minimal cost. 
      To do this without backward search, we can do a forward search, but we must know which states lead to E. Without backward search, we might just trust that all states in minimal graph can lead to E. If not, some tiles may be included that aren't on a full path to E. The user wants all tiles on ANY minimal path to E, so we must ensure we only gather tiles from states that do lead to E.

    Let's do a small trick:
    We'll first identify all states that represent the end tile at minimal cost. Then do a forward DFS from start. If at some point we can't eventually reach E, that would mean a dead end. But how to detect that without backward checks?

    Without a backward search, it's tricky. However, since we constructed the graph from minimal edges, and these edges are only defined where `dist[next] = dist[current] + cost`, it should represent a "gradient" of increasing cost. Eventually, to be minimal, it must lead to an end state (E). There shouldn't be cycles with equal cost increments. If a path doesn't lead to E, it means it's a dead end in the minimal graph (no outgoing edges that maintain minimal property at some point).

    We'll do a DFS that only collects tiles if we can reach E:
    - Actually, since we know minimal cost states at E, we can do a quick memoization:
        If a state can lead to E, we store True.
        If it cannot, we store False.

    Let's add a memo that checks reachability to E states in the minimal graph. We'll do a top-down memoized DFS from start states that returns True if E is reachable from that state. This will not violate the "no backward search" rule as we are still going forward in the minimal graph from S. We will rely on recursion and memoization:
    - If state is at E coordinates and dist[state] == minimal_end_cost: return True
    - Else, recursively check successors. If any successor leads to E, return True.
    - If no successors lead to E, return False.

    This gives us a forward check for E-reachability on the minimal graph.

    After determining E-reachability, we do a final DFS (or during the same DFS) to collect all tiles from states that lead to E.

    We'll implement a helper function `can_reach_E(state)` that returns True/False and collects tiles if True.
    """

def find_minimal_cost_to_end(dist, end_pos):
    # minimal cost to reach end tile at any direction
    candidates = [c for (x,y,d), c in dist.items() if (x,y) == end_pos]
    if not candidates:
        return None
    return min(candidates)

def can_reach_E(state, end_pos, dist, graph, memo, best_tiles, minimal_end_cost):
    if state in memo:
        return memo[state]

    x, y, d = state
    # If this state is on the end tile and dist == minimal_end_cost, we reached E
    if (x, y) == end_pos and dist[state] == minimal_end_cost:
        best_tiles.add((x, y))
        memo[state] = True
        return True

    # Otherwise, check successors
    reachable = False
    for nxt in graph[state]:
        if can_reach_E(nxt, end_pos, dist, graph, memo, best_tiles, minimal_end_cost):
            # If successor leads to E, record this tile
            best_tiles.add((x, y))
            reachable = True

    memo[state] = reachable
    return reachable

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')

    grid, start_pos, end_pos = read_input(file_path)
    print(f"Start Position: {start_pos}")
    print(f"End Position: {end_pos}\n")

    print("Initial Warehouse State:")
    print_grid(grid)
    print("\nStarting Dijkstra's Algorithm...\n")

    # Run Dijkstra forward
    dist = dijkstra(grid, start_pos, end_pos)

    # Find minimal cost to reach E
    minimal_end_cost = find_minimal_cost_to_end(dist, end_pos)
    if minimal_end_cost is None:
        print("\nEnd Tile is unreachable from the Start Tile.")
        return
    print(f"\nLowest score to reach the End Tile: {minimal_end_cost}")

    # Build minimal-path graph
    graph = build_minimal_path_graph(grid, dist, start_pos, end_pos)

    # Now, find all tiles on all minimal paths.
    # Start from (start_x, start_y, 'E') since initial direction is East
    start_state = (start_pos[0], start_pos[1], 'E')
    if start_state not in dist:
        # If we never reached starting direction state, no solution
        print("\nEnd Tile is unreachable from the Start Tile.")
        return

    best_tiles = set()
    memo = {}  # state -> bool whether can reach E
    can_reach_E(start_state, end_pos, dist, graph, memo, best_tiles, minimal_end_cost)

    print(f"\nNumber of tiles part of at least one best path: {len(best_tiles)}")

    # Mark the best path tiles
    marked_grid = [row[:] for row in grid]  # copy grid
    for (x, y) in best_tiles:
        if (x, y) != start_pos and (x, y) != end_pos:
            marked_grid[y][x] = 'O'

    print("\nMarked Grid with Best Path Tiles (O):")
    print_grid(marked_grid)

if __name__ == "__main__":
    main()
