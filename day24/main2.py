import os
from collections import defaultdict
from itertools import combinations

def read_input(file_path):
    """Reads the input file contents."""
    with open(file_path, 'r') as f:
        return f.read()

def parse_input(input_text):
    """
    Parses the input into:
        input_vals: dict of wire -> int (0 or 1) that are initially known
        gates: list of (input1, gate_op, input2, output_wire)
    """
    parts = input_text.strip().split("\n\n")
    
    # First part: initial wire values
    input_vals = {}
    for line in parts[0].splitlines():
        wire, val_str = line.split(": ")
        input_vals[wire] = int(val_str)
        
    # Second part: the gates
    gates = []
    for line in parts[1].splitlines():
        left_side, out_wire = line.split(" -> ")
        input1, gate_op, input2 = left_side.split()
        gates.append((input1, gate_op, input2, out_wire))
    
    return input_vals, gates

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

def run_circuit(gates, initial_values, swapped_pairs=None):
    """
    Simulate the circuit.
    
    :param gates: list of (in1, op, in2, out_wire)
    :param initial_values: dict wire -> 0/1 (for x??, y??, or any known wires)
    :param swapped_pairs: list of pairs [(orig_outA, orig_outB), (orig_outC, orig_outD), ...]
                         indicating that the outputs for those gates should be swapped.
    
    :return: a dict of wire -> 0/1 with the final values of all wires.
    """
    # Copy initial values so we don't mutate the original
    wire_values = dict(initial_values)
    
    # We will build a map:  actual_out_wire_for_gate[g] = wire_name
    # so that if gate g is supposed to output wire X but is swapped with gate h that
    # should output wire Y, then we store the reversed wires. 
    #
    # However, we need to identify gates by index or by some ID. 
    # Let's store the gates in an indexed list and the output wire in a separate array.
    # Then if a gate's output is swapped, we modify that mapping.
    
    # Alternatively, we can handle swapping directly after we produce the gate output:
    #    - each gate has an output wire, but if it's swapped, we store it in the other wire.
    
    # Let's do it in a simpler way for demonstration:
    # 1) Identify the out_wire for each gate in original order: gates[i][3]
    # 2) If swapped_pairs includes (out_wire1, out_wire2), we swap them in a dictionary
    #    so that the gate that was originally outputting out_wire1 now outputs out_wire2, and vice versa.

    # Create a map from original wire -> "adjusted" wire
    # Initially it's identity (no swap)
    wire_swap_map = {}
    for _, _, _, out_wire in gates:
        wire_swap_map[out_wire] = out_wire

    # If we have pairs to swap
    if swapped_pairs:
        # swapped_pairs might look like: [('z05', 'z00'), ('z02', 'z01'), ...]
        # but we need to find which gates produce z05, which produce z00, etc.
        # Actually simpler is to say that if a gate tries to write to 'z05', 
        # we redirect it to 'z00' if that's the pair, and vice versa.
        for (w1, w2) in swapped_pairs:
            # For each wire in the map, if wire_swap_map == w1 => set to w2, if == w2 => set to w1
            for orig_out in list(wire_swap_map.keys()):
                if wire_swap_map[orig_out] == w1:
                    wire_swap_map[orig_out] = w2
                elif wire_swap_map[orig_out] == w2:
                    wire_swap_map[orig_out] = w1
    
    # Now do an iterative approach (like Part One) to process gates in multiple passes
    # until no new changes happen or all gates are resolved.
    gates_remaining = gates[:]
    changed = True
    
    while gates_remaining and changed:
        changed = False
        new_remaining = []
        
        for (in1, op, in2, out_wire) in gates_remaining:
            if in1 in wire_values and in2 in wire_values:
                # We can compute the output
                val_out = apply_gate_op(wire_values[in1], op, wire_values[in2])
                # But we store it under the swapped wire name if there's a swap
                actual_out_wire = wire_swap_map[out_wire]
                prev_val = wire_values.get(actual_out_wire, None)
                wire_values[actual_out_wire] = val_out
                
                if prev_val is None or prev_val != val_out:
                    changed = True
            else:
                new_remaining.append((in1, op, in2, out_wire))
        
        gates_remaining = new_remaining
    
    return wire_values

def get_binary_from_wires(wire_values, prefix='z'):
    """
    Collect wires starting with `prefix` (e.g., z??),
    interpret them as a binary number with wire00 as LSB, wire01 next, etc.
    Return an integer.
    """
    # Gather all wires that start with prefix
    wires = [w for w in wire_values if w.startswith(prefix)]
    # Sort them by numeric part
    # e.g. z00, z01, z02 => 0,1,2
    wires.sort(key=lambda w: int(w[1:]))  # remove the prefix letter
    # Build up bits from least significant to most significant
    bits = [wire_values[w] for w in wires]
    # bits[0] is LSB, bits[-1] is MSB
    # Convert to integer
    result = 0
    for i, bit in enumerate(bits):
        if bit:
            result |= (1 << i)
    return result

