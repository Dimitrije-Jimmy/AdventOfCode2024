import os

def parse_input(input_text):
    """
    Splits the input into two sections:
    1) initial wire values
    2) gates definitions
    
    Returns:
      input_vals: dict { wire_name: 0/1 }
      gates: list of tuples (in1, op, in2, out_wire)
    """
    parts = input_text.strip().split("\n\n")
    
    # 1) Known wire values
    input_vals = {}
    for line in parts[0].splitlines():
        wire_str, val_str = line.split(": ")
        input_vals[wire_str] = int(val_str)
    
    # 2) Gate definitions
    gates = []
    for line in parts[1].splitlines():
        lhs, out_wire = line.split(" -> ")
        in1, op, in2 = lhs.split()
        gates.append((in1, op, in2, out_wire))
    
    return input_vals, gates

def gate_color(op):
    if op == "AND":
        return "red"
    elif op == "OR":
        return "green"
    elif op == "XOR":
        return "blue"
    else:
        return "black"  # default if unknown

def generate_dot(gates, filename="mycircuit.dot"):
    """
    Writes a .dot file that describes the circuit.
    Each gate is a node. We also create wire nodes for clarity.
    """
    with open(filename, "w") as f:
        f.write('digraph "G" {\n')
        
        # Create gate nodes
        for i, (in1, op, in2, out_wire) in enumerate(gates):
            gate_name = f"func{i}"
            color = gate_color(op)
            f.write(f'{gate_name} [label="{op}",color={color},style=filled];\n')
        
        # Create edges
        for i, (in1, op, in2, out_wire) in enumerate(gates):
            gate_name = f"func{i}"
            # We can represent wires as separate nodes if desired:
            # but let's just do them as invisible or minimal-labeled nodes
            # Or skip them if you like. We'll do them for clarity:
            wire_in1_node = f"wire_{in1}"
            wire_in2_node = f"wire_{in2}"
            wire_out_node = f"wire_{out_wire}"
            
            # Make sure we define those wire nodes
            # (We won't style them, just label with their wire name)
            f.write(f'{wire_in1_node} [label="{in1}",shape=box];\n')
            f.write(f'{wire_in2_node} [label="{in2}",shape=box];\n')
            f.write(f'{wire_out_node} [label="{out_wire}",shape=box];\n')
            
            # in1 -> gate
            f.write(f'{wire_in1_node} -> {gate_name};\n')
            # in2 -> gate
            f.write(f'{wire_in2_node} -> {gate_name};\n')
            # gate -> out_wire
            f.write(f'{gate_name} -> {wire_out_node};\n')
        
        f.write('}\n')

def is_x_wire(w):
    return w.startswith("x")

def is_y_wire(w):
    return w.startswith("y")

def is_z_wire(w):
    return w.startswith("z")

def sanity_checks_ripple_adder(gates):
    """
    Implement the logic constraints you mentioned.
    Print warnings for any gate that violates them.
    
    gates = [(in1, op, in2, out_wire), ...]
    """
    # We might also keep track of the "lowest bit" e.g. x00,y00 => half adder
    # but let's just check if we see "x00" and "y00" specifically.
    
    for i, (in1, op, in2, out_wire) in enumerate(gates):
        gate_label = f"gate{i} ({op} {in1} {in2} -> {out_wire})"
        
        # 1) "All XOR gates that input only x__ and y__ cannot output z__ 
        #    unless it's specifically x00,y00 => z00 (the half-adder)."
        if op == "XOR" and is_x_wire(in1) and is_y_wire(in2):
            # If both inputs are x?? and y??, check if it outputs z??
            if is_z_wire(out_wire):
                # Check if it's the special half-adder case:
                if not (in1 == "x00" and in2 == "y00" and out_wire == "z00"):
                    print(f"[WARNING] {gate_label} violates the 'no direct z__ output' for XOR x__,y__ (except half-adder).")
        
        # 2) "All *other* XOR gates must output z__"
        #    i.e. if it's XOR but not purely (x??, y??) as inputs, it presumably
        #    is generating a sum bit => must go to z?? (or final carry).
        #if op == "XOR" and (not (is_x_wire(in1) and is_y_wire(in2))):
        #    # This XOR is presumably an internal sum (carry_in XOR partial sum, etc.)
        #    # We want it to produce z??, or maybe the final carry wire if puzzle does that?
        #    # Let's assume it must produce z__ except for a final carry named zN+1 or something.
        #    if not is_z_wire(out_wire):
        #        print(f"[WARNING] {gate_label} expected to produce z__ but outputs {out_wire}.")
        
        # 3) "All gates that output z__ must be XOR (except e.g. z45 for final carry)."
        #    If we have a 46-bit adder, maybe z45 is the top carry. 
        #    For demonstration, let's say if out_wire == "z45" we skip the check.
        if is_z_wire(out_wire):
            # Suppose final carry is z45
            final_carry_wire = "z45"  
            if out_wire != final_carry_wire:  # skip the final carry
                if op != "XOR":
                    print(f"[WARNING] {gate_label} outputs to z__ but is not XOR. Possible swap or error.")
        
        

        # 4) "All gates checked in (1) must output to gate checked in (2)."
        #    This is a bit more ambiguous from your description, but let's interpret:
        #    the XOR that handles (x_i, y_i) for partial sum shouldn't feed directly to z?? 
        #    (unless half-adder for bit0), but should feed a gate that is also XOR that eventually leads to z??
        #    We can’t fully check that unless we trace the DAG. For now, we might just check:
        #    if it’s an XOR with x__,y__, does it feed another XOR or an AND/OR for the carry logic?
        #    We'll keep it simple and just do a minimal check:
        
        # We'll do a partial check by scanning the gates again to see who consumes out_wire:
        # (Better is to build a graph and see the next gate, but let's do a quick nested loop)
        if op == "XOR" and is_x_wire(in1) and is_y_wire(in2):
            if not (in1 == "x00" and in2 == "y00" and out_wire == "z00"):  # skip the half-adder
                # We expect the out_wire to be used as input to an XOR gate or an AND gate 
                # in typical full-adder architecture. We'll do a quick check:
                consumer_gates = []
                for j, (iin1, iop, iin2, iout) in enumerate(gates):
                    if iin1 == out_wire or iin2 == out_wire:
                        consumer_gates.append((j, iop, iin1, iin2, iout))
                
                # If we found no consumer gates, suspicious
                if not consumer_gates:
                    print(f"[WARNING] {gate_label} XOR x__,y__ => {out_wire} but no gate consumes {out_wire}. Suspicious for a ripple adder.")
                else:
                    # If they exist, check if they are "XOR" or "AND" or "OR" for carry path
                    # This is approximate; real logic might have more gates. We'll just do a minimal check:
                    valid_ops = {"XOR", "AND", "OR"}
                    for (cid, cop, ci1, ci2, cout) in consumer_gates:
                        if cop not in valid_ops:
                            print(f"[WARNING] {gate_label} => used by gate{cid} with op={cop}, not typical for full adder.")

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input4.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')

    # Suppose we read puzzle input from a file
    with open(file_path, "r") as f:
        input_text = f.read()
    
    input_vals, gates = parse_input(input_text)
    
    # Generate the graphviz DOT for visual debugging:
    generate_dot(gates, filename="mycircuit.dot")
    
    # Now do the sanity checks:
    print("Running sanity checks for ripple adder logic...\n")
    sanity_checks_ripple_adder(gates)


if __name__ == "__main__":
    main()