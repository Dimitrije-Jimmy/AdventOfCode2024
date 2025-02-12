import os
import heapq
import pprint as pp

def read_input(file_path):
    """Reads the input and parses it into a list of (x, y) coordinates."""
    with open(file_path, 'r') as f:
        input_text = f.read()
    return input_text

def parse_input(input_text):
    """
    Parses the input into towel patterns and desired designs.
    
    Args:
        input_text (str): The raw input text.
    
    Returns:
        tuple: (set of towel patterns, list of desired designs)
    """
    parts = input_text.strip().split("\n\n")
    towel_patterns = set(parts[0].split(", "))
    desired_designs = parts[1].split("\n")
    return towel_patterns, desired_designs


def can_form_design(design, towel_patterns, memo):
    """
    Determines if a design can be formed using the available towel patterns.
    
    Args:
        design (str): The desired design to form.
        towel_patterns (set): Set of available towel patterns.
        memo (dict): Memoization dictionary for storing results.
    
    Returns:
        bool: True if the design can be formed, False otherwise.
    """
    if design in memo:
        return memo[design]
    
    if design == "":
        return True  # Empty design can always be formed.
    
    for pattern in towel_patterns:
        if design.startswith(pattern):
            remainder = design[len(pattern):]
            if can_form_design(remainder, towel_patterns, memo):
                memo[design] = True
                return True
    
    memo[design] = False
    return False


def count_possible_designs(towel_patterns, desired_designs):
    """
    Counts how many desired designs can be formed using the available towel patterns.
    
    Args:
        towel_patterns (set): Set of available towel patterns.
        desired_designs (list): List of desired designs.
    
    Returns:
        int: The number of designs that can be formed.
    """
    memo = {}
    count = 0
    for design in desired_designs:
        if can_form_design(design, towel_patterns, memo):
            count += 1
    return count


def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')

    # Read and parse the input
    input_text = read_input(file_path)

    # Parse input
    towel_patterns, desired_designs = parse_input(input_text)

    # Count possible designs
    result = count_possible_designs(towel_patterns, desired_designs)
    print(f"Number of possible designs: {result}")


if __name__ == "__main__":
    main()
