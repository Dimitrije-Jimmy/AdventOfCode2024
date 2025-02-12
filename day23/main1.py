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
        if a not in adjacency:
            adjacency[a] = set()
        if b not in adjacency:
            adjacency[b] = set()
        adjacency[a].add(b)
        adjacency[b].add(a)
    return adjacency

def find_triangles(adjacency):
    """
    Finds all unique triangles (fully connected trios) in the network.
    
    Args:
    - adjacency (dict): Adjacency list of the network.
    
    Returns:
    - list of tuple: Each tuple contains three computer names forming a triangle.
    """
    triangles = set()
    # Iterate over all combinations of three computers
    for trio in combinations(adjacency.keys(), 3):
        a, b, c = trio
        # Check if all pairs are connected
        if b in adjacency[a] and c in adjacency[a] and c in adjacency[b]:
            # Sort the trio to avoid duplicates
            sorted_trio = tuple(sorted(trio))
            triangles.add(sorted_trio)
    return list(triangles)

def count_triangles_with_t(triangles):
    """
    Counts how many triangles contain at least one computer starting with 't'.
    
    Args:
    - triangles (list of tuple): List of triangles.
    
    Returns:
    - int: Count of triangles with at least one 't' computer.
    """
    count = 0
    for trio in triangles:
        if any(computer.startswith('t') for computer in trio):
            count += 1
    return count

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
        if a not in adjacency:
            adjacency[a] = set()
        if b not in adjacency:
            adjacency[b] = set()
        adjacency[a].add(b)
        adjacency[b].add(a)
    return adjacency

def find_triangles(adjacency):
    """
    Finds all unique triangles (fully connected trios) in the network.
    
    Args:
    - adjacency (dict): Adjacency list of the network.
    
    Returns:
    - list of tuple: Each tuple contains three computer names forming a triangle.
    """
    triangles = set()
    # Iterate over all combinations of three computers
    for trio in combinations(adjacency.keys(), 3):
        a, b, c = trio
        # Check if all pairs are connected
        if b in adjacency[a] and c in adjacency[a] and c in adjacency[b]:
            # Sort the trio to avoid duplicates
            sorted_trio = tuple(sorted(trio))
            triangles.add(sorted_trio)
    return list(triangles)

def count_triangles_with_t(triangles):
    """
    Counts how many triangles contain at least one computer starting with 't'.
    
    Args:
    - triangles (list of tuple): List of triangles.
    
    Returns:
    - int: Count of triangles with at least one 't' computer.
    """
    count = 0
    for trio in triangles:
        if any(computer.startswith('t') for computer in trio):
            count += 1
    return count

def main():
    """Main function to execute the solution."""
    import os
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    # Replace 'input.txt' with your actual input file if different
    file_path = os.path.join(directory, 'input.txt')  
    #file_path = os.path.join(directory, 'input2.txt')  
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist in the current directory.")
        return
    
    # Read the network map from the file
    with open(file_path, 'r') as file:
        network_map = [line.strip() for line in file if line.strip()]
    
    # Parse the network map
    adjacency = parse_network_map(network_map)
    
    # Find all triangles
    triangles = find_triangles(adjacency)
    
    print(f"Total sets of three interconnected computers: {len(triangles)}")
    
    # Count triangles with at least one 't' computer
    count_with_t = count_triangles_with_t(triangles)
    
    print(f"Sets containing at least one computer starting with 't': {count_with_t}")

if __name__ == "__main__":
    main()