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

def evaluate_reverse_recursive(numbers, target, debug=False):
    """
    Recursively evaluate if the target can be derived by reversing operations
    (subtracting or dividing) starting from the rightmost number.

    Args:
        numbers (list of int): The list of numbers.
        target (int): The target test value.
        debug (bool): If True, print debugging information.

    Returns:
        bool: True if the target can be derived, False otherwise.
    """
    # Base case: if there's only one number left, check if it matches the target
    if len(numbers) == 1:
        if debug:
            print(f"Base case: {numbers[0]} == {target}")
        return numbers[0] == target

    # Recursive case: try subtracting or dividing the last number
    last_number = numbers[-1]
    remaining_numbers = numbers[:-1]

    # Subtract last number
    if evaluate_reverse_recursive(remaining_numbers, target + last_number, debug):
        if debug:
            print(f"Match found by subtraction: {remaining_numbers} -> {target} + {last_number}")
        return True

    # Divide by last number (ensure no division by zero and integer division holds)
    if last_number != 0 and target % last_number == 0:
        if evaluate_reverse_recursive(remaining_numbers, target // last_number, debug):
            if debug:
                print(f"Match found by division: {remaining_numbers} -> {target} // {last_number}")
            return True

    return False

def calculate_total_recursive(file_path, debug=False):
    """
    Calculate the total sum of valid test values using recursive evaluation.

    Args:
        file_path (str): Path to the input file.
        debug (bool): If True, print debugging information.

    Returns:
        int: Total sum of valid test values.
    """
    equations = read_file(file_path)
    total = 0

    for test_value, numbers in equations.items():
        if debug:
            print(f"Checking {test_value}: {numbers}")
        if evaluate_reverse_recursive(numbers, test_value, debug):
            if debug:
                print(f"Valid test value: {test_value}")
            total += test_value
        elif debug:
            print(f"Invalid test value: {test_value}")

    return total

def main():
    """
    Main function to execute the calibration check.
    """
    import os
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(directory, 'input.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    file_path = os.path.join(directory, 'input2.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    
    total = calculate_total_recursive(file_path, debug=True)
    print(f"\nTotal calibration result: {total}")

if __name__ == "__main__":
    main()
