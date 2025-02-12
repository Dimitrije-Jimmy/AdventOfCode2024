Register_A =  44348299
Register_B =  0
Register_C =  0

Program = [2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0]

# Test input
Register_A =  729
Register_B =  0
Register_C =  0

Program = [0,1,5,4,3,0]

import sys

def execute_program(registers, program):
    """
    Executes the program on the Chronospatial Computer.

    Args:
        registers (dict): Initial values of registers A, B, C.
        program (list of int): List of integers representing the program.

    Returns:
        str: Comma-separated string of outputs produced by 'out' instructions.
    """
    A = registers.get('A', 0)
    B = registers.get('B', 0)
    C = registers.get('C', 0)
    outputs = []
    IP = 0  # Instruction Pointer

    # Define operand types per opcode
    operand_types = {
        0: 'combo',   # adv
        1: 'literal', # bxl
        2: 'combo',   # bst
        3: 'literal', # jnz
        4: 'ignored', # bxc
        5: 'combo',   # out
        6: 'combo',   # bdv
        7: 'combo',   # cdv
    }

    while IP < len(program):
        opcode = program[IP]
        if IP + 1 >= len(program):
            # Operand missing; halt the program
            break
        operand = program[IP + 1]
        otype = operand_types.get(opcode, 'invalid')

        # Fetch operand value based on type
        if otype == 'literal':
            operand_value = operand
        elif otype == 'combo':
            if 0 <= operand <= 3:
                operand_value = operand
            elif operand == 4:
                operand_value = A
            elif operand == 5:
                operand_value = B
            elif operand == 6:
                operand_value = C
            else:
                # Invalid operand
                operand_value = None
        elif otype == 'ignored':
            operand_value = None
        else:
            operand_value = None

        if opcode == 0:  # adv: A = A // (2^(operand_value))
            denominator = 1 << operand_value
            if denominator == 0:
                return ",".join(map(str, outputs))
            A = A // denominator
            IP += 2

        elif opcode == 1:  # bxl: B = B ^ operand(literal)
            if otype != 'literal':
                return ",".join(map(str, outputs))
            B = B ^ operand_value
            IP += 2

        elif opcode == 2:  # bst: B = (operand(combo) % 8)
            if otype != 'combo':
                return ",".join(map(str, outputs))
            B = operand_value % 8
            IP += 2

        elif opcode == 3:  # jnz: if A != 0 jump to operand(literal)
            if otype != 'literal':
                return ",".join(map(str, outputs))
            if A != 0:
                IP = operand_value
            else:
                IP += 2

        elif opcode == 4:  # bxc: B = B ^ C
            B = B ^ C
            IP += 2

        elif opcode == 5:  # out: outputs append operand(combo)%8
            if otype != 'combo':
                return ",".join(map(str, outputs))
            out_val = operand_value % 8
            outputs.append(out_val)
            IP += 2

        elif opcode == 6:  # bdv: B = A // (2^(operand_value))
            denominator = 1 << operand_value
            if denominator == 0:
                return ",".join(map(str, outputs))
            B = A // denominator
            IP += 2

        elif opcode == 7:  # cdv: C = A // (2^(operand_value))
            denominator = 1 << operand_value
            if denominator == 0:
                return ",".join(map(str, outputs))
            C = A // denominator
            IP += 2

        else:
            # Invalid opcode
            return ",".join(map(str, outputs))

    return ",".join(map(str, outputs))


def gnarly_expr(a_bits):
    """
    Given the 3 bits we've chosen for this iteration, what output does it produce?
    Assuming that the 'out' instruction just outputs (A % 8), which matches
    the conceptual "lowest three bits of A" logic.

    If your actual logic is different (for example, if the output depends on B or C),
    you'll need to incorporate that logic here.
    """
    # Here, a_bits is just the lowest 3 bits of A at that iteration, so:
    return a_bits % 8


def is_loop_finished(A):
    # Assume the loop ends when A = 0
    return A == 0


def backward_solve(program, final_outputs):
    """
    Given the final output sequence (final_outputs), try to reconstruct the initial A.
    We assume each output corresponds to the lowest 3 bits of A at that iteration.
    Backward:
    - Start from A=0 at the end.
    - For each output going backwards, find which 3-bit value produces that output,
      then integrate that into A.
    """

    def helper(outputs_reversed, current_A):
        # If we've assigned all outputs (no more outputs to match) and loop finished (A=0):
        if not outputs_reversed and is_loop_finished(current_A):
            return current_A

        if not outputs_reversed:
            # Outputs not fully matched, or didn't end at A=0
            return None

        desired_output = outputs_reversed[-1]

        # Try all 3-bit values for this iteration (0 to 7)
        for candidate_bits in range(8):
            if gnarly_expr(candidate_bits) == desired_output:
                # Going backward:
                # Forward we took lowest 3 bits from A. That means forward was something like:
                # A_next = A_before // 8 (if the code reduces A like adv with known power).
                # Backwards: to restore these bits, we do: A_before = (A_after << 3) + candidate_bits
                # Assuming each iteration effectively shifts A down by 3 bits forward.

                # Here we guess that each iteration effectively consumed 3 bits of A (division by 8).
                # If your program uses different divisions, adjust accordingly.
                A_before = (current_A << 3) | candidate_bits

                # Now recurse with one fewer output:
                res = helper(outputs_reversed[:-1], A_before)
                if res is not None:
                    return res

        return None

    # We start backward with current_A = 0 and final_outputs reversed:
    reversed_outs = final_outputs[::-1]
    return helper(reversed_outs, 0)


def main():
    # Example usage:
    # Let's take the sample with program = [0,1,5,4,3,0]
    # and expected output = 4,6,3,5,6,3,5,2,1,0 from the puzzle statement.

    registers = {'A': 729, 'B':0, 'C':0}
    program = [0,1,5,4,3,0]
    expected_output_str = "4,6,3,5,6,3,5,2,1,0"
    expected_output = list(map(int, expected_output_str.split(',')))

    # Check forward with the given A:
    forward_result_str = execute_program(registers, program)
    forward_result = list(map(int, forward_result_str.split(','))) if forward_result_str else []
    print("Forward check with A=729:", forward_result_str, "Matches:", forward_result == expected_output)

    # Now try backward solving:
    # Suppose we only know we want expected_output. Let's try to find A_start.
    A_candidate = backward_solve(program, expected_output)

    if A_candidate is not None:
        print(f"Backward found A_start = {A_candidate}")
        # Verify:
        verify_out_str = execute_program({'A': A_candidate, 'B':0, 'C':0}, program)
        verify_out = list(map(int, verify_out_str.split(','))) if verify_out_str else []
        print("Verification output:", verify_out_str, "Matches:", verify_out == expected_output)
    else:
        print("No A found by backward solving.")


if __name__ == "__main__":
    main()
