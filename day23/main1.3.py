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
        # Split the connection into two computers
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
            # Sort the trio to avoid duplicates (e.g., (A,B,C) same as (B,A,C))
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
        # Check if any computer in the trio starts with 't' or 'T'
        if any(computer.lower().startswith('t') for computer in trio):
            count += 1
    return count

def main():
    """Main function to execute Part One of the solution."""
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

    # Find all triangles in the network
    triangles = find_triangles(adjacency)

    # Count triangles that include at least one computer starting with 't'
    count_with_t = count_triangles_with_t(triangles)

    # Output the results
    print(f"Total sets of three interconnected computers: {len(triangles)}")
    print(f"Sets containing at least one computer starting with 't': {count_with_t}")

if __name__ == "__main__":
    main()
