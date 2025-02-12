def read_map(file_path):
    with open(file_path, 'r') as f:
        grid = [list(line.strip()) for line in f if line.strip()]
    return grid

def compute_density(grid):
    total_positions = 0
    garden_plots = 0
    for row in grid:
        for cell in row:
            if cell == '.' or cell == 'S':
                garden_plots += 1
            total_positions += 1
    density = garden_plots / total_positions
    return density

def calculate_reachable_plots(N, density):
    total_positions = 2 * N * (N + 1) + 1
    reachable_plots = density * total_positions
    return int(round(reachable_plots))

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    file_path = directory+'input.txt'

    grid = read_map(file_path)
    density = compute_density(grid)
    print(f"Density of garden plots: {density}")
    N = 26501365
    #N = 5000
    #N = 6
    reachable_plots = calculate_reachable_plots(N, density)
    print(f"The Elf can reach {reachable_plots} garden plots in exactly {N} steps.")

if __name__ == "__main__":
    main()
