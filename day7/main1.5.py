import os
from itertools import product

def read_file(file_path):
    """
    Reads a file and parses it into a dictionary.

    Args:
        file_path (str): Path to the input file.

    Returns:
        dict: A dictionary where keys are integers (test_value) and values are lists of integers.
    """
    my_dict = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                if ':' not in line:
                    continue
                key, values = line.split(':', 1)
                key = int(key.strip())
                values = list(map(int, values.split()))
                my_dict[key] = values
    except Exception as e:
        print(f"Error reading file: {e}")
    return my_dict

def evaluate_intermediate(numbers, test_value):
    """
    Check if the test_value is reached at any intermediate step.

    Args:
        numbers (list of int): List of numbers.
        test_value (int): The test value to check against.

    Returns:
        bool: True if the test_value is reached, False otherwise.
    """
    if len(numbers) == 1:
        return numbers[0] == test_value

    ops = ['+', '*']
    for ops_comb in product(ops, repeat=len(numbers) - 1):
        result = numbers[0]
        if result == test_value:
            return True  # Immediate match
        for op, num in zip(ops_comb, numbers[1:]):
            if op == '+':
                result += num
            elif op == '*':
                result *= num
            if result == test_value:
                return True  # Match at intermediate step
    return False

def calculate_total(file_path):
    """
    Calculate the total sum of valid test values.

    Args:
        file_path (str): Path to the input file.

    Returns:
        int: Total sum of valid test values.
    """
    equations = read_file(file_path)
    total = 0

    for test_value, numbers in equations.items():
        if evaluate_intermediate(numbers, test_value):
            total += test_value

    return total

def main():
    """
    Main function to execute the calibration check.
    """
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(directory, 'input.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    #file_path = os.path.join(directory, 'input2.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    
    
    total = calculate_total(file_path)
    print(f"Total calibration result: {total}")

if __name__ == "__main__":
    main()
