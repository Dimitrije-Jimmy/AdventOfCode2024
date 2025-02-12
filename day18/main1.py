import os
import pprint as pp
import heapq

def read_input(file_path):
    """
    Reads the input file and parses the warehouse map and movement sequence.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (grid, moves)
            - grid (list of list of str): 2D grid representing the warehouse.
            - moves (str): String of movement directions.
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        #print(lines)
    
    coords = [tuple(map(int, coord.split(','))) for coord in lines]
    #print(coords)
    return coords


def make_grid(coords, bytes, width, height):
    grid = [['.' for _ in range(width+1)] for _ in range(height+1)]
    #for x, y in coords:
    #    grid[y][x] = '#'
    for i in range(bytes):
        x, y = coords[i]
        grid[y][x] = '#'
    return grid

DIRECTIONS = ['N', 'E', 'S', 'W']
DIR_VECTORS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}

def dijkstra(grid, start_pos, end_pos):
    """
    Performs Dijkstra's algorithm to find the lowest score path from Start to End.

    Args:
        grid (list of list of str): 2D grid representing the warehouse.
        start_pos (tuple): (x, y) coordinates of the Start tile.
        end_pos (tuple): (x, y) coordinates of the End tile.

    Returns:
        int: The lowest total score to reach End from Start.
    """
    # Initialize the priority queue
    heap = []
    # Initial state: cost=0, position=start_pos, facing East
    initial_dir = 'E'
    heapq.heappush(heap, (0, start_pos[0], start_pos[1], initial_dir))

    # Visited dictionary: (x, y, direction) -> cost
    visited = {}

    while heap:
        cost, x, y, direction = heapq.heappop(heap)

        # If reached the end, return the cost
        if (x, y) == end_pos:
            return cost

        # If this state has been visited with a lower cost, skip
        state = (x, y, direction)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        # Explore possible actions

        # 1. Move Forward
        dx, dy = DIR_VECTORS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            target_cell = grid[new_y][new_x]
            if target_cell != '#':  # Can move forward
                heapq.heappush(heap, (cost + 1, new_x, new_y, direction))

        # 2. Rotate Clockwise
        new_dir = rotate(direction, 'CW')
        heapq.heappush(heap, (cost + 1000, x, y, new_dir))

        # 3. Rotate Counterclockwise
        new_dir = rotate(direction, 'CCW')
        heapq.heappush(heap, (cost + 1000, x, y, new_dir))

    # If End is unreachable
    return -1



def main():
    """
    Main function to execute the solution.
    """
    # Define the input file path
    # Adjust the path as necessary
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    file_path = os.path.join(directory, 'input2.txt')

    # Read and parse the input
    coords = read_input(file_path)
    print(coords) 

    # Define the grid size
    width = 70
    height = 70

    # Make the grid
    width = 6
    height = 6
    grid = make_grid(coords, 12, width, height)
    pp.pprint(grid)


if __name__ == "__main__":
    main()