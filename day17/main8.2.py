def reverse_outputs(outputs):
    """
    Given the output sequence, compute the initial A that would produce this sequence.
    """
    outputs = list(map(int, outputs))  # Ensure outputs are integers
    A_next = 0  # Loop ends when A == 0
    for output in reversed(outputs):
        # Possible B1 values that result in the observed output
        B1_candidates = [b for b in range(8) if b % 8 == output]
        A_prev_candidates = []

        for B1 in B1_candidates:
            # B1 = B0 ^ C
            # We need to find B0 and C such that B1 = B0 ^ C

            # Since C = (A1) // (2^B0)
            # And A1 = A_prev ^ 1
            # And A1 = A_prev ^ 1
            # Also, A_prev = ((A_next * 8) ^ 5) ^ 1 (derived from A_next = ((A_prev ^ 1) ^ 5) // 8)

            # Rearranging the equation:
            # A_prev = ((A_next * 8) ^ 5) ^ 1

            A_prev = ((A_next * 8) ^ 5) ^ 1
            B0 = A_prev % 8

            A1 = A_prev ^ 1
            C = A1 // (1 << B0)  # C = A1 // (2^B0)

            # Check if B1 = B0 ^ C
            if B1 == B0 ^ C:
                # Valid candidate
                A_prev_candidates.append(A_prev)

        if not A_prev_candidates:
            # No valid A_prev found for this output, backtrack
            return None

        # Since A_prev is uniquely determined in this setup, we can pick the first candidate
        A_next = A_prev_candidates[0]  # Or consider all candidates if multiple paths are possible

    # After processing all outputs, A_next is the initial A
    return A_next

def execute_program(registers, program):
    """
    Executes the program on the Chronospatial Computer.

    (The same execute_program function as in your code)
    """
    # ... [Your existing execute_program code] ...
    A = registers.get('A', 0)
    B = registers.get('B', 0)
    C = registers.get('C', 0)
    outputs = []
    IP = 0  # Instruction Pointer

    # ... [Rest of your execute_program code] ...

    return ",".join(map(str, outputs))

def main():
    # Example output sequence from your program
    outputs_str = "0,3,5,4,3,0"
    outputs = outputs_str.strip().split(',')

    # Reverse engineer the initial A
    A_initial = reverse_outputs(outputs)
    if A_initial is not None:
        print(f"Found initial A: {A_initial}")
        # Verify by running the program forward
        registers = {'A': A_initial, 'B': 0, 'C': 0}
        program = [0,3,5,4,3,0]  # Your program
        output = execute_program(registers, program)
        print(f"Verification Output: {output}")
        if output == outputs_str:
            print("Verification successful!")
        else:
            print("Verification failed.")
    else:
        print("No valid initial A found.")

if __name__ == "__main__":
    main()
