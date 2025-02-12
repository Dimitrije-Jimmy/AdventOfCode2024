import os
from collections import defaultdict
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
    input_strs = parts[0].split("\n")
    input_vals = {}
    for str in input_strs:
        input_vals[str.split(": ")[0]] = int(str.split(": ")[1])
    logic_gates_input = parts[1].split("\n")
    logic_gates = []
    for gate in logic_gates_input:
        input, result = gate.split(" -> ")
        input1, logic_gate, input2 = input.split(" ")
        logic_gates.append((input1, logic_gate, input2, result))
    return input_vals, logic_gates

def process_logic_gate(input_vals, one_logic_gate):
    input1, logic_gate, input2, result = one_logic_gate
    val1 = input_vals[input1]
    val2 = input_vals[input2]
    if logic_gate == "AND":
        input_vals[result] = val1 and val2
    elif logic_gate == "OR":
        input_vals[result] = val1 or val2
    elif logic_gate == "NOT":
        input_vals[result] = not val1
    
    return input_vals


def convert_to_int(input_vals):
    result = ''

    sorted_keys = sorted(input_vals.keys())
    for key in sorted_keys:
        if key[0] == 'z':
            result += str(input_vals[key])
    
    return result, int(result)

def main():
    """Main function to execute the solution."""
    # Define the input file path
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')
    file_path = os.path.join(directory, 'input3.txt')

    # Read and parse the input
    input_text = read_input(file_path)

    # Parse input
    input_vals, logic_gates = parse_input(input_text)
    print(input_vals)
    print(logic_gates)

    # Process Logic Gates
    for gate in logic_gates:
        input_vals = process_logic_gate(input_vals, gate)
    print(input_vals)


    # Convert to int
    result, result2 = convert_to_int(input_vals)
    print(f'binary: {result}, decimal: {result2}')

if __name__ == "__main__":
    main()
