import networkx as nx
import itertools

def parse_graph_networkx(input_lines):
    G = nx.Graph()
    for line in input_lines:
        if line.strip():
            node, neighbors = line.strip().split(':')
            node = node.strip()
            neighbor_nodes = neighbors.strip().split()
            for neighbor in neighbor_nodes:
                neighbor = neighbor.strip()
                if neighbor:
                    G.add_edge(node, neighbor)
    return G

def find_cuts_of_size_k(G, k):
    # Find all edge cuts of size k
    # For large graphs, this may not be feasible directly
    # Instead, use approximation or heuristics
    # Since we need exactly a cut of size 3, we can attempt to find one using edge connectivity
    edge_connectivity = nx.edge_connectivity(G)
    print(f"Edge connectivity of the graph: {edge_connectivity}")

    if edge_connectivity < k:
        print(f"The graph can be disconnected by removing less than {k} edges.")
        return None, None

    # Use NetworkX function to find edge cuts
    # For small k, this is acceptable
    cuts = []
    # Generate all combinations of edges
    edges = list(G.edges())
    for removed_edges in itertools.combinations(edges, k):
        H = G.copy()
        H.remove_edges_from(removed_edges)
        components = list(nx.connected_components(H))
        if len(components) == 2:
            sizes = [len(c) for c in components]
            product = sizes[0] * sizes[1]
            cuts.append((removed_edges, sizes, product))
    return cuts

def find_optimal_cut_networkx(G, k=3):
    cuts = find_cuts_of_size_k(G, k)
    if not cuts:
        return None, None
    # Select the cut with the maximum product of component sizes
    optimal_cut = max(cuts, key=lambda x: x[2])
    removed_edges, sizes, product = optimal_cut
    return removed_edges, sizes, product

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    file_path = directory+'input.txt'

    # Read input from 'input.txt' file
    with open(file_path, 'r') as file:
        input_lines = file.readlines()

    G = parse_graph_networkx(input_lines)
    k = 3  # Number of edges to remove

    removed_edges, sizes, product = find_optimal_cut_networkx(G, k)

    if removed_edges:
        print(f"Edges to remove: {removed_edges}")
        print(f"Group sizes: {sizes}")
        print(f"Product of group sizes: {product}")
    else:
        print(f"No valid cut found by removing {k} edges.")

if __name__ == "__main__":
    main()
