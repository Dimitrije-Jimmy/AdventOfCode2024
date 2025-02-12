import re
import numpy as np

def read_grid(file_path):
    """
    Reads the grid from the input file and returns it as a list of uppercase strings.
    """
    with open(file_path, 'r') as f:
        grid = [line.strip().upper() for line in f if line.strip()]
    return grid

def get_diagonals(grid):
    """
    Extracts all diagonals (both directions) from the grid that are at least as long as the target word.
    """
    array = np.array([list(row) for row in grid])
    rows, cols = array.shape

    # Top-left to bottom-right diagonals
    diags = [array.diagonal(i) for i in range(-rows + 1, cols)]
    diags = [''.join(diag) for diag in diags if len(diag) >= 4]

    # Top-right to bottom-left diagonals
    diags_rev = [np.fliplr(array).diagonal(i) for i in range(-rows + 1, cols)]
    diags_rev = [''.join(diag) for diag in diags_rev if len(diag) >= 4]

    return diags + diags_rev

def count_occurrences(lines, word):
    """
    Counts the number of times 'word' and its reverse appear in the provided lines.
    """
    count = 0
    pattern_forward = re.compile(re.escape(word))
    pattern_backward = re.compile(re.escape(word[::-1]))
    
    for line in lines:
        # Search forward
        count += len(pattern_forward.findall(line))
        # Search backward
        count += len(pattern_backward.findall(line))
    return count

def count_xmas_in_grid(grid, word="XMAS"):
    """
    Counts all occurrences of 'word' in the grid in all eight directions.
    """
    total_count = 0
    
    # 1. Horizontal lines (left to right)
    horizontal = grid
    total_count += count_occurrences(horizontal, word)
    
    # 2. Vertical lines (top to bottom)
    vertical = [''.join(col) for col in zip(*grid)]
    total_count += count_occurrences(vertical, word)
    
    # 3. Diagonal lines
    diagonals = get_diagonals(grid)
    total_count += count_occurrences(diagonals, word)
    
    return total_count

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    print(file_path)
    
    grid = read_grid(file_path)
    total_xmas = count_xmas_in_grid(grid, "XMAS")
    print(f"The word 'XMAS' appears {total_xmas} times in the word search.")

if __name__ == "__main__":
    main()
