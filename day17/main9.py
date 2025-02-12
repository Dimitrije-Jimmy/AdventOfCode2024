def run_iteration_forward(A, B, C):
    """
    Run one iteration of the program:
    Program: 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0
    Instructions by step:

    1) bst 4: B = A % 8
    2) bxl 5 (literal 5): B = B XOR 5
    3) cdv 5 (combo 5=B): C = A // (2^(B))
    4) bxl 6 (literal 6): B = B XOR 6
    5) adv 3 (combo 3=3): A = A // 8
    6) bxc: B = B XOR C
    7) out 5 (combo 5=B): output = B % 8
    8) jnz 0: if A != 0 jump (handled outside this function)

    Returns: (A_next, B_next, C_next, output)
    """

    # Step 1: bst 4
    B = A % 8
    # Step 2: bxl 5
    B = B ^ 5
    # Step 3: cdv 5 -> C = A // (2^(B))
    C = A // (2 ** B)
    # Step 4: bxl 6
    B = B ^ 6
    # Step 5: adv 3 -> A = A // 8
    A = A // 8
    # Step 6: bxc -> B = B XOR C
    B = B ^ C
    # Step 7: out 5 -> output = B % 8
    out_val = B % 8
    return A, B, C, out_val

def run_full_forward(A_init, program_length):
    # Given a starting A (with B=0, C=0), run the loop until A=0, collecting outputs
    A = A_init
    B = 0
    C = 0
    outputs = []
    # This could potentially run indefinitely if A never becomes 0, but we rely on the logic that
    # to produce exactly 'program_length' outputs matching the program, it will eventually end.
    for _ in range(program_length):
        if A == 0:
            break
        A, B, C, o = run_iteration_forward(A, B, C)
        outputs.append(o)
    # If after producing the required outputs A is not 0, let's run one more iteration to confirm it halts:
    # Actually, we know from the puzzle that halting occurs when we pass end of program or A=0 stops jnz from looping.
    return outputs

def invert_iteration(A_next, output):
    """
    Given A_next (the value of A after the iteration) and the output produced during that iteration,
    find all possible A values at the start of the iteration that yield that output and end with A_next.

    From the forward steps:
    Let A_i = initial A, B_i=0, C_i=0 at start of iteration (since we always restore B,C from final step? Actually no, B and C carry over)
    Actually B and C do carry over between iterations. We must track them backward as well.

    This complicates the problem because B and C from one iteration affect the next. 
    But from the code, we see that each iteration redefines B and C from scratch based on A:
    Wait, it does not. We must confirm how B and C get updated between iterations.

    Let's reconsider carefully:
    The instructions each iteration do not reset B and C. B and C carry over from previous iteration's end.

    That means we must also track possible B,C states going backward. 
    This greatly increases complexity.

    To handle this complexity, we must store states as (iteration_index, A_next, B_next, C_next) and find (A,B,C) that lead to it.

    Let's define a backward step function that tries all A_i in range 8*A_next to 8*A_next+7:
    For each candidate A_i, we run the forward iteration and see if it matches output and results in A_next from A_i.
    We must also guess previous B, C. That's unknown at the first backward step.

    Wait, we do know final conditions: after final iteration A=0. But B and C can be anything. 
    We must consider that after last iteration we only need correctness of output. B and C do not matter after the program halts.

    But the program halts after reading past end. Actually, from the puzzle: "If tries to read an opcode past the end, halts."
    In our code, we run a loop checking for A. The jnz 0 loops until A=0. When A=0, it does not jump, execution continues to next instruction pair. 
    But next instruction would be past end of program -> halt. 
    So after final iteration A=0, the next step halts. B and C final values are irrelevant at the end. We can just not constrain them at the last step.

    This is still tricky because we must guess B and C from scratch going backward. 
    But notice from forward iteration: B and C after iteration depends only on A at the start of that iteration. 
    If we know A_i and we know the output_i, we can compute what B and C must have been forward and check consistency.

    So backward step:
    - We know at iteration i: final A = A_(i+1)
    - We know output_i
    - We want to find A_i, B_i_start, C_i_start that leads forward to the given output_i and A_(i+1).

    But we do not know B_i_start or C_i_start. They are from previous iteration end. 
    However, each iteration's code fully determines B and C at the end from A_i, starting from known B_i_start, C_i_start.

    Wait, we have a circular problem. 
    Actually, B and C carry over. We must track them in the state as we do backward.

    Approach:
    - When going backward, at iteration i we know the final (A_(i+1), B_(i+1), C_(i+1)) that must result from the iteration i. 
      Actually, at the final iteration, we know A_(final+1)=0, but not B_(final+1), C_(final+1).

    Let's store partial states and do a backward search with memoization on (i, A_next, B_next, C_next).

    For i-th iteration from the end:
    We know output_i and want to find all (A_i, B_i, C_i) that after one forward iteration give (A_next, B_next, C_next) and output_i.

    But at the final iteration, we don't have B_next, C_next constraints. After final iteration, program halts immediately. 
    Actually, after final iteration A=0. The next step tries to read opcode beyond end and halts. B and C next are irrelevant. 
    So for the last iteration, let's just say we only know A_next=0 (and we don't care about B_next and C_next). 
    We'll try all B,C possibilities backward?
    That's infinite. We must rely on the derived formula we have.

    Let's simplify the problem by noticing from the forward code:
    B and C at the start of iteration are whatever they ended with last iteration. Initially, B=0, C=0 at iteration 1 start.

    Let's define the sequence of outputs and the number of iterations equals program length = 16.

    We know:
    - Initially: A = unknown, B=0, C=0
    - After 16 iterations: A=0. The final output is known.

    If we attempt a full backward search with B and C as well, complexity skyrockets.

    Another approach: Because every iteration sets B early from A (bst sets B to A%8), B and C at start influence final B differently. 
    Let's carefully re-check if B,C are indeed influenced by previous iteration. Actually, they are:
      On the first iteration, B=0, C=0 initially given.
      On the second iteration, B and C are what remained after first iteration.

    We must track them. Without that, we can't solve backward easily.

    But notice a pattern: 
    The instructions:
      - B is overwritten at step1: B = A%8
        This means the previous value of B is discarded each iteration at the very beginning (bst sets B from A%8).
      So B at the start of iteration doesn't matter! It's overwritten immediately.

    What about C at the start of iteration?
    On step3: C = A // (2^(B after step2)). B after step2 is computed from B after step1 (which depends only on A).
    C at start of iteration is never used before being overwritten. So C at iteration start also doesn't matter.

    Conclusion:
    The final output depends only on A_i. B and C from previous iteration are irrelevant because they are overwritten unconditionally.

    This is a crucial simplification!
    So at each iteration forward, the result (A_next, B_final, C_final, output) depends only on A_i. B_i_start, C_i_start are irrelevant since B and C get fully redefined.

    Perfect! Now backward is simpler:
    From the equations:
    Forward:
      Given A_i:
        B_1 = (A_i % 8)
        B_2 = B_1 XOR 5 = (A_i % 8) XOR 5
        C = A_i // (2^(B_2))
        B_3 = B_2 XOR 6 = ((A_i % 8) XOR 5) XOR 6 = (A_i % 8) XOR 3
        A_next = A_i // 8
        B_final = B_3 XOR C = ((A_i % 8) XOR 3) XOR C
        output = B_final % 8

    We want:
    output_i = (( (A_i % 8) XOR 3 ) XOR (A_i // (2^( ((A_i % 8) XOR 5) )) )) % 8
    and A_next = A_i // 8

    Given A_next and output_i, find A_i:
    A_i = 8*A_next + x, where x in [0..7].

    For each x:
      C = (8*A_next + x) // (2^(x XOR 5))
      B_final = (x XOR 3) XOR C
      Check if B_final % 8 == output_i
      If yes, (A_i) is a candidate.

    This gives up to 8 candidates per iteration. We choose the minimal positive A after processing all iterations backward.

    We'll start from the last iteration (i=16) where A_next=0 and output_16=0.
    For iteration i from 16 down to 1:
      We'll have a set of possible A_next values from the "future".
      For each A_next and the known output_i,
      find all A_i that lead to that output_i and A_next.
      Keep track of minimal A_i encountered as we go backward.

    At the end (i=1), we get all possible initial A that produce the full sequence. We return the smallest positive one.

    Let's implement this now.
    """

