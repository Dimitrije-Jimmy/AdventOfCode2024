def f(A):
    """Simulate the output-producing function based on A."""
    B = (A % 8) ^ 1
    C = A >> B
    B = B ^ 4
    B = B ^ C
    return B % 8

def generate_candidates_for_output(output, current_candidates):
    """
    Reverse the operations to generate all possible A values that could produce the given output.

    Args:
        output (int): The required output at the current step.
        current_candidates (set): The set of A values from the previous step.

    Returns:
        set: New set of A candidates for the previous step.
    """
    new_candidates = set()

    # For each current candidate, undo the division by 8 and explore all 8 possible lower bits (0..7)
    for candidate in current_candidates:
        for lower_bits in range(8):
            A = (candidate << 3) + lower_bits  # Undo A // 8
            if f(A) == output:
                new_candidates.add(A)

    return new_candidates

def reverse_engineer_program(program):
    """
    Reverse the program to determine the smallest initial A that produces the program as output.

    Args:
        program (list): The program input, which must match the output sequence.

    Returns:
        int: The smallest initial A value that produces the program as output.
    """
    n = len(program)
    outputs = program[::-1]  # Reverse the program to work backward

    # Step 1: Start with the last output
    candidates = set()
    for A in range(8):  # Only need to consider A values with the lowest 3 bits matching
        if f(A) == outputs[0]:
            candidates.add(A)

    # Step 2: Work backward through the outputs
    for output in outputs[1:]:
        candidates = generate_candidates_for_output(output, candidates)
        if not candidates:
            return None  # No valid candidates found

    # Step 3: Validate candidates by running the program forward
    def execute_forward(A, program_length):
        """Run the forward program to produce the output sequence."""
        outputs = []
        for _ in range(program_length):
            B = (A % 8) ^ 1
            C = A >> B
            B = B ^ 4
            B = B ^ C
            outputs.append(B % 8)
            A = A // 8
        return outputs

    valid_candidates = []
    for A in candidates:
        if execute_forward(A, n) == program:
            valid_candidates.append(A)

    return min(valid_candidates) if valid_candidates else None

def main():
    # Example program (output sequence)
    program = [0, 3, 5, 4, 3, 0]  # Program input that must match the output sequence

    # Reverse engineer the program to find the smallest initial A
    result = reverse_engineer_program(program)
    if result is not None:
        print(f"The smallest initial A value that produces the program as output is: {result}")
    else:
        print("No valid solution found.")

if __name__ == "__main__":
    main()
