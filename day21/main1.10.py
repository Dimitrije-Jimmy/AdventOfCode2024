import numpy as np
import os
from collections import deque
import sys

def read_codes(file_path):
    """Reads codes from a file, each code on a separate line."""
    codes = []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.strip()
            if row:
                codes.append(row)
    return codes

def best_path(x1, y1, x2, y2, loc_x, loc_y):
    """
    Computes the optimal path between two points on the keypad grid.
    :param x1, y1: Starting coordinates.
    :param x2, y2: Target coordinates.
    :param loc_x, loc_y: Blocking position for '#' if relevant.
    :return: Optimal path as a string.
    """
    lt, rt = '<' * (y1 - y2), '>' * (y2 - y1)
    up, dn = '^' * (x1 - x2), 'v' * (x2 - x1)

    if loc_x['#'] == min(x1, x2) and loc_y['#'] == min(y1, y2):
        return dn + rt + up + lt + "A"
    elif loc_x['#'] == max(x1, x2) and loc_y['#'] == min(y1, y2):
        return up + rt + dn + lt + "A"
    else:
        return lt + dn + up + rt + "A"

def construct_matrix(grid, loc_x, loc_y):
    """
    Constructs a dynamic cost matrix for transitions on the keypad grid.
    :param grid: Combined grid of both keypads.
    :param loc_x, loc_y: Maps of x and y positions for characters.
    :return: Cost matrix.
    """
    size = len(loc_x)
    cost_matrix = np.zeros((size, size), dtype=int)

    for char1 in loc_x:
        for char2 in loc_x:
            x1, y1 = loc_x[char1], loc_y[char1]
            x2, y2 = loc_x[char2], loc_y[char2]
            cost_matrix[char1][char2] = len(best_path(x1, y1, x2, y2, loc_x, loc_y))

    return cost_matrix

def fast_matrix_exponentiation(matrix, depth):
    """
    Applies fast matrix exponentiation to compute costs at a given recursion depth.
    :param matrix: Base cost matrix.
    :param depth: Target recursion depth.
    :return: Matrix raised to the power of 'depth'.
    """
    return np.linalg.matrix_power(matrix, depth)

def merge_keypads(numeric_keypad, directional_keypad):
    """
    Merges both keypads into a unified grid with shared 'A' button.
    :param numeric_keypad: The numeric keypad.
    :param directional_keypad: The directional keypad.
    :return: Merged grid and updated character positions.
    """
    loc_x, loc_y = {}, {}

    # Merge the numeric keypad
    for i, row in enumerate(numeric_keypad):
        for j, char in enumerate(row):
            if char:
                loc_x[char], loc_y[char] = i, j

    # Offset for the directional keypad
    offset_x, offset_y = len(numeric_keypad), 0

    # Merge the directional keypad
    for i, row in enumerate(directional_keypad):
        for j, char in enumerate(row):
            if char:
                loc_x[char], loc_y[char] = i + offset_x, j + offset_y

    return loc_x, loc_y

def calculate_complexity(grid, codes, loc_x, loc_y):
    """
    Calculates the complexity for a list of codes based on the keypad grid.
    :param grid: The combined grid.
    :param codes: List of codes to process.
    :param loc_x, loc_y: Mappings of character positions.
    :return: Total complexity.
    """
    total_complexity = 0
    cost_matrix = construct_matrix(grid, loc_x, loc_y)

    for code in codes:
        numeric_part = int(code[:-1])  # Extract numeric part, ignoring the trailing 'A'
        depth = len(code) - 1  # Depth is determined by the length of the code

        exp_matrix = fast_matrix_exponentiation(cost_matrix, depth)
        complexity = numeric_part * np.sum(exp_matrix)
        total_complexity += complexity

    return total_complexity

def main():
    numeric_keypad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [None, '0', 'A']
    ]

    directional_keypad = [
        [None, '^', 'A'],
        ['<', 'v', '>'],
        [None, '#', None]  # Add `#` to the grid if necessary
    ]

    # Merge the keypads
    loc_x, loc_y = merge_keypads(numeric_keypad, directional_keypad)

    # Sample codes
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    # Replace 'input.txt' with your actual input file if different
    file_path = os.path.join(directory, 'input.txt')  
    file_path = os.path.join(directory, 'input2.txt')  

    # Read codes from the input file
    codes = read_codes(file_path)
    print("Codes to type:", codes)
    print()
    #codes = ['029A', '980A', '179A', '456A', '379A']

    # Calculate total complexity
    grid = numeric_keypad + directional_keypad  # Unified grid
    total_complexity = calculate_complexity(grid, codes, loc_x, loc_y)

    print(f"Total complexity: {total_complexity}")

if __name__ == "__main__":
    main()