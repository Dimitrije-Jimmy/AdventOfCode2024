def read_grid(puzzle_input):
    grid = [list(line.strip()) for line in puzzle_input.strip().split('\n') if line.strip()]
    return grid

#def read_grid(file_path):
#    """
#    Reads the grid from the input file and returns it as a list of uppercase strings.
#    """
#    with open(file_path, 'r') as f:
#        grid = [line.strip().upper() for line in f if line.strip()]
#    return grid
"""
M.M
.A.
S.S

M.S
.A.
M.S

S.S
.A.
M.M

S.M
.A.
S.M
"""
def count_xmas_occurrences(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Define the four patterns
    patterns = [
        # Pattern 1
        [('M', -1, -1), ('M', -1, 1), ('S', 1, -1), ('S', 1, 1)],
        # Pattern 2
        [('M', -1, -1), ('S', -1, 1), ('M', 1, -1), ('S', 1, 1)],
        # Pattern 3
        [('S', -1, -1), ('S', -1, 1), ('M', 1, -1), ('M', 1, 1)],
        # Pattern 4
        [('S', -1, -1), ('M', -1, 1), ('S', 1, -1), ('M', 1, 1)],
    ]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'A':
                for pattern in patterns:
                    found = True
                    for expected_char, dr, dc in pattern:
                        nr = row + dr
                        nc = col + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr][nc] != expected_char:
                                found = False
                                break
                        else:
                            found = False
                            break
                    if found:
                        count += 1
    return count

def main():
    # Replace the puzzle_input with your actual puzzle input
    puzzle_input = """
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """

    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    print(file_path)

    with open(file_path, 'r') as file:
        puzzle_input = file.read()

    grid = read_grid(puzzle_input)
    total_occurrences = count_xmas_occurrences(grid)
    print(f"The X-MAS pattern appears {total_occurrences} times in the word search.")

if __name__ == "__main__":
    main()
