import networkx as nx
from collections import defaultdict

def parse_input(input_text):
    """
    Parses the puzzle input into:
      - input_vals: dict of wire_name -> int (0 or 1) for wires that start with a known value
      - gates: list of (input1, gate_op, input2, output_wire)
    """
    parts = input_text.strip().split("\n\n")
    
    # First part: known wire values
    input_vals = {}
    for line in parts[0].splitlines():
        wire, val_str = line.split(": ")
        input_vals[wire] = int(val_str)
    
    # Second part: gate definitions
    gates = []
    for line in parts[1].splitlines():
        left_side, out_wire = line.split(" -> ")
        in1, op, in2 = left_side.split()
        gates.append((in1, op, in2, out_wire))
    
    return input_vals, gates

def build_circuit_graph(gates):
    """
    Build a DAG where:
      - Each gate is a node named gate_{i} with attributes:
          {
            "op": ...,        # "AND", "OR", "XOR", ...
            "input_wires": (in1, in2),
            "output_wire": out_wire
          }
      - Each wire is also a node named wire_{wire_name} with attribute:
          {
            "is_wire": True
          }
      - Directed edges:
          wire_{in1}  -> gate_{i}
          wire_{in2}  -> gate_{i}
          gate_{i}    -> wire_{out}
    """
    G = nx.DiGraph()
    
    for i, (in1, op, in2, out_wire) in enumerate(gates):
        gate_name = f"gate_{i}"
        
        # Add gate node
        G.add_node(gate_name, 
                   op=op, 
                   input_wires=(in1, in2), 
                   output_wire=out_wire, 
                   is_gate=True)
        
        # Ensure wire nodes exist
        wire_in1_node = f"wire_{in1}"
        wire_in2_node = f"wire_{in2}"
        wire_out_node = f"wire_{out_wire}"
        
        if not G.has_node(wire_in1_node):
            G.add_node(wire_in1_node, is_wire=True)
        if not G.has_node(wire_in2_node):
            G.add_node(wire_in2_node, is_wire=True)
        if not G.has_node(wire_out_node):
            G.add_node(wire_out_node, is_wire=True)
        
        # Add edges
        G.add_edge(wire_in1_node, gate_name)
        G.add_edge(wire_in2_node, gate_name)
        G.add_edge(gate_name, wire_out_node)
    
    return G

def attach_initial_wire_values(G, input_vals):
    """
    Attach an attribute "value" = 0/1 to the wire nodes 
    that appear in input_vals.
    """
    for wire_name, val in input_vals.items():
        wire_node = f"wire_{wire_name}"
        if wire_node in G.nodes:
            G.nodes[wire_node]["value"] = val
        else:
            # It's possible the puzzle input has a wire that's not used in gates,
            # or you might want to add that node to the graph if missing.
            G.add_node(wire_node, is_wire=True, value=val)

def topological_order(G):
    return list(nx.topological_sort(G))

def apply_gate_op(val1, gate_op, val2):
    if gate_op == "AND":
        return val1 & val2
    elif gate_op == "OR":
        return val1 | val2
    elif gate_op == "XOR":
        return val1 ^ val2
    else:
        raise ValueError(f"Unknown gate op: {gate_op}")

def propagate_values(G):
    """
    Perform a topological pass over G, and compute gate outputs 
    for nodes that have known inputs. Store results in wire nodes' "value".
    """
    topo_nodes = nx.topological_sort(G)  # generator
    
    for node in topo_nodes:
        # If it's a gate node, compute its output
        if G.nodes[node].get("is_gate"):
            op = G.nodes[node]["op"]
            in1, in2 = G.nodes[node]["input_wires"]
            # The input wire nodes are wire_in1_node = f"wire_{in1}", etc.
            in1_val = G.nodes[f"wire_{in1}"].get("value")
            in2_val = G.nodes[f"wire_{in2}"].get("value")
            
            # Only proceed if both inputs are known
            if in1_val is not None and in2_val is not None:
                out_val = apply_gate_op(in1_val, op, in2_val)
                out_wire_name = G.nodes[node]["output_wire"]
                G.nodes[f"wire_{out_wire_name}"]["value"] = out_val

        # If it's a wire node, there's nothing to do except read or store "value".
        # The value might be set in the step above, or from initial input values.

