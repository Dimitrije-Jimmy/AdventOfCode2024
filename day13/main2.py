import re
import os
import sys

def read_machines(file_path):
    """
    Reads the input file and parses each machine's configuration.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list of dict: Each dict contains button movements and prize coordinates.
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split the input into blocks separated by empty lines
    blocks = [block.strip() for block in content.split('\n\n') if block.strip()]
    
    machines = []
    
    # Define regex patterns to extract numbers
    button_a_pattern = r'Button A:\s*X\+(\d+),\s*Y\+(\d+)'
    button_b_pattern = r'Button B:\s*X\+(\d+),\s*Y\+(\d+)'
    prize_pattern = r'Prize:\s*X=(\d+),\s*Y=(\d+)'
    
    for block in blocks:
        a_match = re.search(button_a_pattern, block)
        b_match = re.search(button_b_pattern, block)
        p_match = re.search(prize_pattern, block)
        
        if a_match and b_match and p_match:
            X_A, Y_A = int(a_match.group(1)), int(a_match.group(2))
            X_B, Y_B = int(b_match.group(1)), int(b_match.group(2))
            X_p, Y_p = int(p_match.group(1)), int(p_match.group(2))
            
            machines.append({
                'X_A': X_A,
                'Y_A': Y_A,
                'X_B': X_B,
                'Y_B': Y_B,
                'X_p': X_p,
                'Y_p': Y_p
            })
        else:
            print("Warning: Failed to parse a machine block:")
            print(block)
    
    return machines

def adjust_prize_coordinates(machines, delta=10_000_000_000_000):
    """
    Adjusts the prize coordinates by adding a delta to both X and Y.

    Args:
        machines (list of dict): List of machines with prize coordinates.
        delta (int, optional): The value to add to both X and Y. Defaults to 10^13.

    Returns:
        list of dict: Machines with adjusted prize coordinates.
    """
    for machine in machines:
        machine['X_p'] += delta
        machine['Y_p'] += delta
    return machines

def find_min_tokens(machine):
    """
    Finds the minimal number of tokens required to win the prize for a given machine.

    Args:
        machine (dict): A machine's configuration.

    Returns:
        int or None: The minimal tokens required, or None if no solution exists.
    """
    X_A = machine['X_A']
    Y_A = machine['Y_A']
    X_B = machine['X_B']
    Y_B = machine['Y_B']
    X_p = machine['X_p']
    Y_p = machine['Y_p']
    
    det = X_A * Y_B - X_B * Y_A
    
    if det == 0:
        # No unique solution exists
        return None
    
    a_num = Y_p * X_B - Y_B * X_p
    #b_num = X_p * Y_A - Y_p * X_A
    b_num = Y_p * X_A - Y_A * X_p
    
    # Check if a_num and b_num are divisible by det
    if a_num % det != 0 or b_num % det != 0:
        # No integer solution exists
        return None
    
    a = a_num // det
    b = b_num // det
    
    #if a < 0 or b < 0:
    #    # Negative presses are invalid
    #    return None
    
    # Calculate token cost
    tokens = 3 * a + b
    
    return tokens


def calculate_total_tokens(machines):
    """
    Calculates the total tokens required to win all possible prizes.

    Args:
        machines (list of dict): List of machines with configurations.

    Returns:
        int: Total tokens required.
    """
    total_tokens = 0
    won_prizes = 0  # To track how many prizes were successfully won
    
    for idx, machine in enumerate(machines, start=1):
        tokens = find_min_tokens(machine)
        if tokens is not None:
            print(f"Machine {idx}: Minimum tokens = {tokens}")
            total_tokens += tokens
            won_prizes +=1
        else:
            print(f"Machine {idx}: No valid combination found.")
    
    print(f"Total tokens to win {won_prizes} prizes: {total_tokens}")
    return total_tokens

def main():
    """
    Main function to execute the solution.
    """
    directory = os.path.dirname(__file__) + '\\'
    file_path = os.path.join(directory, 'input.txt')
    # Uncomment the following line if using a different input file
    file_path = os.path.join(directory, 'input2.txt')
    
    machines = read_machines(file_path)
    print(f"Total machines parsed: {len(machines)}")
    for idx, machine in enumerate(machines, start=1):
        print(f"Machine {idx}: Button A -> X+{machine['X_A']}, Y+{machine['Y_A']} | "
              f"Button B -> X+{machine['X_B']}, Y+{machine['Y_B']} | "
              f"Prize at X={machine['X_p']}, Y={machine['Y_p']}")
    
    # Adjust prize coordinates for Part Two
    machines = adjust_prize_coordinates(machines)
    print(machines)
    
    total_tokens = calculate_total_tokens(machines)
    print(f"Final Total Tokens Required: {total_tokens}")
    
if __name__ == "__main__":
    main()
