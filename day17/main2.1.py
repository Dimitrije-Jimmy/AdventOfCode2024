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

    while IP < len(program):
        opcode = program[IP]
        if IP + 1 >= len(program):
            # Operand missing; halt the program
            break
        operand = program[IP + 1]

        # Determine operand type based on instruction
        # Each instruction specifies the type of its operand; assuming it's predefined per opcode
        # However, the problem statement doesn't specify which opcode uses which operand type
        # We'll assume:
        # - adv (0): combo operand
        # - bxl (1): literal operand
        # - bst (2): combo operand
        # - jnz (3): literal operand
        # - bxc (4): operand is read but ignored
        # - out (5): combo operand
        # - bdv (6): combo operand
        # - cdv (7): combo operand

        # Define operand types per opcode
        # 0: combo
        # 1: literal
        # 2: combo
        # 3: literal
        # 4: operand ignored
        # 5: combo
        # 6: combo
        # 7: combo

        # Mapping opcodes to operand types
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

        operand_type = operand_types.get(opcode, 'invalid')

        # Fetch operand value based on its type
        if operand_type == 'literal':
            operand_value = operand
        elif operand_type == 'combo':
            if 0 <= operand <= 3:
                operand_value = operand
            elif operand == 4:
                operand_value = A
            elif operand == 5:
                operand_value = B
            elif operand == 6:
                operand_value = C
            else:
                # Invalid operand (7), but per problem statement, it won't appear
                operand_value = None
        elif operand_type == 'ignored':
            operand_value = None
        else:
            # Invalid operand type
            operand_value = None

        # Execute instruction based on opcode
        if opcode == 0:  # adv
            denominator = 2 ** operand_value
            if denominator == 0:
                print(f"Error: Division by zero at IP {IP}")
                return ",".join(map(str, outputs))
            result = A // denominator
            A = result
            # Debug
            # print(f"adv: A={A} after dividing by 2^{operand_value}={denominator}")
            IP += 2

        elif opcode == 1:  # bxl
            if operand_type != 'literal':
                print(f"Error: bxl expects a literal operand at IP {IP}")
                return ",".join(map(str, outputs))
            result = B ^ operand_value
            B = result
            # Debug
            # print(f"bxl: B={B} after XOR with {operand_value}")
            IP += 2

        elif opcode == 2:  # bst
            if operand_type != 'combo':
                print(f"Error: bst expects a combo operand at IP {IP}")
                return ",".join(map(str, outputs))
            result = operand_value % 8
            B = result
            # Debug
            # print(f"bst: B={B} after setting to {operand_value} % 8")
            IP += 2

        elif opcode == 3:  # jnz
            if operand_type != 'literal':
                print(f"Error: jnz expects a literal operand at IP {IP}")
                return ",".join(map(str, outputs))
            if A != 0:
                IP = operand_value
                # Debug
                # print(f"jnz: A={A} !=0, jumping to {IP}")
            else:
                # Debug
                # print(f"jnz: A={A} ==0, no jump")
                IP += 2

        elif opcode == 4:  # bxc
            result = B ^ C
            B = result
            # Debug
            # print(f"bxc: B={B} after XOR with C={C}")
            IP += 2  # Operand is read but ignored

        elif opcode == 5:  # out
            if operand_type != 'combo':
                print(f"Error: out expects a combo operand at IP {IP}")
                return ",".join(map(str, outputs))
            output_value = operand_value % 8
            outputs.append(output_value)
            # Debug
            # print(f"out: Output {output_value}")
            IP += 2

        elif opcode == 6:  # bdv
            denominator = 2 ** operand_value
            if denominator == 0:
                print(f"Error: Division by zero at IP {IP}")
                return ",".join(map(str, outputs))
            result = A // denominator
            B = result
            # Debug
            # print(f"bdv: B={B} after dividing A={A} by 2^{operand_value}={denominator}")
            IP += 2

        elif opcode == 7:  # cdv
            denominator = 2 ** operand_value
            if denominator == 0:
                print(f"Error: Division by zero at IP {IP}")
                return ",".join(map(str, outputs))
            result = A // denominator
            C = result
            # Debug
            # print(f"cdv: C={C} after dividing A={A} by 2^{operand_value}={denominator}")
            IP += 2

        else:
            print(f"Error: Invalid opcode {opcode} at IP {IP}")
            return ",".join(map(str, outputs))

    return ",".join(map(str, outputs))