def find_initial_A(program):
    # program is the output sequence we want
    # number of iterations = length of the program
    n = len(program)

    # We'll go backward. After the last iteration:
    # A_next = 0 (so that the program halts)
    possible_As = {0}  # at iteration n+1, A=0

    # Go backwards from iteration n down to 1
    for i in range(n-1, -1, -1):
        output_i = program[i]
        new_possible_As = set()
        for A_next in possible_As:
            # Try all x in 0..7
            for x in range(8):
                A_i = 8*A_next + x
                B2 = x ^ 5
                if B2 > 50: 
                    # no need, but just a sanity check: no
                    pass
                # Compute C
                denom = 2**B2
                if denom == 0:
                    continue
                C = A_i // denom
                B_final = ( (x ^ 3) ^ C )
                if (B_final % 8) == output_i:
                    # This A_i leads to the correct output and A_next
                    new_possible_As.add(A_i)
        # Prune: we only need small As to keep memory manageable,
        # since we want the minimal A at the end.
        # Keep only, say, the smallest 1000 candidates to limit memory (heuristic).
        # Or just keep them all, hoping not too large.
        # The user said about 15 digits, let's prune aggressively:
        if len(new_possible_As) > 20000:
            new_possible_As = set(sorted(new_possible_As)[:20000])

        possible_As = new_possible_As

        if not possible_As:
            # No solution
            return None

    # After finishing, possible_As contains all initial A that can produce the sequence.
    # We want the smallest positive one.
    res = min(a for a in possible_As if a > 0) if any(a > 0 for a in possible_As) else None
    return res


if __name__ == "__main__":
    # Given:
    # Register A: unknown, must find
    # Register B: 0
    # Register C: 0
    # Program: 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0
    # The output must equal the program itself.

    program = [2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0]
    #program = [0, 3, 5, 4, 3, 0]
    #program = [0,3,5,4,3,0]
    result = find_initial_A(program)
    if result is not None:
        print("Found A:", result)
        # Verify by running forward:
        outputs = run_full_forward(result, len(program))
        if outputs == program:
            print("Verification passed. Program outputs itself.")
        else:
            print("Verification failed. Got:", outputs)
    else:
        print("No solution found.")
