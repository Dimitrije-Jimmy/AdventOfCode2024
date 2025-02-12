import networkx as nx

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
        connections = [line.strip() for line in file if line.strip()]
    
    # Create an undirected graph
    G = nx.Graph()
    for connection in connections:
        a, b = connection.split('-')
        G.add_edge(a, b)
    
    # Find all triangles using NetworkX
    triangles = list(nx.enumerate_all_cliques(G))
    triangles = [clique for clique in triangles if len(clique) == 3]
    
    print(f"Total sets of three interconnected computers: {len(triangles)}")
    
    # Count triangles with at least one 't' computer
    count_with_t = 0
    for trio in triangles:
        if any(computer.startswith('t') for computer in trio):
            count_with_t += 1
    
    print(f"Sets containing at least one computer starting with 't': {count_with_t}")

if __name__ == "__main__":
    main()
