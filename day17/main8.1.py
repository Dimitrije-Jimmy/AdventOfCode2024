def reverse_program(outputs, program_length):
    """
    Reverse the program to determine the minimum initial A value
    that produces the given output sequence.

    Args:
        outputs (list): The list of outputs to reverse-engineer.
        program_length (int): The number of iterations in the program.

    Returns:
        int: The minimum initial A value that produces the given output sequence.
    """
    def f_mod(a):
        """Compute B (A mod 8) and C based on the given operations."""
        B = (a % 8) ^ 1
        C = a >> B
        B = B ^ 4
        B = B ^ C
        return B % 8  # The value outputted by the program

    # Breadth-First Search (BFS) Queue: Start with candidates that produce the last output
    candidates = set()

    # Step 1: Initialize with numbers that produce the last output
    for a_candidate in range(8):  # Only check the last 3 bits (0-7)
        if f_mod(a_candidate) == outputs[-1]:
            candidates.add(a_candidate)

    # Step 2: Reverse-engineer the sequence
    for output in reversed(outputs[:-1]):  # Go backward through outputs (excluding last)
        new_candidates = set()

        for a in candidates:
            # Reverse the division by 8: Try all possible lower 3 bits
            for x in range(8):
                candidate = (a << 3) + x  # Multiply by 8 and add 0..7
                if f_mod(candidate) == output:
                    new_candidates.add(candidate)

        candidates = new_candidates  # Move to the previous state

        if not candidates:
            return -1  # If no candidates are valid, return failure

    return min(candidates)  # Return the smallest valid A


def main():
    # Example output and program:
    outputs = [0, 3, 5, 4, 3, 0]  # Given outputs
    outputs = [1, 3, 5, 4, 3, 0]  # Given outputs
    program_length = len(outputs)  # Number of iterations (length of the program)

    # Reverse the program to find the minimum A
    min_initial_A = reverse_program(outputs, program_length)

    if min_initial_A != -1:
        print(f"The minimum initial A that produces the outputs {outputs} is: {min_initial_A}")
    else:
        print("No valid solution found.")

if __name__ == "__main__":
    main()
