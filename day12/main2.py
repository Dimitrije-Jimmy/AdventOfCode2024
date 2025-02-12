import sys
import os
sys.setrecursionlimit(10**7)

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

def get_boundary_edges(region_positions, grid):
    """Return a set of edges that form the boundary of the region.
       Represent each edge by a tuple of coordinates ((r1,c1),(r2,c2))
       where (r1,c1) < (r2,c2) to keep a consistent ordering.
       
       We'll represent edges in terms of the grid cell corners.
       For a cell (r,c), the corners are:
         top-left: (r,c), top-right: (r,c+1)
         bottom-left: (r+1,c), bottom-right: (r+1,c+1)
       
       We'll check each cell boundary and if it's on the region boundary, we add that edge.
    """
    region_set = set(region_positions)
    edges = set()
    n = len(grid)
    m = len(grid[0])
    
    for (r, c) in region_positions:
        # top edge
        if r == 0 or (r-1,c) not in region_set:
            # edge between (r,c) and (r,c+1) in corner coords: ((r,c),(r,c+1))
            e = ((r,c),(r,c+1))
            edges.add(normalize_edge(e))
        # bottom edge
        if r == n-1 or (r+1,c) not in region_set:
            e = ((r+1,c),(r+1,c+1))
            edges.add(normalize_edge(e))
        # left edge
        if c == 0 or (r,c-1) not in region_set:
            e = ((r,c),(r+1,c))
            edges.add(normalize_edge(e))
        # right edge
        if c == m-1 or (r,c+1) not in region_set:
            e = ((r,c+1),(r+1,c+1))
            edges.add(normalize_edge(e))
    
    return edges

def normalize_edge(e):
    """Ensure the edge tuple is always in a consistent order.
       e is ((r1,c1),(r2,c2)) - let's ensure (r1,c1) < (r2,c2) lex order.
    """
    p1, p2 = e
    if p1 < p2:
        return (p1,p2)
    else:
        return (p2,p1)

def form_loops_from_edges(edges):
    """Convert a set of edges into a list of loops.
       Each loop is a list of edges forming a closed polygon.
       
       We know each polygon is closed, so we can start from any edge,
       then find connected edges until we return to the start.
    """
    # Build adjacency: for each vertex, which edges are connected?
    vertex_map = {}
    for e in edges:
        p1, p2 = e
        vertex_map.setdefault(p1, []).append(e)
        vertex_map.setdefault(p2, []).append(e)
    
    unused = set(edges)
    loops = []
    
    while unused:
        start_edge = unused.pop()
        loop = [start_edge]
        
        # We'll find a path from start_edge until we return to the start vertex
        # start_edge: (p1,p2)
        # pick one endpoint to start with
        current_vertex = start_edge[1]
        prev_edge = start_edge
        while current_vertex != start_edge[0]:
            # Find the next edge that shares current_vertex
            # It should be prev_edge and another edge connecting at current_vertex
            connected_edges = vertex_map[current_vertex]
            # We have to pick the edge not equal to prev_edge
            for ce in connected_edges:
                if ce != prev_edge and ce in unused:
                    loop.append(ce)
                    unused.remove(ce)
                    # advance
                    # determine next vertex
                    if ce[0] == current_vertex:
                        current_vertex = ce[1]
                    else:
                        current_vertex = ce[0]
                    prev_edge = ce
                    break
            else:
                # If no break happened, means we didn't find a matching next edge
                # This can happen if the polygon is complex; we assume well-formed input.
                # For complex shapes, more logic needed.
                break
        
        loops.append(loop)
    
    return loops

def count_sides_in_loop(loop_edges):
    """Count how many sides in a loop.
       First, order the edges in a chain. The form_loops_from_edges tries to return them connected,
       but we must ensure loop edges are in the correct traveling order.
    """
    # Order edges properly into a sequence of points
    # Start with loop_edges[0]
    chain = [loop_edges[0][0], loop_edges[0][1]]
    used = {loop_edges[0]}
    current_point = chain[-1]

    # We know loop is closed, so length of chain after done = number_of_edges+1 (same start & end)
    while len(used) < len(loop_edges):
        # find edge connected to current_point not in used
        for e in loop_edges:
            if e not in used:
                if e[0] == current_point:
                    chain.append(e[1])
                    current_point = e[1]
                    used.add(e)
                    break
                elif e[1] == current_point:
                    chain.append(e[0])
                    current_point = e[0]
                    used.add(e)
                    break

    # chain is a sequence of vertices forming the loop
    # Now determine directions of each edge in chain
    directions = []
    for i in range(len(chain)):
        p1 = chain[i]
        p2 = chain[(i+1)%len(chain)]  # next vertex in loop (wrap around)
        if p1[0] == p2[0]:
            # horizontal
            directions.append('H')
        else:
            # vertical
            directions.append('V')

    # Count direction changes
    changes = 0
    for i in range(len(directions)):
        curr = directions[i]
        prev = directions[i-1]
        if curr != prev:
            changes += 1

    # changes = number of direction changes = number of sides in polygonal chain
    return changes

def count_sides_for_region(region_positions, grid):
    edges = get_boundary_edges(region_positions, grid)
    loops = form_loops_from_edges(edges)
    
    total_sides = 0
    for loop in loops:
        sides = count_sides_in_loop(loop)
        total_sides += sides
    return total_sides

def solve(grid):
    regions = get_regions(grid)
    total_cost = 0
    for letter, region_positions in regions:
        area = len(region_positions)
        sides = count_sides_for_region(region_positions, grid)
        cost = area * sides
        total_cost += cost
    return total_cost

def main():
    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    file_path = directory+'input2.txt'
    lines = read_grid(file_path)

    score = solve(lines)
    print(score)

if __name__ == "__main__":
    main()
