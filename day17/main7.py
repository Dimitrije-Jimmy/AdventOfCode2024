def f(A):
    B = (A % 8) ^ 2
    C = A >> B
    return (B ^ C ^ 3) % 8

def solve_outputs(outputs):
    """
    Given a sequence of outputs, find all possible initial A values that produce them.
    We'll implement the backward logic described.
    """

    # Start with the first output:
    # We know f(A) only depends on A mod 2^10 = A & 1023.
    # For the first output, find all A in [0..1023] that produce outputs[0].
    desired_out = outputs[0]
    current_set = []
    #for a_candidate in range(1024):  # 2^10 = 1024
    for a_candidate in range(1048576):  # 2^10 = 1024
        if f(a_candidate) == desired_out:
            current_set.append(a_candidate)

    # current_set now holds all 10-bit numbers that produce the first output.

    # For subsequent outputs:
    # After each iteration, A was shifted by 3 bits forward, so backward we must:
    # - For each candidate in current_set (which is (10 + 3*i)-bit number),
    #   we "add" 3 bits in front by testing all 8 possibilities.
    # - Check if they produce the next output.
    # - Keep only those that match.

    # We'll track how many bits we currently consider. Initially 10 bits after first output.
    bit_length = 10

    # For each subsequent output:
    for i in range(1, len(outputs)):
        next_out = outputs[i]
        new_set = []
        bit_length += 3  # each iteration adds 3 more bits from going backward.

        # To go backward:
        # current candidates represent A values AFTER i-th iteration (so they produce out[i]).
        # Before shifting by 3 bits (forward direction), the original A had 3 extra bits.
        # So we take each current candidate and generate all 8 expansions:
        # newA = (candidate << 3) + x, for x in [0..7].
        # Check if f(newA) == next_out.

        # Note: We must still consider f(newA) mod 2^10 only depends on lower 10 bits of newA.
        # But because we are building sets step-by-step, we keep the full integer.
        # If performance is an issue, we could store only the necessary bits.
        # Here we store full int and rely on Python's integer handling.

        for c in current_set:
            base = c << 3
            for x in range(8):
                candidate = base + x
                # candidate now has (bit_length) bits considered.
                # Check output:
                if f(candidate) == next_out:
                    new_set.append(candidate)

        current_set = new_set

        if not current_set:
            # No candidates match at this stage, no solution
            return []

    # After processing all outputs, current_set contains all possible A values (with bit_length bits)
    # that produce the entire output sequence from first to last iteration.
    # Actually, these represent the final A before the last iteration is reversed back to the start.
    # In a real scenario, after N iterations, you'd have the full original A since we kept adding bits.

    return current_set

def main():
    # Example usage:
    # Suppose we have an output sequence from the "program":
    # This is just an example. You'd use the actual output sequence from your puzzle.
    example_outputs = [3, 5, 2, 1]  # some arbitrary short sequence
    example_outputs = [0, 3, 5, 4, 3, 0]  # some arbitrary short sequence
    example_outputs = [1,5,4,3,0]  # some arbitrary short sequence
    example_outputs = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3]  # some arbitrary short sequence
    example_outputs = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0]  # some arbitrary short sequence
    example_outputs = [0,3,5,4,3,0]  # some arbitrary short sequence

    solutions = solve_outputs(example_outputs)
    if solutions:
        print("Possible initial A values that produce the given outputs:")
        # solutions may contain multiple values. Let's print a few.
        for s in solutions[:10]:
            print(s)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
