import os
from collections import defaultdict

def read_input(file_path):
    """Reads the input file contents."""
    with open(file_path, 'r') as f:
        return f.read()

def parse_input(input_text):
    """
    Parses the input into:
        input_vals: dict of wire -> int (0 or 1) that are initially known
        logic_gates: list of (input1, gate_op, input2, output_wire)
    """
    parts = input_text.strip().split("\n\n")
    # First section (initial wire values)
    input_strs = parts[0].split("\n")
    input_vals = {}
    for line in input_strs:
        wire_name, val_str = line.split(": ")
        input_vals[wire_name] = int(val_str)
    # Second section (logic gates)
    logic_lines = parts[1].strip().split("\n")
    logic_gates = []
    for line in logic_lines:
        left_side, result = line.split(" -> ")
        # Example: "x00 AND y00 -> z00" => input1='x00', gate_op='AND', input2='y00'
        split_left = left_side.split()
        if len(split_left) == 3:
            input1, gate_op, input2 = split_left
        else:
            raise ValueError(f"Unexpected gate line format: {line}")
        logic_gates.append((input1, gate_op, input2, result))
    return input_vals, logic_gates

def apply_gate_op(val1, gate_op, val2):
    """Applies a single gate operation: AND, OR, XOR, etc."""
    if gate_op == "AND":
        return val1 & val2
    elif gate_op == "OR":
        return val1 | val2
    elif gate_op == "XOR":
        return val1 ^ val2
    else:
        raise ValueError(f"Unsupported gate operation: {gate_op}")

def process_all_logic_gates(input_vals, logic_gates):
    """
    Iteratively try to process all gates until no progress can be made.
    Moves gates that cannot be processed yet (due to unknown inputs)
    into a `remaining_gates` list, and tries them again on subsequent passes.
    """
    remaining_gates = logic_gates[:]
    processed_something = True
    
    while processed_something and remaining_gates:
        processed_something = False
        new_remaining = []
        
        for gate in remaining_gates:
            input1, gate_op, input2, output_wire = gate
            
            # Check if we know both inputs
            if input1 in input_vals and input2 in input_vals:
                # We can process this gate
                val1 = input_vals[input1]
                val2 = input_vals[input2]
                output_val = apply_gate_op(val1, gate_op, val2)
                input_vals[output_wire] = output_val
                processed_something = True
            else:
                # We have to wait until we know both input1 and input2
                new_remaining.append(gate)
        
        remaining_gates = new_remaining
    
    # If there are still gates left in remaining_gates, it typically means
    # we could not resolve them (maybe missing input wires?). For AoC puzzle,
    # usually this means all wires will eventually be known, so ideally 
    # remaining_gates should end up empty.
    
    return input_vals

def extract_z_bits_as_decimal(input_vals):
    """
    Combine wires that start with 'z' into a binary string:
      z00 is least significant bit (LSB),
      z01 is next, etc.
    Convert that binary string to a decimal number and return it.
    """
    # Collect 'z' wires
    z_wires = [w for w in input_vals if w.startswith('z')]
    # Sort them by numeric part (z00, z01, z02, ...)
    # so that z00 is least significant bit, z01 is next, etc.
    z_wires.sort(key=lambda w: int(w[1:]))  # Convert e.g. z00 -> 00 -> int(0)
    
    # Build the binary number (note that z00 is LSB, so we want z00 to be
    # at the right end of the binary string)
    # But typically strings are built left-to-right with the LSB at the far right,
    # so we can just append in ascending order, then reverse at the end or
    # append to an array and reverse. Another approach is to build from left to right
    # but read it in reverse to interpret it. 
    # Below, we’ll just build from the left with z00 last:
    
    bits = []
    for wire in reversed(z_wires):
        bits.append(str(input_vals[wire]))
    # bits[0] is the highest bit, bits[-1] is the LSB (z00).
    # We want a binary string with the highest bit on the left.
    # So let's do: bits = reversed(z_wires) => zWires from highest to lowest
    # Then bits as string is top -> bottom
    # Actually, let's simplify by building from z00 -> zNN left to right, and at the end we reverse it:
    
    # Actually let's do it this simpler way:
    # z_wires is sorted ascending: z00, z01, z02, ...
    # We want z00 to be the rightmost bit in a typical binary representation.
    # So we can do:
    bin_str = ''
    for wire in reversed(z_wires):
        bin_str += str(input_vals[wire])
    # Now bin_str[0] is the highest bit and bin_str[-1] is the lowest bit
    # to interpret it properly, let's reverse it again:
    #bin_str = bin_str[::-1]  # Now z00 is least significant (rightmost)
    
    decimal_val = int(bin_str, 2) if bin_str else 0
    return bin_str, decimal_val

def extract_key_bits_as_decimal(input_vals, key):
    """
    Combine wires that start with 'key' into a binary string:
      z00 is least significant bit (LSB),
      z01 is next, etc.
    Convert that binary string to a decimal number and return it.
    """
    # Collect 'key' wires
    key_wires = [w for w in input_vals if w.startswith(key)]
    key_wires.sort(key=lambda w: int(w[1:]))  
    

    bin_str = ''
    for wire in reversed(key_wires):
        bin_str += str(input_vals[wire])

    decimal_val = int(bin_str, 2) if bin_str else 0
    return bin_str, decimal_val

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input4.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')
    
    # Read the puzzle input
    input_text = read_input(file_path)
    
    # Parse into known wire values + gates
    input_vals, logic_gates = parse_input(input_text)
    
    # Process until no more gates can be resolved
    input_vals = process_all_logic_gates(input_vals, logic_gates)
    
    # Finally, convert the wires that start with 'z' to a decimal number
    x_bin, x_dec = extract_key_bits_as_decimal(input_vals, 'x')
    y_bin, y_dec = extract_key_bits_as_decimal(input_vals, 'y')
    binary_result, decimal_result = extract_z_bits_as_decimal(input_vals)
    
    print(f"Binary output from x-wires = {x_bin}")
    print(f"Decimal output = {x_dec}")
    print(f"Binary output from y-wires = {y_bin}")
    print(f"Decimal output = {y_dec}")

    print(x_dec + y_dec)

    print(f"Binary output from z-wires = {binary_result}")
    print(f"Decimal output = {decimal_result}")

if __name__ == "__main__":
    main()