def apply_gate_expr(expr1, gate_op, expr2):
    if gate_op == "AND":
        return f"({expr1}) & ({expr2})"
    elif gate_op == "OR":
        return f"({expr1}) | ({expr2})"
    elif gate_op == "XOR":
        return f"({expr1}) ^ ({expr2})"
    else:
        raise ValueError(f"Unknown gate op: {gate_op}")

def propagate_expressions(G):
    """
    Similar to propagate_values, but store symbolic expressions 
    instead of actual bit values.
    """
    # Initialize wire nodes
    for node in G.nodes:
        if G.nodes[node].get("is_wire"):
            # If this wire had an initial int value, transform it into a literal string
            val = G.nodes[node].get("value")
            if val is not None:
                # "0" or "1" as a string
                G.nodes[node]["expr"] = str(val)
            else:
                # If we know it's an x?? or y?? wire but not set, store its name
                # e.g. wire_x00 -> "x00"
                wire_label = node.replace("wire_", "")
                # If you want to treat it symbolically: "x00"
                G.nodes[node]["expr"] = wire_label
    
    # Topological pass
    topo_nodes = list(nx.topological_sort(G))
    
    for node in topo_nodes:
        if G.nodes[node].get("is_gate"):
            op = G.nodes[node]["op"]
            in1, in2 = G.nodes[node]["input_wires"]
            expr1 = G.nodes[f"wire_{in1}"].get("expr")
            expr2 = G.nodes[f"wire_{in2}"].get("expr")
            
            if expr1 is not None and expr2 is not None:
                out_expr = apply_gate_expr(expr1, op, expr2)
                out_wire = G.nodes[node]["output_wire"]
                G.nodes[f"wire_{out_wire}"]["expr"] = out_expr

import networkx as nx

def solve_puzzle(input_text):
    # 1) Parse
    input_vals, gates = parse_input(input_text)
    
    # 2) Build DAG
    G = build_circuit_graph(gates)
    
    # 3) Attach known wire values
    attach_initial_wire_values(G, input_vals)
    
    # 4) Topological order (optional, we'll do that inside the propagate function too)
    # order = topological_order(G)
    
    # 5) Propagate symbolic expressions
    propagate_expressions(G)
    
    # 6) Now G.nodes["wire_XXX"]["expr"] has a symbolic expression for each wire
    #    Let's see what the final 'z??' wires have as expressions:
    z_wires = [n for n in G.nodes if n.startswith("wire_z")]
    # Sort them by numeric portion (z00, z01, z02, etc.)
    z_wires.sort(key=lambda w: int(w.split("_z")[1]))
    
    for w in z_wires:
        expr = G.nodes[w].get("expr", None)
        print(f"{w} => {expr}")
    
    # 7) We see the suspicious wires or notice mismatches: 
    #    in a correct adder, z00 might be something like "((x00) ^ (y00)) ^ (carry_in_0)"
    #    but if there's a swap, we might see "((x05) & (y05))" instead, etc.
    #
    #    Identify pairs of wires that are "crossed".
    #    This step is logic/pattern matching:
    #      - Possibly parse the expr and see if it matches known sub-expressions.
    #      - Keep track of which wire is actually providing which function.
    #      - If wire_z00's function is actually the expression for z05,
    #        and wire_z05's function is actually the expression for z00, 
    #        that's a prime candidate for a swapped pair.
    
    # 8) Once we identify 4 pairs, sort them and produce the final answer.

    # For the example puzzle, you'd do more thorough logic steps,
    # or partial truth table checks, to confirm which gates are swapped.

    # Return or print the final result
    return


def main():
    import os
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    #file_path = os.path.join(directory, 'input2.txt')
    #file_path = os.path.join(directory, 'input3.txt')

    with open(file_path, "r") as f:
        input_text = f.read()
    solve_puzzle(input_text)

if __name__ == "__main__":
    main()
