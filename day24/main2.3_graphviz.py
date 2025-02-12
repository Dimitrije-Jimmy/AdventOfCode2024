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
def main():
    import os
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')

    with open(file_path, "r") as f:
        input_text = f.read()
    input_vals, gates = parse_input(input_text)
    generate_dot(gates, "mycircuit.dot")

if __name__ == "__main__":
    main()

# run command to generate png:
# dot -Tpng mycircuit.dot -o mycircuit.png 

"""
Implement the “sanity checks” you described for a (ripple-carry) adder, specifically checking constraints like:
Certain XOR gates must (or must not) output to z__.
Gates that produce z__ bits must be XOR (except final carry).
Etc.

For part 2, I basically used python to process the wiring data and output graphviz dot code so I could generate a png 
file of the wiring and manually inspect it. I created nodes for the wires and also nodes for the "AND/OR/XOR" gates. 
I added color coding for the gates (red, green, or blue depending on the gate type) to make them easier to distinguish. 
I ended up focusing only on how there should always be two ANDs going into an OR (which corresponds to the full adder schematic 
I wrote down from the web), so usually there was a problem there, although I think 1 of the 4 problems was somewhere else, 
like in the XOR and AND from 2 of the inputs. (The gates were named like func0, func1, etc, but they were labeled with their function.)

So my output started like

digraph "G" {
func0 [label="OR",color=green]
svv -> func0
bcd -> func0
func0 -> bbk
func1 [label="OR",color=green] 
hsw -> func1
qfg -> func1
func1 -> bbt
func2 [label="AND",color=red]

art 2 (initial attempt): Since we're only using OR XOR AND gates, the referenced circuit was no doubt a ripple carry adder
. Thus it was relatively straightforwards to solve this by running a series of sanity checks to make sure all the wires were done correctly.

All XOR gates that input x__ and y__ cannot every output z__ (unless x00,y00 because the first one is a half adder)

All other XOR gates must output z__

All gates that output z__ must be XOR (except for z45, which is the final carry)

All gates checked in (1) must output to gate checked in (2)

If there are any swaps unaccounted for, manually review




Sanity Checks (Ripple-Carry Adder Constraints)
You outlined checks like:

All XOR gates that input only x__ and y__ cannot output z__ (except if they’re the half-adder for bit 0).
In other words, if a gate is XOR and its inputs are named x?? and y??, it must not produce a z__ wire output (except for x00,y00). 
Because the typical half-adder for the LSB might directly produce z00 (the sum bit for the 0th position).
All other XOR gates must output z__.
This reflects that in a full-adder chain, sum bits come from XOR gates that combine carry_in with partial sums, etc.
All gates that output z__ must be XOR (except the final carry wire, e.g. z45 or whatever label your puzzle uses for the top bit).
So if you see an AND or OR producing a wire named z22, that’s suspicious.
(From your message) “All gates checked in (1) must output to gate checked in (2)” - i.e., partial XOR outputs feed a subsequent stage, not directly to a final z??, in normal ripple design.
"""