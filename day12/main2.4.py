import numpy as np
import os
import sys
sys.setrecursionlimit(10**7)

def read_grid(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # strip whitespace and skip empty lines
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
                
                # DFS or BFS
                stack = [(i,j)]
                visited[i][j] = True
                
                while stack:
                    r, c = stack.pop()
                    region_positions.append((r,c))
                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < n and 0 <= nc < m:
                            if not visited[nr][nc] and grid[nr][nc] == letter:
                                visited[nr][nc] = True
                                stack.append((nr,nc))
                
                # region_positions now contains one entire region of the same letter
                regions.append((letter, region_positions))
    
    return regions

def get_boundary_edges(region_positions, grid):
    """
    Return a set of edges representing the fence boundary for a given region.
    Each edge will be represented as a tuple of two points ((x1,y1),(x2,y2))
    where (x1,y1) and (x2,y2) are grid line coordinates.
    """
    n = len(grid)
    m = len(grid[0])
    region_set = set(region_positions)
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    edges = set()
    
    for (i, j) in region_positions:
        # For each cell, check the four directions. If it's a boundary, record that edge.
        # Represent corners in a grid where cell (i,j) top-left corner is (i,j)
        # So cell (i,j) spans from vertical lines j to j+1 and horizontal lines i to i+1.
        
        # UP EDGE
        if i == 0 or (i-1,j) not in region_set:
            # edge along top of cell: from (i,j) to (i,j+1)
            e = ((i, j), (i, j+1))
            edges.add(edge_normalized(e))
        
        # DOWN EDGE
        if i == n-1 or (i+1,j) not in region_set:
            # bottom edge: from (i+1,j) to (i+1,j+1)
            e = ((i+1, j), (i+1, j+1))
            edges.add(edge_normalized(e))
        
        # LEFT EDGE
        if j == 0 or (i,j-1) not in region_set:
            # left edge: from (i, j) to (i+1, j)
            e = ((i, j), (i+1, j))
            edges.add(edge_normalized(e))
        
        # RIGHT EDGE
        if j == m-1 or (i,j+1) not in region_set:
            # right edge: from (i, j+1) to (i+1, j+1)
            e = ((i, j+1), (i+1, j+1))
            edges.add(edge_normalized(e))
            
    return edges

def edge_normalized(e):
    # Normalize edge representation so the lower coordinate always comes first
    # This ensures we don't distinguish direction in the set of edges
    (x1, y1), (x2, y2) = e
    if (x2 < x1) or (x2 == x1 and y2 < y1):
        return ((x2, y2), (x1, y1))
    else:
        return ((x1, y1), (x2, y1 if x2!=x1 else y2))

def build_loops(edges):
    """
    Given a set of edges (each edge is ((x1,y1),(x2,y2))),
    form closed loops. Each loop is a list of vertices in order.
    
    Steps:
    - Convert edges into adjacency dict {point: [connected_points]}
    - Find loops by walking until we return to start
    """
    adj = {}
    for e in edges:
        p1, p2 = e
        adj.setdefault(p1, []).append(p2)
        adj.setdefault(p2, []).append(p1)
    
    # We must find cycles. Every edge should be part of a loop.
    # Since this forms closed polygons, each connected component forms one or more loops.
    visited_edges = set()
    loops = []
    
    # Convert edges to a more "walkable" form
    # We'll pick an unused edge, follow adjacency to form a loop.
    # Because this is a polygon boundary, each vertex should have an even degree (2 or more).
    
    edges_list = list(edges)
    for start_edge in edges_list:
        if start_edge in visited_edges:
            continue
        # Start a loop from this edge
        loop = []
        # We'll pick direction. start_edge = (p1, p2)
        p1, p2 = start_edge
        current = p1
        prev = None
        next_point = p2
        
        # To walk the loop:
        loop.append(p1)
        loop.append(p2)
        visited_edges.add((p1,p2) if p1<p2 else (p2,p1))
        
        current = p2
        prev = p1
        
        # Walk until we get back to start
        while current != loop[0]:
            # find next_point in adj[current] which is not prev
            neighbors = adj[current]
            # one of them is prev, the other continues the loop
            if len(neighbors) > 2:
                # Might be a complex node, pick the correct edge that forms a polygon chain
                # The polygon edges should form simple loops, at each vertex exactly two edges belong
                # to the polygon loop we are currently tracing. 
                # The 'prev' is where we came from, so we pick the other neighbor that isn't prev.
                candidate = [p for p in neighbors if p != prev]
                if len(candidate) != 1:
                    # This would be unusual for a simple polygon boundary,
                    # but could happen if there's branching. Normally, polygon edges
                    # from a region form closed simple polygons without branching at a node.
                    # If multiple candidates, pick one systematically. 
                    # In a well-formed puzzle, this should not happen.
                    pass
                next_point = candidate[0]
            else:
                # Exactly two neighbors (prev and one other)
                if neighbors[0] == prev:
                    next_point = neighbors[1]
                else:
                    next_point = neighbors[0]
            
            loop.append(next_point)
            # Mark this edge as visited
            ed = (current,next_point) if current<next_point else (next_point,current)
            visited_edges.add(ed)
            prev, current = current, next_point
        
        # We formed a loop. Remove duplicate of first point at the end if present
        if loop[-1] == loop[0]:
            # It's a closed loop. Good.
            loops.append(loop)
    
    return loops

def count_loop_sides(loop):
    """
    Given a loop (list of coordinates (x,y)), count how many sides it has under the new rule.
    The loop is a sequence of vertices; edges are between consecutive vertices.
    Multiple consecutive edges in the same direction (horizontal or vertical) form a single side.
    """
    # Extract edges from consecutive pairs in loop: (loop[i], loop[i+1])
    # The last vertex in loop == first vertex (closed), so the loop length includes start repeated at end.
    # If the loop is formed as [p1, p2, p3, ..., p1], we should ignore the last repeated vertex for direction counting.
    # Actually, from build_loops we do have p1 repeated at end. Let's ensure the loop ends with the start point:
    if loop[0] != loop[-1]:
        loop.append(loop[0])
    
    sides = 0
    # Determine direction changes
    # direction: 'H' for horizontal, 'V' for vertical
    prev_dir = None
    for i in range(len(loop)-1):
        x1, y1 = loop[i]
        x2, y2 = loop[i+1]
        if x1 == x2:
            current_dir = 'H'
        else:
            current_dir = 'V'
        
        if current_dir != prev_dir:
            sides += 1
        prev_dir = current_dir
    
    return sides

def calculate_sides(region_positions, grid):
    """
    Calculate the number of sides for a given region according to Part Two rules.
    """
    edges = get_boundary_edges(region_positions, grid)
    loops = build_loops(edges)
    # Each region can have multiple loops: one outer boundary and possibly holes.
    # The total sides is sum of the sides of all loops.
    total_sides = 0
    for loop in loops:
        total_sides += count_loop_sides(loop)
    return total_sides

def solve_part2(grid):
    # Similar to part one, but now we calculate sides instead of perimeter
    regions = get_regions(grid)
    total_cost = 0
    for letter, region_positions in regions:
        area = len(region_positions)
        sides = calculate_sides(region_positions, grid)
        cost = area * sides
        total_cost += cost
    return total_cost

def main():
    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    file_path = directory+'input2.txt' # Use correct input file here

    lines = read_grid(file_path)
    # Part Two solution:
    score = solve_part2(lines)
    print(score)

if __name__ == "__main__":
    main()
