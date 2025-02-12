import os
import numpy as np

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

    evaluated_dict = {}
    total = 0
    for key, numbers in grid.items():
        evaluated_results = generate_and_evaluate(numbers)
        evaluated_dict[key] = evaluated_results
        print(f"Key: {key}")
        for ops, value in evaluated_results:
            # Construct the expression string for display
            #expression = f"{numbers[0]}"
            #for op, num in zip(ops, numbers[1:]):
            #    expression += f" {op} {num}"
            #print(f"  {expression} = {value}")
            if value == key:
                total += key
                break
        #print()  # Blank line for readability
    
    print(f"Total: {total}")
    #303876483687
    #303876483687
    #303876483687
    #303876483687
    #303876513451
    #303876513451

if __name__ == "__main__":
    main()