import sys
sys.setrecursionlimit(10**7)
import os

def read_grid(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def get_regions(grid):
    n = len(grid)
    m = len(grid[0])
    visited = [[False]*m for _ in range(n)]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    regions = []
    
    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                letter = grid[i][j]
                region_positions = []
                stack = [(i,j)]
                visited[i][j] = True
                while stack:
                    r, c = stack.pop()
                    region_positions.append((r,c))
                    for dr, dc in directions:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < n and 0 <= nc < m:
                            if not visited[nr][nc] and grid[nr][nc] == letter:
                                visited[nr][nc] = True
                                stack.append((nr,nc))
                regions.append((letter, region_positions))
    
    return regions

def edge_normalized(e):
    (x1, y1), (x2, y2) = e
    if (x2 < x1) or (x2 == x1 and y2 < y1):
        return ((x2, y2), (x1, y1))
    else:
        return ((x1, y1), (x2, y2))

def get_boundary_edges(region_positions, grid):
    n = len(grid)
    m = len(grid[0])
    region_set = set(region_positions)
    edges = set()
    
    for (i, j) in region_positions:
        # Top
        if i == 0 or (i-1,j) not in region_set:
            e = ((i, j), (i, j+1))
            edges.add(edge_normalized(e))
        # Bottom
        if i == n-1 or (i+1,j) not in region_set:
            e = ((i+1, j), (i+1, j+1))
            edges.add(edge_normalized(e))
        # Left
        if j == 0 or (i,j-1) not in region_set:
            e = ((i, j), (i+1, j))
            edges.add(edge_normalized(e))
        # Right
        if j == m-1 or (i,j+1) not in region_set:
            e = ((i, j+1), (i+1, j+1))
            edges.add(edge_normalized(e))
            
    return edges

def build_adjacency(edges):
    adj = {}
    for e in edges:
        p1, p2 = e
        adj.setdefault(p1, []).append(p2)
        adj.setdefault(p2, []).append(p1)
    for k in adj:
        adj[k].sort()
    return adj

def is_horizontal(p1, p2):
    return p1[0] == p2[0]

def direction(p1, p2):
    # return a vector direction (dx,dy) from p1 to p2
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return (dx, dy)

def turn_right(d):
    dx, dy = d
    # turn right: (dx, dy) -> (dy, -dx)
    return (dy, -dx)

def turn_left(d):
    dx, dy = d
    # turn left: (dx, dy) -> (-dy, dx)
    return (-dy, dx)

def turn_back(d):
    dx, dy = d
    return (-dx, -dy)

def all_directions(d):
    # return directions in priority order: try straight, then right turn, then left turn, then back
    # For walking the polygon boundary consistently, we will try to go "straight" or "right" first to keep interior to one side.
    # Actually, since we want to go around consistently, let's pick a rule:
    # We'll always keep the polygon interior on our left side. For that, at each vertex:
    # - We have a current direction d.
    # - We want to turn left if possible (which keeps interior on left), if not go straight, if not turn right, if not back.
    # Let's prioritize left, straight, right, back for a "counterclockwise" orientation.

    # directions are relative turns we can make:
    # Let's define them:
    # left turn, straight, right turn, back
    return [turn_left(d), d, turn_right(d), turn_back(d)]

def next_vertex(current, direction):
    return (current[0] + direction[0], current[1] + direction[1])

def find_loops_in_component(adj, edges_component):
    # edges_component is a set of edges in this connected component
    # We'll find loops by:
    # 1) Convert edges to a dict for quick lookup
    edge_set = set(edges_component)
    # unused edges
    unused = set(edge_set)

    loops = []
    
    # Build a helper for checking if an edge exists:
    def has_edge(u,v):
        e = edge_normalized((u,v))
        return e in unused

    # Get all vertices in this component
    vertices = set()
    for e in edges_component:
        vertices.add(e[0])
        vertices.add(e[1])
    # Sort vertices to find a stable start point
    vertices = sorted(vertices)
    
    # We try to form loops starting from the lowest vertex that still has unused edges.
    # We'll trace a polygon boundary in a counterclockwise manner: always turning left if possible.
    
    def trace_loop(start):
        # pick an initial edge from start:
        # Just pick the smallest adjacent vertex to define initial direction
        neighbors = adj[start]
        # find a direction to start with. We'll pick the neighbor that forms an edge we haven't used.
        initial_neighbor = None
        for nbr in neighbors:
            if has_edge(start, nbr):
                initial_neighbor = nbr
                break
        if initial_neighbor is None:
            return None
        
        # initial direction:
        d = direction(start, initial_neighbor)
        loop = [start, initial_neighbor]
        unused.remove(edge_normalized((start, initial_neighbor)))
        current = initial_neighbor

        # Now walk around until we get back to start
        # At each step, we are at 'current' and came from 'loop[-2]'
        # direction d is from loop[-2] to loop[-1].
        while True:
            prev = loop[-2]
            cur = loop[-1]
            d = direction(prev, cur)
            # Try directions in order: left, straight, right, back to find next edge
            candidates = all_directions(d)
            found_next = False
            for nd in candidates:
                nxt = next_vertex(cur, nd)
                if nxt in adj[cur] and has_edge(cur, nxt):
                    # use this edge
                    loop.append(nxt)
                    unused.remove(edge_normalized((cur, nxt)))
                    found_next = True
                    if nxt == start:
                        # closed loop
                        return loop
                    break
            if not found_next:
                # Can't continue loop from here - this means something complex happened
                # We'll break and not return a loop. Possibly a disconnected or strange shape.
                # This should not happen for valid puzzles.
                return None
    
    while True:
        # find a vertex with unused edges:
        start_vertex = None
        for v in vertices:
            # check if v has any unused edges
            for w in adj[v]:
                if edge_normalized((v,w)) in unused:
                    start_vertex = v
                    break
            if start_vertex is not None:
                break
        
        if start_vertex is None:
            # no more unused edges
            break
        
        lp = trace_loop(start_vertex)
        if lp is not None and len(lp) > 2:
            # normalize loop
            loops.append(normalize_loop(lp))
        else:
            # If we failed to form a loop, it might be due to complexity or branching.
            # In a well-formed puzzle, every component should form loops.
            # If you run into this scenario, you might need even more complex logic
            # but let's assume the puzzle input is valid.
            pass

    return loops

def normalize_loop(loop):
    # Remove duplicate end point if present
    if loop[0] == loop[-1]:
        loop.pop()
    # Normalize by rotating to smallest vertex
    min_pt = min(loop)
    idx = loop.index(min_pt)
    loop = loop[idx:] + loop[:idx]
    # Check reversed ordering
    rev = loop[::-1]
    min_pt2 = min(rev)
    idx2 = rev.index(min_pt2)
    rev = rev[idx2:] + rev[:idx2]
    if tuple(rev) < tuple(loop):
        loop = rev
    return tuple(loop)

def connected_components(vertices, edges):
    adj = {}
    for e in edges:
        p1, p2 = e
        adj.setdefault(p1, []).append(p2)
        adj.setdefault(p2, []).append(p1)
    for v in adj:
        adj[v].sort()
    visited = set()
    comps = []
    def dfs(s):
        stack = [s]
        comp = set()
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            comp.add(u)
            for w in adj.get(u,[]):
                if w not in visited:
                    stack.append(w)
        return comp
    
    for v in vertices:
        if v not in visited:
            c = dfs(v)
            # extract edges in this component
            comp_edges = []
            for e in edges:
                if e[0] in c and e[1] in c:
                    comp_edges.append(e)
            comps.append((c, comp_edges))
    return comps

def count_loop_sides(loop):
    # loop is a tuple of points forming a closed polygon
    loop = list(loop)
    if loop[0] != loop[-1]:
        loop.append(loop[0])
    sides = 0
    prev_dir = None
    for i in range(len(loop)-1):
        d = direction(loop[i], loop[i+1])
        # direction class: horizontal or vertical is enough
        dir_char = 'H' if d[0] == 0 else 'V'
        if dir_char != prev_dir:
            sides += 1
        prev_dir = dir_char
    return sides

def calculate_sides(region_positions, grid):
    edges = get_boundary_edges(region_positions, grid)
    # Build global vertex set
    vertices = set()
    for e in edges:
        vertices.add(e[0])
        vertices.add(e[1])
    vertices = list(vertices)
    comps = connected_components(vertices, edges)
    total_sides = 0
    for c, ed in comps:
        adj = build_adjacency(ed)
        loops = find_loops_in_component(adj, ed)
        for lp in loops:
            total_sides += count_loop_sides(lp)
    return total_sides

def solve_part2(grid):
    regions = get_regions(grid)
    total_cost = 0
    for letter, region_positions in regions:
        area = len(region_positions)
        sides = calculate_sides(region_positions, grid)
        cost = area * sides
        total_cost += cost
    return total_cost

def main():
    # Adjust the input filename as needed
    directory = os.path.dirname(__file__) + os.sep
    file_path = directory + 'input.txt'
    #file_path = directory + 'input2.txt'
    lines = read_grid(file_path)
    score = solve_part2(lines)
    print(score)

if __name__ == "__main__":
    main()

    # 1491532 <-- previous wrong too high
    # 909564 <-- let's see this one
    # FUCK YEAH IT's CORRECT!