def find_minimal_A(program, initial_B=0, initial_C=0, max_A=10**6):
    """
    Finds the smallest positive initial value for register A that causes the program
    to output a copy of itself.

    Args:
        program (list of int): The program to execute.
        initial_B (int): Initial value of register B.
        initial_C (int): Initial value of register C.
        max_A (int): Maximum A value to search to prevent infinite loops.

    Returns:
        int: The smallest positive initial value for register A that satisfies the condition.
             Returns -1 if not found within the search limit.
    """
    for A in range(1, max_A + 1):
        registers = {'A': A, 'B': initial_B, 'C': initial_C}
        output = execute_program(registers, program)
        if output is None:
            continue  # Skip if program didn't execute correctly
        if output == program:
            print(f"Solution found! Initial A value: {A}")
            return A
        if A % 10000 == 0:
            print(f"Checked A = {A}, not a solution yet...")
    print("No solution found within the search limit.")
    return -1

def find_minimum_A_for_self_replicating_program(program):
    # We assume B=0, C=0 as specified by the problem.
    B = 0
    C = 0
    
    A = 1
    while True:
        if A % 10000 == 0:
            print(f"Checked A = {A}, not a solution yet...")
        
        registers = {'A': A, 'B': B, 'C': C}
        output_str = execute_program(registers, program)
        
        # Convert the output to a list of integers for easy comparison
        if output_str.strip() == "":
            output_list = []
        else:
            output_list = list(map(int, output_str.split(',')))
        
        if output_list == program:
            return A
        A += 1

# Example usage:
program = [0,3,5,4,3,0]
result = find_minimum_A_for_self_replicating_program(program)
print("The lowest positive A that causes the program to output a copy of itself:", result)

# Example usage:
program = [2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0]
result = find_minimum_A_for_self_replicating_program(program)
print("The lowest positive A that causes the program to output a copy of itself:", result)


exit()
def main():
    """
    Main function to execute the Chronospatial Computer simulation.
    """
    # Example input:
    # Register A: 729
    # Register B: 0
    # Register C: 0
    # Program: 0,1,5,4,3,0
    #
    # Expected Output: 4,6,3,5,6,3,5,2,1,0

    # For demonstration purposes, we'll define a function to parse input.
    # In practice, you might read from a file or standard input.

    # Sample Inputs
    samples = [
        {
            'registers': {'A': 44348299, 'B': 0, 'C': 0},
            'program': [2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0],
            'expected_output': "Not known"
        },
        # Add more samples if needed
    ]
    samples2 = [
        {
            'registers': {'A': 729, 'B': 0, 'C': 0},
            'program': [0,1,5,4,3,0],
            'expected_output': "4,6,3,5,6,3,5,2,1,0"
        },
        # Add more samples if needed
    ]
    samples3 = [
        {
            'registers': {'A': 2024, 'B': 0, 'C': 0},
            'program': [0,3,5,4,3,0],
            'expected_output': "0,3,5,4,3,0"
        }
    ]
    samples4 = [
        {
            'registers': {'A': 117440, 'B': 0, 'C': 0},
            'program': [0,3,5,4,3,0],
            'expected_output': "0,3,5,4,3,0"
        }
    ]
    samples = samples4

    # Run samples
    for idx, sample in enumerate(samples, 1):
        print(f"--- Sample {idx} ---")
        registers = sample['registers']
        program = sample['program']
        expected = sample['expected_output']
        output = execute_program(registers, program)
        print(f"Register A: {registers['A']}")
        print(f"Register B: {registers['B']}")
        print(f"Register C: {registers['C']}")
        print(f"Program: {','.join(map(str, program))}")
        print(f"Expected Output: {expected}")
        print(f"Actual Output:   {output}")
        print(f"Test Passed: {output == expected}\n")

    # For user input, you can modify the following section:
    """
    # Read initial register values
    A = int(input("Register A: "))
    B = int(input("Register B: "))
    C = int(input("Register C: "))

    # Read program as comma-separated values
    program_input = input("Program: ")
    program = list(map(int, program_input.strip().split(',')))

    # Initialize registers
    registers = {'A': A, 'B': B, 'C': C}

    # Execute program
    output = execute_program(registers, program)

    # Print output
    print(f"Output: {output}")
    """

    # Part two:
    # Replace this with your actual program input
    program_input = "0,3,5,4,3,0"  # Example program; replace as needed

    # Parse the program list
    program = list(map(int, program_input.strip().split(',')))

    # Search for the minimal A that causes the program to output a copy of itself
    minimal_A = find_minimal_A(program, initial_B=0, initial_C=0)

    if minimal_A != -1:
        print(f"The lowest positive initial value for register A is: {minimal_A}")
    else:
        print("No valid initial A found within the search limit.")

if __name__ == "__main__":
    main()
