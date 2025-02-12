import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)

import re

def calculate_mul_sum(input_string):
    # Define the regex pattern
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'

    # Find all matches
    matches = re.findall(pattern, input_string)

    total_sum = 0

    # Iterate over the matches and compute the sum
    for x_str, y_str in matches:
        x = int(x_str)
        y = int(y_str)
        product = x * y
        total_sum += product
        print(f"mul({x},{y}) = {product}")

    print(f"\nTotal Sum: {total_sum}")
    return total_sum

# Example usage with your sample input
input_string = "[why()what()]:!*<)~mul(929,350)({)when()@mul(878,389)}$!? mul(786,950)~when();[(#mul(808,160)mul(659,500)&+?*mul(659,863)~~&:;,>do()(%@from()^!how()how()'@mul(281,23)"
with open(file_path, 'r') as file:
    input_string = file.read()


calculate_mul_sum(input_string)

def calculate_do_dont(input_string):
    # Define the regex pattern
    pattern1 = r'mul\((\d{1,3}),(\d{1,3})\)'
    pattern2 = r'do\(\)'
    pattern3 = r'don\'t\(\)'

    # Find all matches
    matches1 = re.findall(pattern1, input_string)
    matches2 = re.findall(pattern2, input_string)
    matches3 = re.findall(pattern3, input_string)

    total_sum = 0

    # Iterate over the matches and compute the sum
    for x_str, y_str in matches1:
        x = int(x_str)
        y = int(y_str)
        product = x * y
        total_sum += product
        print(f"mul({x},{y}) = {product}")

    print(f"\nTotal Sum: {total_sum}")
    return total_sum

#calculate_do_dont(input_string)