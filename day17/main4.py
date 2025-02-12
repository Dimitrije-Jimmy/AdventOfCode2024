class SymbolicVar:
    # A class to represent a symbolic variable or expression.
    # For simplicity, just store a representation (like a tuple).
    def __init__(self, name):
        # name could be 'A', 'B', 'C', or something else
        self.name = name
    
    def __repr__(self):
        return self.name

class SymbolicExpr:
    # Represent expressions like ("xor", expr1, expr2), ("fdiv2", expr, power), etc.
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def __repr__(self):
        return f"({self.op} {' '.join(map(str,self.args))})"

# We'll keep track of the state of A,B,C as symbolic expressions.
# Initially, at the end of the program, we have:
# A = A_final (an unknown variable representing initial A after all transformations)
# Similarly for B, C. Actually, at the end of the program, we might just say:
# A, B, C = SymVar('A_final'), SymVar('B_final'), SymVar('C_final')
# and we move backward, rewriting them in terms of A_initial.

def backward_execute(program):
    # We'll store states as tuples (A_expr, B_expr, C_expr)
    # Start from the end state: these represent the final known state
    # Actually, at the end of the program, we don't know A,B,C. Let's name them:
    A = SymbolicVar("A_end")
    B = SymbolicVar("B_end")
    C = SymbolicVar("C_end")

    # We also need to record output constraints:
    # We'll keep a list of constraints of the form (expr % 8 = value)
    constraints = []

    # Operand types
    operand_types = {
        0: 'combo',
        1: 'literal',
        2: 'combo',
        3: 'literal',
        4: 'ignored',
        5: 'combo',
        6: 'combo',
        7: 'combo'
    }

    # Function to get symbolic operand
    def get_operand_expr(otype, operand, A, B, C):
        if otype == 'literal':
            return operand
        elif otype == 'combo':
            if 0 <= operand <= 3:
                return operand
            elif operand == 4:
                return A
            elif operand == 5:
                return B
            elif operand == 6:
                return C
            else:
                raise ValueError("Invalid combo operand 7")
        elif otype == 'ignored':
            return None
        else:
            raise ValueError("Invalid operand type")

    # We'll process the program backwards:
    # This is complex due to jumps (jnz). For simplicity, assume we know the execution path.

    IP = 0
    # First, we must know the order instructions executed in the forward direction.
    # For now, let's assume no complicated jumps or that we recorded the execution path already.
    # A real solution would run forward once with a symbolic condition (A != 0) and handle branches.

    # Let's say we know the linear sequence of instructions executed:
    # For a real solution, you'd first run forward with a symbolic A and track the path chosen by jnz.
    # Here we assume linear execution for demonstration.

    executed_instructions = []
    pos = 0
    while pos < len(program):
        opcode = program[pos]
        if pos+1 >= len(program): break
        operand = program[pos+1]
        executed_instructions.append((pos, opcode, operand))
        if opcode == 3: # jnz
            # If we knew A != 0 at runtime, jump:
            # For a real solver, you'd store conditions.
            pass
        # Move forward by 2 unless jumped (we ignore complexity here)
        pos += 2

    # Now go backwards:
    for ip, opcode, operand in reversed(executed_instructions):
        otype = operand_types[opcode]
        # Get operand in terms of the current (backward) state A,B,C:
        # Actually we need the forward meaning: we know how A,B,C after changed from before.
        # We'll invert the operation:
        if opcode == 5: # out
            # out: output_val = operand_expr % 8 must equal program[ip] (the instruction's code)
            # operand_expr = get_operand_expr(otype, operand, A, B, C)
            # But we are going backward: at the time of 'out', A,B,C represent post state.
            # Actually, after 'out', registers do not change. So before 'out', A,B,C = after 'out'.
            # Constraint: (operand_expr % 8) = program[ip] (the instruction to replicate)
            val = get_operand_expr(otype, operand, A, B, C)
            constraints.append(("mod8_eq", val, program[ip+1])) # Actually the out matches program[<some index>]

            # No register changed by out, so A,B,C remain the same going backward.
            # Just record constraint.

        elif opcode == 0: # adv: A = floor(A_before / 2^(operand_expr))
            # Forward: A_after = A_before // (2^operand_expr)
            # Backward: A_before = A_after * (2^operand_expr)
            val = get_operand_expr(otype, operand, A, B, C)
            A = SymbolicExpr("mul2pow", A, val) # represent A_before as (A_after * 2^val)
            # A_after was what we called A now, so redefine A as A_before:
            # Actually, we need a temporary. Let's say:
            # After ADV: A_after known as old A,
            # Before ADV: new A = (old A * 2^val)
            # But we must handle the old A. Let's say we have a stack of states.

        # Similarly handle other instructions...
        # Due to complexity, we won't fully implement this now.

    # At the end, constraints should relate A_end, B_end, C_end to A_start.
    # Replace A_end, B_end, C_end with A_start, B_start, C_start eventually, after processing all instructions.
    # Solve constraints.

    return constraints

def solve_constraints(constraints):
    # This function would take the constraints and try to solve them.
    # This might involve:
    # - Converting them into a bit-level SAT problem.
    # - Trying a small search only on constrained bits of A.
    # Since this is problem-dependent, we only outline it here.

    # For demonstration:
    # If constraints look like (mod8_eq, A, 2), it means A % 8 = 2.
    # This gives A = 8k+2 for some k.
    # Combine such constraints from all instructions to narrow down A.

    # Without a real set of constraints to solve, we can't implement a solver here.
    # But you would:
    # 1. Collect all mod8 and XOR conditions.
    # 2. Reduce them to equations on bits.
    # 3. Try a small search on those bits or use a solver.

    pass

def main():
    # Example usage:
    program = [0,3,5,4,3,0] # a small example
    constraints = backward_execute(program)
    print("Collected constraints:", constraints)
    # Then solve them:
    solve_constraints(constraints)

if __name__ == "__main__":
    main()
