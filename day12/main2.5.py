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
                # Start a new region from this cell
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
        # Check all 4 edges of cell
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
    # Sort adjacency lists for reproducibility
    for k in adj:
        adj[k].sort()
    return adj

def is_horizontal(p1, p2):
    return p1[0] == p2[0]

def is_vertical(p1, p2):
    return p1[1] == p2[1]

def direction(p1, p2):
    # return 'H' or 'V'
    return 'H' if is_horizontal(p1,p2) else 'V'

def normalize_loop(loop):
    # loop is a list of points starting and ending at the same point
    # Remove duplicated last point:
    if loop[0] == loop[-1]:
        loop = loop[:-1]
    # find lexicographically smallest point
    min_pt = min(loop)
    idx = loop.index(min_pt)
    # rotate loop so it starts at min_pt
    loop = loop[idx:] + loop[:idx]
    # Ensure it's consistently oriented:
    # Compare the first edge direction with reversed loop's first edge direction
    # We'll pick the ordering that is lexicographically smallest after rotation
    rev = list(reversed(loop))
    min_pt2 = min(rev)
    idx2 = rev.index(min_pt2)
    rev = rev[idx2:] + rev[:idx2]
    if rev < loop:
        loop = rev
    return tuple(loop)

def find_loops(adj, edges):
    # We must find all simple cycles that use these edges.
    # Each edge belongs to at least one cycle since it's a polygon boundary.
    # A backtracking approach: pick an unused edge, try to form a loop.

    unused_edges = set(edges)
    visited_loops = set()

    def backtrack(path, start, current, came_from):
        # path: list of vertices visited so far
        # start: starting vertex of this attempt
        # current: current vertex
        # came_from: previous vertex
        # We need to form a loop that returns to start.
        # Also ensure rectilinear polygon: edges alternate H/V/H/V...
        
        if len(path) > 2 and current == start:
            # Closed loop found
            loop = normalize_loop(path)
            visited_loops.add(loop)
            return
        
        # Determine required direction change:
        # If we have at least one edge, we know the direction of last edge:
        if len(path) >= 2:
            prev_dir = direction(path[-2], path[-1])
        else:
            prev_dir = None

        for nxt in adj[current]:
            if nxt == came_from:
                continue
            # Check if edge current->nxt is unused:
            e = edge_normalized((current, nxt))
            if e not in unused_edges:
                continue
            # Check direction alternating:
            if prev_dir is not None:
                # new_dir must be perpendicular to prev_dir or could be same direction if continuing a straight line
                new_dir = direction(current, nxt)
                # Actually, for rectilinear polygons, consecutive edges must turn 90 degrees or continue straight.
                # Wait, puzzle states sides are straight runs in one direction. Edges are always axis-aligned.
                # Polygons are orthogonal, so edges must alternate directions to form corners.
                # If we don't allow straight runs to form separate sides, we can still have consecutive edges 
                # in the same direction forming a longer straight segment (they would be separate edges along the same line).
                # For a valid polygon boundary, we can have sequences of collinear edges. So same direction is allowed.
                
                # So no restriction other than edges must be axis aligned. The polygon can have straight segments made of multiple edges in line.
                # We'll rely on final counting of sides for direction changes.
                # So no direction check needed other than ensuring no weird crossing loops. This might risk false cycles, but
                # since every vertex has a grid structure, we should still form proper loops.
                pass
            
            # Try this edge
            unused_edges.remove(e)
            path.append(nxt)
            backtrack(path, start, nxt, current)
            path.pop()
            unused_edges.add(e)

    # Run backtracking from each edge once
    # To reduce complexity, start from each edge only once if it's still unused
    # Pick an unused edge, start from its p1 as start and try to form a loop
    # Actually, start a path with that edge: path = [p1, p2]
    # This will find multiple loops (since we may form loops in both directions).
    # We'll rely on normalization to avoid duplicates.
    edges_list = list(unused_edges)
    for e in edges_list:
        if e in unused_edges:
            p1, p2 = e
            # Try loop starting at p1->p2
            unused_edges.remove(e)
            backtrack([p1, p2], p1, p2, p1)
            unused_edges.add(e)
            # Also try the other direction p2->p1 if needed
            # Actually, this is redundant since the loop search is undirected,
            # but let's be thorough in case orientation matters:
            unused_edges.remove(e)
            backtrack([p2, p1], p2, p1, p2)
            unused_edges.add(e)

    return visited_loops

def count_loop_sides(loop):
    # loop is a tuple of points forming a closed polygon
    # Count direction changes to find the number of sides.
    # Actually, sides = number of straight segments. Each time direction changes from H to V or V to H, increment sides.
    # If multiple consecutive edges are in the same direction, they form one side.
    if loop[0] != loop[-1]:
        loop = list(loop)
        loop.append(loop[0])
    sides = 0
    prev_dir = None
    for i in range(len(loop)-1):
        d = direction(loop[i], loop[i+1])
        if d != prev_dir:
            sides += 1
        prev_dir = d
    return sides

def calculate_sides(region_positions, grid):
    edges = get_boundary_edges(region_positions, grid)
    adj = build_adjacency(edges)
    loops = find_loops(adj, edges)
    total_sides = 0
    for loop in loops:
        total_sides += count_loop_sides(loop)
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
    directory = os.path.dirname(__file__) + os.sep
    file_path = directory+'input.txt'
    # Adjust if needed:
    #file_path = directory+'input2.txt'

    lines = read_grid(file_path)
    score = solve_part2(lines)
    print(score)

if __name__ == "__main__":
    main()
