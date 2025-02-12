from itertools import combinations

def parse_network_map(connections):
    """
    Parses the network connections into an adjacency dictionary.

    Args:
    - connections (list of str): Each string represents a connection in the format 'A-B'.

    Returns:
    - dict: A dictionary where keys are computer names, and values are sets of connected computers.
    """
    adjacency = {}
    for connection in connections:
        a, b = connection.strip().split('-')
        
        # Initialize the adjacency sets if not already present
        if a not in adjacency:
            adjacency[a] = set()
        if b not in adjacency:
            adjacency[b] = set()
        
        # Add the connection bidirectionally
        adjacency[a].add(b)
        adjacency[b].add(a)
    return adjacency

def bron_kerbosch(R, P, X, adjacency, cliques):
    """
    Bron–Kerbosch recursive algorithm without pivoting to find all maximal cliques.

    Args:
    - R (set): Current clique.
    - P (set): Potential nodes to expand the clique.
    - X (set): Nodes already processed.
    - adjacency (dict): Adjacency list of the graph.
    - cliques (list): List to store all maximal cliques found.
    """
    if not P and not X:
        cliques.append(R)
        return
    for vertex in list(P):
        bron_kerbosch(R.union({vertex}),
                      P.intersection(adjacency[vertex]),
                      X.intersection(adjacency[vertex]),
                      adjacency,
                      cliques)
        P.remove(vertex)
        X.add(vertex)

def find_maximal_cliques(adjacency):
    """
    Finds all maximal cliques in the network using the Bron–Kerbosch algorithm.

    Args:
    - adjacency (dict): Adjacency list of the network.

    Returns:
    - list of set: Each set contains computer names forming a maximal clique.
    """
    cliques = []
    P = set(adjacency.keys())
    R = set()
    X = set()
    bron_kerbosch(R, P, X, adjacency, cliques)
    return cliques

def find_maximum_clique(cliques):
    """
    Identifies the largest clique(s) from a list of cliques.

    Args:
    - cliques (list of set): List of maximal cliques.

    Returns:
    - list of set: List containing the largest clique(s).
    """
    max_size = 0
    max_cliques = []
    for clique in cliques:
        if len(clique) > max_size:
            max_size = len(clique)
            max_cliques = [clique]
        elif len(clique) == max_size:
            max_cliques.append(clique)
    return max_cliques

def generate_password(clique):
    """
    Generates the password by sorting the clique's computer names and joining them with commas.

    Args:
    - clique (set): The nodes forming the maximum clique.

    Returns:
    - str: The password.
    """
    sorted_clique = sorted(clique)
    password = ','.join(sorted_clique)
    return password

def main_part_two():
    """Main function to execute Part Two of the solution."""
    import os

    # Define the input file name
    input_file = 'input.txt'  # Ensure this file exists in the same directory
    #input_file = 'input2.txt'  # Ensure this file exists in the same directory

    # Determine the script's directory to locate the input file
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, input_file)

    # Check if the input file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{input_file}' does not exist in the directory '{directory}'.")
        return

    # Read the network map from the file
    with open(file_path, 'r') as file:
        network_map = [line.strip() for line in file if line.strip()]

    # Parse the network map into an adjacency dictionary
    adjacency = parse_network_map(network_map)

    # Find all maximal cliques using the Bron–Kerbosch algorithm
    cliques = find_maximal_cliques(adjacency)

    # Identify the largest clique(s)
    max_cliques = find_maximum_clique(cliques)

    # Assuming there's only one maximum clique, select the first one
    # If multiple cliques have the same maximum size, you can handle accordingly
    largest_clique = max_cliques[0] if max_cliques else set()

    # Generate the password
    password = generate_password(largest_clique)

    # Output the results
    print(f"Largest fully connected set (clique): {sorted(largest_clique)}")
    print(f"Password to enter the LAN party: {password}")

if __name__ == "__main__":
    main_part_two()
