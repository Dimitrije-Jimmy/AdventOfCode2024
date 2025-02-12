import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)

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


def read_grid(puzzle_input):
    grid = []
    for line in puzzle_input.strip().split('\n'):
        grid.append(list(line.strip()))
    return grid

def count_xmas_occurrences(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Directions for diagonals
    # (delta_row, delta_col) pairs
    # Up-Left, Down-Right
    diag1 = [(-1, -1), (1, 1)]
    # Up-Right, Down-Left
    diag2 = [(-1, 1), (1, -1)]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'A':
                # Check Pattern 1: Up-Left 'M', Down-Right 'S'
                if (check_char(grid, row, col, -1, -1, 'M') and
                    check_char(grid, row, col, 1, 1, 'S')):
                    count += 1
                # Check Pattern 2: Up-Left 'S', Down-Right 'M'
                if (check_char(grid, row, col, -1, -1, 'S') and
                    check_char(grid, row, col, 1, 1, 'M')):
                    count += 1
                # Check Pattern 3: Up-Right 'M', Down-Left 'S'
                if (check_char(grid, row, col, -1, 1, 'M') and
                    check_char(grid, row, col, 1, -1, 'S')):
                    count += 1
                # Check Pattern 4: Up-Right 'S', Down-Left 'M'
                if (check_char(grid, row, col, -1, 1, 'S') and
                    check_char(grid, row, col, 1, -1, 'M')):
                    count += 1
    return count

def check_char(grid, row, col, delta_row, delta_col, expected_char):
    rows = len(grid)
    cols = len(grid[0])
    new_row = row + delta_row
    new_col = col + delta_col
    if 0 <= new_row < rows and 0 <= new_col < cols:
        return grid[new_row][new_col] == expected_char
    return False

def main():
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

    grid = read_grid(puzzle_input)
    total_occurrences = count_xmas_occurrences(grid)
    print(f"The X-MAS pattern appears {total_occurrences} times in the word search.")

if __name__ == "__main__":
    main()