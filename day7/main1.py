import os
import numpy as np

def read_file(file_path):
    my_dict = {}
    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                # Remove leading/trailing whitespace
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue
                
                # Split the line into key and values parts
                if ':' not in line:
                    print(f"Warning: Line {line_number} is missing a ':' delimiter. Skipping line.")
                    continue  # Skip lines without the expected format
                
                key_part, values_part = line.split(':', 1)  # Split only on the first ':'
                
                try:
                    key = int(key_part.strip())  # Convert key to integer
                except ValueError:
                    print(f"Warning: Key '{key_part}' on line {line_number} is not an integer. Skipping line.")
                    continue  # Skip lines with non-integer keys
                
                # Split the values_part into individual strings and convert to integers
                try:
                    # Handle cases where there might be multiple spaces or tabs
                    values = [int(value) for value in values_part.strip().split()]
                except ValueError as e:
                    print(f"Warning: One of the values on line {line_number} is not an integer. Skipping line.")
                    continue  # Skip lines with non-integer values
                
                my_dict[key] = values
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return my_dict

def read_file2(file_path):
    my_dict = {}
    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            key_part, values_part = line.split(':', 1)
            key = int(key_part.strip())
            values = [int(value) for value in values_part.strip().split()]
            my_dict[key] = values
    return my_dict

from itertools import product

def generate_and_evaluate(numbers):
    if not numbers:
        return []
    
    if len(numbers) == 1:
        return [([], numbers[0])]
    
    ops = ['+', '*']
    n = len(numbers) - 1
    results = []
    
    # Generate all possible combinations of operations
    for op_comb in product(ops, repeat=n):
        # Evaluate the expression from left to right
        result = numbers[0]
        for op, num in zip(op_comb, numbers[1:]):
            if op == '+':
                result += num
            elif op == '*':
                result *= num
        results.append((op_comb, result))
    
    return results
def test_generate_and_evaluate():
    numbers = [81, 40, 27]
    results = generate_and_evaluate(numbers)
    for ops, value in results:
        # Construct the expression string for display
        expression = f"{numbers[0]}"
        for op, num in zip(ops, numbers[1:]):
            expression += f" {op} {num}"
        print(f"{expression} = {value}")

def step(key, numbers):
    results = generate_and_evaluate(numbers)
    is_right = False
    for ops, value in results:
        if value == key:
            is_right = True
            break
    return is_right


def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input2.txt'
    file_path = directory+'input.txt'

    grid = read_file2(file_path)
    print(grid)

    total = 0
    for key, values in grid.items():
        is_right = step(key, values)
        if is_right:
            total += key
    print(total)

if __name__ == "__main__":
    main()