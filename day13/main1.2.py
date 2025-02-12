import re
import os
import sys

def read_machines(file_path):
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


def find_min_tokens(machine, max_presses=100):
    X_A = machine['X_A']
    Y_A = machine['Y_A']
    X_B = machine['X_B']
    Y_B = machine['Y_B']
    X_p = machine['X_p']
    Y_p = machine['Y_p']
    
    min_tokens = None  # Initialize with None to handle no solution cases
    
    for a in range(0, max_presses + 1):
        for b in range(0, max_presses + 1):
            total_X = a * X_A + b * X_B
            total_Y = a * Y_A + b * Y_B
            
            if total_X == X_p and total_Y == Y_p:
                tokens = 3 * a + b
                if (min_tokens is None) or (tokens < min_tokens):
                    min_tokens = tokens
    return min_tokens


def calculate_total_tokens(machines, max_presses=100):
    total_tokens = 0
    won_prizes = 0  # To track how many prizes were successfully won
    
    for idx, machine in enumerate(machines, start=1):
        min_tokens = find_min_tokens(machine, max_presses)
        if min_tokens is not None:
            print(f"Machine {idx}: Minimum tokens = {min_tokens}")
            total_tokens += min_tokens
            won_prizes +=1
        else:
            print(f"Machine {idx}: No valid combination found.")
    
    print(f"Total tokens to win {won_prizes} prizes: {total_tokens}")
    return total_tokens

def main():
    directory = os.path.dirname(__file__) + '\\'
    file_path = directory + 'input.txt'
    # Uncomment the following line if using a different input file
    #file_path = directory + 'input2.txt'

    machines = read_machines(file_path)
    print(f"Total machines parsed: {len(machines)}")
    for idx, machine in enumerate(machines, start=1):
        print(f"Machine {idx}: Button A -> X+{machine['X_A']}, Y+{machine['Y_A']} | Button B -> X+{machine['X_B']}, Y+{machine['Y_B']} | Prize at X={machine['X_p']}, Y={machine['Y_p']}")

    total_tokens = calculate_total_tokens(machines, max_presses=100)
    print(f"Final Total Tokens Required: {total_tokens}")

if __name__ == "__main__":
    main()