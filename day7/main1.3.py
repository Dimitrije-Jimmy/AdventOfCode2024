import os
from itertools import product

def read_file(file_path):
    """
    Reads a file and parses it into a dictionary.

    Each line in the file should be in the format:
    test_value: number1 number2 ... numberN

    Args:
        file_path (str): The path to the input file.

    Returns:
        dict: A dictionary where keys are integers (test_value) and values are lists of integers.
    """
    my_dict = {}
    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                if ':' not in line:
                    print(f"Warning: Line {line_number} is missing a ':' delimiter. Skipping line.")
                    continue
                key_part, values_part = line.split(':', 1)
                try:
                    key = int(key_part.strip())
                except ValueError:
                    print(f"Warning: Key '{key_part}' on line {line_number} is not an integer. Skipping line.")
                    continue
                try:
                    values = [int(value) for value in values_part.strip().split()]
                except ValueError:
                    print(f"Warning: One of the values on line {line_number} is not an integer. Skipping line.")
                    continue
                my_dict[key] = values
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
    return my_dict

def generate_and_evaluate(numbers):
    """
    Generates all possible expressions by inserting '+' or '*' between numbers
    and evaluates them from left to right (ignoring operator precedence).

    Args:
        numbers (list of int): The list of numbers.

    Returns:
        list of int: The list of evaluated results.
    """
    if not numbers:
        return []
    
    if len(numbers) == 1:
        return [numbers[0]]
    
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
        results.append(result)
    
    return results

def main():
    """
    Main function to execute the calibration check.
    """
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(directory, 'input.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    file_path = os.path.join(directory, 'input2.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    
    # Read and parse the input file
    equations = read_file(file_path)
    
    print("Parsed Equations:")
    for key, numbers in equations.items():
        print(f"{key}: {numbers}")
    print("\nEvaluating Equations...\n")
    
    total_calibration = 0
    valid_equations = []
    
    for test_value, numbers in equations.items():
        evaluated_results = generate_and_evaluate(numbers)
        # Check if any of the evaluated results match the test_value
        if test_value in evaluated_results:
            total_calibration += test_value
            valid_equations.append(test_value)
            print(f"Valid: {test_value}: {numbers}")
        else:
            print(f"Invalid: {test_value}: {numbers}")
    
    print("\nSummary:")
    print(f"Valid Test Values: {valid_equations}")
    print(f"Total Calibration Result: {total_calibration}")

if __name__ == "__main__":
    main()
