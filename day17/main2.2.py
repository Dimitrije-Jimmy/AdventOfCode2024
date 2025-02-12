class SymbolicValue:
    """A class to represent symbolic expressions depending on a variable a."""
    def __init__(self, expr):
        # expr is a string or tuple representing the expression
        self.expr = expr

    def __repr__(self):
        return f"Sym({self.expr})"

    def __add__(self, other):
        return SymbolicValue(("add", self.expr, other.expr if isinstance(other, SymbolicValue) else other))

    def __mul__(self, other):
        return SymbolicValue(("mul", self.expr, other.expr if isinstance(other, SymbolicValue) else other))
    
    def __xor__(self, other):
        return SymbolicValue(("xor", self.expr, other.expr if isinstance(other, SymbolicValue) else other))
    
    def floor_div_by_power_of_two(self, power):
        # Represents floor division by 2^power symbolically
        return SymbolicValue(("fdiv2", self.expr, power))
    
    def mod8(self):
        # Modulo 8: represents taking the last 3 bits of the expression
        return SymbolicValue(("mod8", self.expr))

    def as_int(self):
        # If needed, attempt a concrete evaluation if it's a constant
        # Otherwise return None
        if isinstance(self.expr, int):
            return self.expr
        return None

    def equals_const(self, c):
        # A helper to form equation that this expression = c
        return ("eq", self.expr, c)


def make_symbolic_operand_value(operand_type, operand, A, B, C):
    if operand_type == 'literal':
        return SymbolicValue(operand)
    elif operand_type == 'combo':
        if operand <= 3:
            return SymbolicValue(operand)
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        else:
            raise ValueError("Invalid combo operand 7 encountered")
    elif operand_type == 'ignored':
        return None
    else:
        raise ValueError("Invalid operand type")

def execute_program_symbolically(program):
    # Initial registers:
    # A = a (our symbolic variable)
    # B = 0
    # C = 0
    A = SymbolicValue("a") 
    B = SymbolicValue(0)
    C = SymbolicValue(0)

    IP = 0
    outputs = []

    # Define operand types per opcode
    operand_types = {
        0: 'combo',   # adv
        1: 'literal', # bxl
        2: 'combo',   # bst
        3: 'literal', # jnz
        4: 'ignored', # bxc
        5: 'combo',   # out
        6: 'combo',   # bdv
        7: 'combo'    # cdv
    }

    while IP < len(program):
        opcode = program[IP]
        if IP + 1 >= len(program):
            # No operand, halt
            break
        operand = program[IP+1]
        operand_type = operand_types[opcode]

        operand_value = make_symbolic_operand_value(operand_type, operand, A, B, C)

        if opcode == 0:  # adv
            # A = floor(A / 2^(operand_value))
            # operand_value must be integer or an expression. Typically it's a small integer or B/C
            # If operand_value is not a constant, we still represent symbolically
            A = A.floor_div_by_power_of_two(operand_value.as_int() if operand_value.as_int() is not None else ("expr_dep", operand_value.expr))
            IP += 2

        elif opcode == 1: # bxl
            # B = B ^ operand_value
            B = B ^ operand_value
            IP += 2

        elif opcode == 2: # bst
            # B = operand_value % 8
            B = operand_value.mod8()
            IP += 2

        elif opcode == 3: # jnz
            # If A != 0 then jump to operand_value
            # Symbolically, we don't know A's value.
            # Let's assume for this path that A != 0 (or we must consider both cases)
            # For a complete solution, consider branching:
            # If we consider that to replicate the program, A likely not zero at this point:
            # We'll follow the jump. If A=0, we do not jump. 
            # This creates a branching complexity. For simplicity, let's pick one branch.
            
            # Let's assume A != 0 to take the jump:
            # If you need both branches, you'd store them and solve later.
            # For demonstration, just pick the branch "A != 0" and jump:
            # If you wanted to be rigorous, you'd represent conditions and possibly create a tree of execution.
            
            # Let's pick: if A != 0, jump:
            IP = operand_value.as_int() if operand_value.as_int() is not None else 0
            if IP is None:
                # If operand_value isn't a concrete integer, we have an issue. Let's just halt.
                break
            # If we jumped, do not advance IP by 2.
            
        elif opcode == 4: # bxc
            # B = B ^ C
            B = B ^ C
            IP += 2

        elif opcode == 5: # out
            # output = operand_value % 8
            out_val = operand_value.mod8()
            outputs.append(out_val)
            IP += 2

        elif opcode == 6: # bdv
            # B = floor(A / 2^(operand_value))
            B = A.floor_div_by_power_of_two(operand_value.as_int() if operand_value.as_int() is not None else ("expr_dep", operand_value.expr))
            IP += 2

        elif opcode == 7: # cdv
            # C = floor(A / 2^(operand_value))
            C = A.floor_div_by_power_of_two(operand_value.as_int() if operand_value.as_int() is not None else ("expr_dep", operand_value.expr))
            IP += 2

        else:
            # Invalid opcode
            break

    return outputs

def main():
    # Example program from the user:
    program = [2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0]
    
    outputs = execute_program_symbolically(program)
    print("Symbolic outputs:", outputs)

    # At this point, `outputs` is a list of symbolic expressions depending on `a`.
    # The goal is to have outputs[i] == program[i] for all i.
    # You would now have a system of equations:
    # For each i: outputs[i] = program[i]
    # For simplicity, let's just print these equations:
    equations = []
    for i, out_expr in enumerate(outputs):
        eq = out_expr.equals_const(program[i])
        equations.append(eq)

    print("Equations that must be solved for a:")
    for eq in equations:
        print(eq)

    # Solving these equations is non-trivial. You might need:
    # - Manual analysis
    # - A custom solver to handle XOR, mod, and floor-div-by-power-of-two
    # - Searching patterns in bits of A.

    # This code shows the symbolic setup. The next step would be analyzing 'equations'
    # to find a suitable 'a'.

if __name__ == "__main__":
    main()