def check_addition_correctness(gates, swapped_pairs, num_bits=5, test_count=10):
    """
    Randomly test if, for multiple x,y inputs (each up to num_bits bits),
    the circuit with the given swapped_pairs produces z = x + y for all tests.
    
    :return: True if passes all tests, else False
    """
    import random
    
    for _ in range(test_count):
        x_val = random.randint(0, (1 << num_bits) - 1)
        y_val = random.randint(0, (1 << num_bits) - 1)
        
        # Build initial wire values for x?? and y??
        init_vals = {}
        # x?? bits
        for i in range(num_bits):
            bit = (x_val >> i) & 1
            wire_name = f"x{str(i).zfill(2)}"
            init_vals[wire_name] = bit
        # y?? bits
        for i in range(num_bits):
            bit = (y_val >> i) & 1
            wire_name = f"y{str(i).zfill(2)}"
            init_vals[wire_name] = bit
        
        # Run circuit
        final_values = run_circuit(gates, init_vals, swapped_pairs=swapped_pairs)
        z_val = get_binary_from_wires(final_values, prefix='z')
        
        if z_val != (x_val + y_val):
            return False
    return True

def main():
    """
    Example approach to searching for the correct 4 swapped pairs.
    This is a high-level brute-force sketch. For a large puzzle input,
    you would need to optimize or incorporate puzzle-specific logic.
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')
    
    # 1) Parse
    puzzle_input = read_input(file_path)
    initial_values, gates = parse_input(puzzle_input)

    # We *assume* we know how many bits might be involved. 
    # For demonstration, let's guess it might be around 8 or 10. 
    # (For the real puzzle, parse from the wire names or from known constraints.)
    num_bits = 10  # or detect from the highest x?? or y?? wire
    
    #
    # 2) Identify all output wires (the ones that appear as out_wire in the gate list).
    #
    out_wires = [gate[3] for gate in gates]
    out_wires = list(set(out_wires))  # unique
    
    #
    # 3) We need exactly four pairs to swap, so 8 wires total are involved in swaps.
    #    That means we choose 8 distinct wires out of out_wires, 
    #    then pair them up in all possible ways.
    # 
    # If there are many output wires, this is large.  In a real puzzle, 
    # you might use logic or partial checks to prune the search space.
    #
    possible_solutions = []
    
    # Choose 8 distinct wires among all out_wires
    # (Combinations of out_wires of size 8)
    for wires_8 in combinations(out_wires, 8):
        # wires_8 is a tuple of 8 wires
        # Now we want to form pairs.  The number of ways to partition 8 distinct items
        # into 4 disjoint pairs is (8!)/(2^4 * 4!) = 105. 
        # We can use a small helper or do a recursion approach, but let's use a known trick:
        
        def pair_partitions(eight_wires):
            """Return all ways to split 8 wires into 4 distinct pairs."""
            if not eight_wires:
                return [[]]  # one way (no pairs)
            res = []
            first = eight_wires[0]
            for i in range(1, len(eight_wires)):
                pair = (first, eight_wires[i])
                # Remainder
                rem = eight_wires[1:i] + eight_wires[i+1:]
                for sub in pair_partitions(rem):
                    res.append([pair] + sub)
            return res
        
        for pairing in pair_partitions(list(wires_8)):
            # pairing is a list of 4 pairs: [ (w1, w2), (w3, w4), (w5, w6), (w7, w8) ]
            swapped_pairs = pairing
            
            # 4) Test if this swap scheme works for the addition logic
            #    We'll do multiple random tests for x,y 
            #    (We could also do a thorough test of all possibilities up to num_bits, 
            #     but that might be large if num_bits is big.)
            if check_addition_correctness(gates, swapped_pairs, num_bits=num_bits, test_count=20):
                # If it passes, store it
                possible_solutions.append(swapped_pairs)
                # Often AoC puzzle has a unique solution, so we might break early.
                # But let's just collect all.
    
    if not possible_solutions:
        print("No solutions found with this brute-force approach.")
        return
    
    if len(possible_solutions) == 1:
        print("Found unique solution!")
        solution = possible_solutions[0]
    else:
        print(f"Found {len(possible_solutions)} solutions, picking the first.")
        solution = possible_solutions[0]
    
    # solution is a list of 4 pairs: [ (w1, w2), (w3, w4), (w5, w6), (w7, w8) ]
    # We need to produce the 8 wire names, sorted, joined by commas.
    swapped_wires = []
    for (a, b) in solution:
        swapped_wires.append(a)
        swapped_wires.append(b)
    swapped_wires.sort()
    answer = ",".join(swapped_wires)
    print("Swapped wires (sorted):", answer)

if __name__ == "__main__":
    main()
