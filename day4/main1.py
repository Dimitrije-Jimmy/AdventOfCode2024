import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)


def read_grid(puzzle_input):
    grid = []
    for line in puzzle_input.strip().split('\n'):
        grid.append(list(line.strip()))
    return grid

def count_word_occurrences(grid, word):
    rows = len(grid)
    cols = len(grid[0])
    word_length = len(word)
    count = 0

    # Directions: (row_delta, col_delta)
    directions = [
        (-1, 0),  # Up
        (-1, 1),  # Up-Right
        (0, 1),   # Right
        (1, 1),   # Down-Right
        (1, 0),   # Down
        (1, -1),  # Down-Left
        (0, -1),  # Left
        (-1, -1), # Up-Left
    ]

    for row in range(rows):
        for col in range(cols):
            for dr, dc in directions:
                found = True
                for k in range(word_length):
                    nr = row + dr * k
                    nc = col + dc * k
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] != word[k]:
                            found = False
                            break
                    else:
                        found = False
                        break
                if found:
                    count += 1
    return count

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

    with open(file_path, 'r') as file:
        puzzle_input = file.read()

    grid = read_grid(puzzle_input)
    word = "XMAS"
    total_occurrences = count_word_occurrences(grid, word)
    print(f"The word '{word}' appears {total_occurrences} times in the word search.")

if __name__ == "__main__":
    main()
