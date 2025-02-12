def parse_graph(input_lines):
    graph = {}
    for line in input_lines:
        if line.strip():
            node, neighbors = line.strip().split(':')
            node = node.strip()
            neighbor_nodes = neighbors.strip().split()
            if node not in graph:
                graph[node] = set()
            for neighbor in neighbor_nodes:
                neighbor = neighbor.strip()
                if neighbor:
                    graph[node].add(neighbor)
                    # Ensure bidirectional edges
                    if neighbor not in graph:
                        graph[neighbor] = set()
                    graph[neighbor].add(node)
    return graph

import itertools

def get_edges(graph):
    edges = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            edge = tuple(sorted([node, neighbor]))
            edges.add(edge)
    return list(edges)

def is_graph_connected(graph, removed_edges):
    visited = set()
    nodes = list(graph.keys())
    if not nodes:
        return True
    start_node = nodes[0]

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            edge = tuple(sorted([node, neighbor]))
            if edge not in removed_edges and neighbor not in visited:
                dfs(neighbor)

    dfs(start_node)
    return len(visited) == len(graph)

def find_optimal_cut(graph):
    edges = get_edges(graph)
    max_product = 0
    optimal_cut = None

    # Generate all combinations of three edges
    for removed_edges in itertools.combinations(edges, 3):
        # Create a copy of the graph without the removed edges
        new_graph = {node: neighbors.copy() for node, neighbors in graph.items()}
        for edge in removed_edges:
            u, v = edge
            new_graph[u].remove(v)
            new_graph[v].remove(u)

        # Find connected components
        components = []
        visited = set()

        for node in new_graph:
            if node not in visited:
                component = set()

                def dfs(node):
                    visited.add(node)
                    component.add(node)
                    for neighbor in new_graph[node]:
                        if neighbor not in visited:
                            dfs(neighbor)

                dfs(node)
                components.append(component)

        if len(components) == 2:
            sizes = [len(c) for c in components]
            product = sizes[0] * sizes[1]
            if product > max_product:
                max_product = product
                optimal_cut = (removed_edges, sizes)

    return optimal_cut, max_product

def main():
    input_text = """
    jqt: rhn xhk nvd
    rsh: frs pzl lsr
    xhk: hfx
    cmg: qnr nvd lhk bvb
    rhn: xhk bvb hfx
    bvb: xhk hfx
    pzl: lsr hfx nvd
    qnr: nvd
    ntq: jqt hfx bvb xhk
    nvd: lhk
    lsr: lhk
    rzs: qnr cmg lsr rsh
    frs: qnr lhk lsr
    """
    input_lines = input_text.strip().split('\n')
    
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    print(file_path)

    with open(directory+'input.txt', 'r') as file:
        input_lines = file.readlines()

    graph = parse_graph(input_lines)
    optimal_cut, max_product = find_optimal_cut(graph)

    if optimal_cut:
        removed_edges, sizes = optimal_cut
        print(f"Edges to remove: {removed_edges}")
        print(f"Group sizes: {sizes}")
        print(f"Product of group sizes: {max_product}")
    else:
        print("No valid cut found.")

if __name__ == "__main__":
    main()
