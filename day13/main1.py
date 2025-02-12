import numpy as np
import os
import re
import sys

def read_regex(file_path):
    with open(file_path, 'r') as file:
        input_string = file.read()

    # Define the regex pattern with named groups
    pattern = r"""
        (?P<A>Button A: X+(\d{1,2}), Y+(\d{1,2}))   # Matches mul(X,Y)
        |                                      # OR
        (?P<B>Button B: X+(\d{1,2}), Y+(\d{1,2}))                         # Matches do()
        |                                      # OR
        (?P<X>Prize: X=(\d{1,5}), Y=(\d{1,5}))   # Matches Prize: X=X, Y=Y
    """
    regex = re.compile(pattern, re.VERBOSE)

    a, b = 3, 1

    for match in regex.finditer(input_string):
        if match.group('do'):
            continue

    return regex


def main():
    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    file_path = directory+'input2.txt'    
    print(file_path)
    
    read_regex(file_path)
