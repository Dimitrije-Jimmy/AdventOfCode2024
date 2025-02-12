def f(A):
    # Given function:
    # B = (A mod 8) xor 2
    # C = A >> B
    # return (B xor C xor 3) mod 8
    B = (A % 8) ^ 2
    C = A >> B
    return (B ^ C ^ 3) % 8

def backward_solve_from_end(outputs):
    """
    Given the full output sequence (from first to last),
    we will start from the LAST output and go backward.
    
    Steps:
    - At the end of the program, A=0.
    - For the last output out_last, find all 10-bit A's that produce out_last.
    - Those represent A before the last iteration ran. But we must now 'reverse' the shift:
      forward: A_next = A_prev >> 3
      backward: A_prev = (A_next << 3) + x, for x in [0..7]
    - Repeat this for each previous output.
    
    After processing all outputs backward, we get a set of possible initial A values.
    One of them should match the known solution if it exists.
    """

    # We'll proceed backward in outputs:
    # Start from A=0 at the end: This doesn't directly tell us A before last iteration.
    # Instead, we know that for the last output out_n: f(A_before_last) = out_n.
    # A_before_last must be a 10-bit number that gives out_n when f(A_before_last) is called.

    reversed_outputs = outputs[::-1]

    # Start with a single candidate set: after no iterations backward, we know A_final = 0.
    # But we actually need to find A_before_last iteration.
    # Let's call current_set the set of A candidates at the current stage of backward reasoning.

    # For the last output (reversed_outputs[0]), we must find 10-bit numbers that produce it.
    last_out = reversed_outputs[0]
    current_set = []
    for a_candidate in range(1024): # 10-bit search
        if f(a_candidate) == last_out:
            current_set.append(a_candidate)

    bit_length = 10

    # Now go through each preceding output:
    # Each step:
    # current_set represents A BEFORE the current iteration we are processing backward.
    # We need to incorporate 3 more bits to undo the right shift by 3.
    # For each candidate in current_set:
    #   previous_A_candidates = []
    #   for each candidate c:
    #       for x in [0..7]:
    #           prev_A = (c << 3) + x
    #           if f(prev_A) == next_out:
    #               keep prev_A
    #   current_set = new filtered set
    for i in range(1, len(reversed_outputs)):
        next_out = reversed_outputs[i]
        new_set = []
        bit_length += 3

        base_candidates = current_set
        current_set = []  # we'll rebuild it
        for c in base_candidates:
            # Undo the shift: prev_A = (c << 3) + x
            base = c << 3
            for x in range(8):
                candidate = base + x
                if f(candidate) == next_out:
                    new_set.append(candidate)

        current_set = new_set
        if not current_set:
            # No candidates match at this stage, no solution
            return []

    # After finishing all outputs, current_set contains possible initial A values.
    return current_set

def main():
    # Known example from the puzzle: output sequence = [0,3,5,4,3,0]
    # The known solution is A=117440
    outputs = [0,3,5,4,3,0]

    solutions = backward_solve_from_end(outputs)
    if solutions:
        print("Possible initial A values that produce the given outputs (going backward):")
        for s in solutions[:]:
            print(s)
        # Check if 117440 is among them:
        if 117440 in solutions:
            print("117440 found!")
        else:
            print("117440 not found in the first 20 listed, but might be further in the set." 
                  "Check full set or optimize search.")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
