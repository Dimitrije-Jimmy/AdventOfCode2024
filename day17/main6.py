from z3 import BitVec, Solver, BitVecVal, URem, UDiv, LShR, sat

def solve_initial_A(outputs):
    """
    Given a list of outputs (each 0-7), find an initial A that produces this output sequence.
    """
    num_iterations = len(outputs)
    # We'll represent A as a 64-bit integer to be safe.
    # Adjust if needed.
    bitwidth = 64

    solver = Solver()

    # Create arrays for A, B, C variables at each iteration
    A_vars = [BitVec(f"A_{i}", bitwidth) for i in range(num_iterations+1)]
    B_vars = [BitVec(f"B_{i}", bitwidth) for i in range(num_iterations)]
    C_vars = [BitVec(f"C_{i}", bitwidth) for i in range(num_iterations)]

    # Initial A is what we're solving for: A_0 is unknown
    # We allow any non-negative integer. If we need non-negative:
    # Add constraint A_0 >= 0 (if needed).
    # If A can be large, we won't constrain its sign, but since it's a bit-vector,
    # treat all operations as unsigned.

    for i in range(num_iterations):
        # Forward logic for iteration i:
        # B_i = (A_i % 8)
        B_init = URem(A_vars[i], BitVecVal(8, bitwidth))

        # B_i = B_i ^ 1
        B_step1 = B_init ^ BitVecVal(1, bitwidth)

        # C_i = A_i >> B_i (logical shift right)
        # For shift, we must extract the amount from B_step1's lower bits.
        # B_step1 can be large, but we only care about low bits. Still, it works directly.
        C_val = LShR(A_vars[i], B_step1)

        # A_(i+1) = A_i // 8
        A_next = UDiv(A_vars[i], BitVecVal(8, bitwidth))

        # B_i = B_i ^ 4
        B_step2 = B_step1 ^ BitVecVal(4, bitwidth)

        # B_i = B_i ^ C_i
        B_final = B_step2 ^ C_val

        # out_i = B_final % 8
        out_val = URem(B_final, BitVecVal(8, bitwidth))

        # Add constraints:
        # out_val == outputs[i]
        solver.add(out_val == outputs[i])

        # Set the variables for next iteration:
        solver.add(A_vars[i+1] == A_next)
        solver.add(B_vars[i] == B_final)
        solver.add(C_vars[i] == C_val)

    # After all iterations, A_n = 0 (loop ends)
    solver.add(A_vars[num_iterations] == 0)

    # Solve
    if solver.check() == sat:
        model = solver.model()
        A_start_val = model[A_vars[0]].as_long()
        return A_start_val
    else:
        return None

def main():
    # Suppose we have a known output sequence and want to backsolve for A.
    # Let's pick a small example:
    # If we had a certain output sequence, say [3, 1, 7], 
    # we want to find A that produces these outputs.
    # In a real scenario, you'd have the actual outputs from a puzzle.

    example_outputs = [3, 1, 7]
    example_outputs = [0,3,5,4,3,0]
    #example_outputs = [0,1,5,4,3,0]
    #example_outputs = [2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0]
    A_start = solve_initial_A(example_outputs)

    if A_start is not None:
        print(f"Found A_start = {A_start}")
        # Verify by running forward:
        forward_out = execute_forward(A_start)
        print("Forward check:", forward_out)
    else:
        print("No solution found.")

def execute_forward(A_init):
    """ Just to verify the found A by running the logic forward in Python """
    A = A_init
    outputs = []
    while A != 0:
        B = A % 8
        B = B ^ 1
        C = A >> B
        A = A // 8
        B = B ^ 4
        B = B ^ C
        out_val = B % 8
        outputs.append(out_val)
    return outputs

if __name__ == "__main__":
    main()
