def f(A):
    B = (A % 8) ^ 2
    C = A >> B
    return (B ^ C ^ 3) % 8

def backward_solve_from_end(outputs):
    reversed_outputs = outputs[::-1]

    # Find all 10-bit numbers that produce the last output:
    last_out = reversed_outputs[0]
    current_set = [a for a in range(1024) if f(a) == last_out]

    bit_length = 10

    # Process each preceding output:
    for i in range(1, len(reversed_outputs)):
        next_out = reversed_outputs[i]
        new_set = []
        bit_length += 3

        # For each candidate c, prev_A = (c << 3) + x for x in [0..7]
        # Keep those that produce next_out
        for c in current_set:
            base = c << 3
            for x in range(8):
                candidate = base + x
                if f(candidate) == next_out:
                    new_set.append(candidate)

        current_set = new_set
        if not current_set:
            return []

    return current_set

def main():
    # Given example program:
    outputs = [0,3,5,4,3,0]
    solutions = backward_solve_from_end(outputs)

    if solutions:
        # Sort the solutions before printing/searching:
        solutions.sort()
        print("Number of solutions found:", len(solutions))

        # Print first 20 after sorting:
        print("First 20 solutions:")
        for s in solutions[:20]:
            print(s)

        # Check if 117440 is in solutions
        if 117440 in solutions:
            print("117440 found in solutions!")
        else:
            print("117440 not found in the final solution set.")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
