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
    """Convert a set of edges into a list of closed loops.
       Each loop is a list of edges forming a closed polygon.
       
       If a loop can't be closed, we do not record it and restore its edges to 'unused'.
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
        start_vertex = start_edge[0]
        current_vertex = start_edge[1]
        prev_edge = start_edge

        completed = False
        # Try to follow edges around until we come back to start_vertex
        while True:
            connected_edges = vertex_map[current_vertex]
            next_edge = None
            # Find the next edge that continues the loop
            for ce in connected_edges:
                if ce != prev_edge and ce in unused:
                    next_edge = ce
                    break
            
            if next_edge is None:
                # No next edge found, can't close the loop
                break
            
            # Use the next edge
            loop.append(next_edge)
            unused.remove(next_edge)
            # Move current_vertex along the loop
            current_vertex = next_edge[1] if next_edge[0] == current_vertex else next_edge[0]
            prev_edge = next_edge
            
            if current_vertex == start_vertex:
                # Loop closed
                completed = True
                break

        if completed:
            loops.append(loop)
        else:
            # Failed to form a closed loop, restore edges to unused
            for e in loop:
                if e not in unused:
                    unused.add(e)
            # Try another start edge from the while loop
    
    return loops

def count_sides_in_loop(loop_edges):
    # Reconstruct the chain of vertices
    chain = [loop_edges[0][0], loop_edges[0][1]]
    used = {loop_edges[0]}
    current_point = chain[-1]

    # Build full chain
    while len(used) < len(loop_edges):
        found_next = False
        for e in loop_edges:
            if e not in used:
                if e[0] == current_point:
                    chain.append(e[1])
                    current_point = e[1]
                    used.add(e)
                    found_next = True
                    break
                elif e[1] == current_point:
                    chain.append(e[0])
                    current_point = e[0]
                    used.add(e)
                    found_next = True
                    break
        if not found_next:
            # This shouldn't happen if loops are properly formed
            # Means we didn't form a proper closed loop
            # For debugging, you could print an error or raise an exception
            pass

    # Determine directions
    directions = []
    for i in range(len(chain)):
        p1 = chain[i]
        p2 = chain[(i+1) % len(chain)]
        if p1[0] == p2[0]:
            directions.append('H')
        else:
            directions.append('V')

    # Compress consecutive identical directions into one side
    sides = 1
    for i in range(1, len(directions)):
        if directions[i] != directions[i-1]:
            sides += 1

    return sides

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

