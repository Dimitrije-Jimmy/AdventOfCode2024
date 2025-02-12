import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)

import re

def calculate_mul_sum_with_state(input_string):
    # Define the regex pattern with named groups
    pattern = r"""
        (?P<mul>mul\((\d{1,3}),(\d{1,3})\))   # Matches mul(X,Y)
        |                                      # OR
        (?P<do>do\(\))                         # Matches do()
        |                                      # OR
        (?P<dont>don't\(\))                    # Matches don't()
    """
    regex = re.compile(pattern, re.VERBOSE)
    
    # Initial state: mul instructions are enabled
    is_enabled = True
    total_sum = 0

    # Iterate over all matches in order
    for match in regex.finditer(input_string):
        if match.group('do'):
            is_enabled = True
            print("do() encountered: mul instructions enabled")
        elif match.group('dont'):
            is_enabled = False
            print("don't() encountered: mul instructions disabled")
        elif match.group('mul'):
            # Extract the numbers
            x_str, y_str = match.group(2), match.group(3)
            x = int(x_str)
            y = int(y_str)
            product = x * y
            if is_enabled:
                total_sum += product
                print(f"mul({x},{y}) = {product} (Enabled)")
            else:
                print(f"mul({x},{y}) = {product} (Disabled)")
    print(f"\nTotal Sum: {total_sum}")
    return total_sum

# Example usage with sample input
input_string = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

with open(file_path, 'r') as file:
    input_string = file.read()
calculate_mul_sum_with_state(input_string)
