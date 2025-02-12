import networkx as nx
import os

def parse_network_map(connections):
    """
    Parses the network connections into an undirected graph.
    
    Args:
    - connections (list of str): Each string represents a connection in the format 'A-B'.
    
    Returns:
    - networkx.Graph: An undirected graph representing the network.
    """
    G = nx.Graph()
    for connection in connections:
        a, b = connection.strip().split('-')
        G.add_edge(a, b)
    return G

def find_maximum_clique(G):
    """
    Finds the largest clique in the graph.
    
    Args:
    - G (networkx.Graph): The network graph.
    
    Returns:
    - list of str: The nodes forming the maximum clique.
    """
    cliques = list(nx.find_cliques(G))
    max_clique = []
    max_size = 0
    for clique in cliques:
        if len(clique) > max_size:
            max_size = len(clique)
            max_clique = clique
    return max_clique

def generate_password(clique):
    """
    Generates the password by sorting the clique's computer names and joining them with commas.
    
    Args:
    - clique (list of str): The nodes forming the maximum clique.
    
    Returns:
    - str: The password.
    """
    sorted_clique = sorted(clique)
    password = ','.join(sorted_clique)
    return password

def main():
    """Main function to execute the solution."""
    import os
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    # Replace 'input.txt' with your actual input file if different
    file_path = os.path.join(directory, 'input.txt')  
    file_path = os.path.join(directory, 'input2.txt')  
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist in the current directory.")
        return
    
    # Read the network map from the file
    with open(file_path, 'r') as file:
        connections = [line.strip() for line in file if line.strip()]
    
    # Parse the network map into a graph
    G = parse_network_map(connections)
    
    # Find the maximum clique
    max_clique = find_maximum_clique(G)
    
    # Generate the password
    password = generate_password(max_clique)
    
    print(f"Largest fully connected set (clique): {sorted(max_clique)}")
    print(f"Password to enter the LAN party: {password}")

if __name__ == "__main__":
    main()
