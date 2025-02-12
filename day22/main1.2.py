def next_secret(secret):
    """
    Given the current secret number, compute the next secret number by performing:
    1. Multiply by 64, XOR with current secret, prune.
    2. Divide by 32 (floor), XOR with current secret, prune.
    3. Multiply by 2048, XOR with current secret, prune.
    """
    # Step 1: Multiply by 64, XOR with current secret, prune
    temp = (secret * 64)
    secret = (secret ^ temp) % 16777216  # Prune by modulo 16,777,216

    # Step 2: Divide by 32 (floor division), XOR with current secret, prune
    temp = secret // 32
    secret = (secret ^ temp) % 16777216

    # Step 3: Multiply by 2048, XOR with current secret, prune
    temp = secret * 2048
    secret = (secret ^ temp) % 16777216

    return secret

def next_secret(secret):
    """
    Given the current secret number, compute the next secret number by performing:
    1. Multiply by 64 (2^6) using left shift, XOR with current secret, and prune.
    2. Divide by 32 (2^5) using right shift, XOR with current secret, and prune.
    3. Multiply by 2048 (2^11) using left shift, XOR with current secret, and prune.
    
    All operations ensure that the secret number remains within 24 bits by applying a bitmask.
    """
    # Define constants for bit operations
    MULTIPLY_64_SHIFT = 6      # 2^6 = 64
    DIVIDE_32_SHIFT = 5        # 2^5 = 32
    MULTIPLY_2048_SHIFT = 11   # 2^11 = 2048
    MODULO_MASK = 0xFFFFFF     # 24-bit mask (2^24 - 1) = 16777215

    # Step 1: Multiply by 64 using left shift, then XOR with current secret, and prune
    temp = secret << MULTIPLY_64_SHIFT          # Equivalent to secret * 64
    secret = (secret ^ temp) & MODULO_MASK      # XOR and prune to 24 bits

    # Step 2: Divide by 32 using right shift, then XOR with current secret, and prune
    temp = secret >> DIVIDE_32_SHIFT            # Equivalent to secret // 32
    secret = (secret ^ temp) & MODULO_MASK      # XOR and prune to 24 bits

    # Step 3: Multiply by 2048 using left shift, then XOR with current secret, and prune
    temp = secret << MULTIPLY_2048_SHIFT        # Equivalent to secret * 2048
    secret = (secret ^ temp) & MODULO_MASK      # XOR and prune to 24 bits

    return secret


def simulate_buyer(initial_secret, steps=2000):
    """
    Simulate the generation of 'steps' secret numbers for a buyer starting with 'initial_secret'.
    Returns the 'steps'th secret number.
    """
    secret = initial_secret
    for _ in range(steps):
        secret = next_secret(secret)
    return secret

def main():
    import os

    # Define the filename (ensure it's in the same directory as the script)
    filename = 'day22/input.txt'
    filename = 'day22/input2.txt'

    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"Error: The file '{filename}' does not exist in the current directory.")
        return

    initial_secrets = []
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                stripped_line = line.strip()
                if stripped_line:  # Skip empty lines
                    try:
                        secret = int(stripped_line)
                        initial_secrets.append(secret)
                    except ValueError:
                        print(f"Warning: Line {line_number} in '{filename}' is not a valid integer and will be skipped.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    if not initial_secrets:
        print("No valid initial secrets found in the file.")
        return

    # For each buyer, simulate 2000 steps and collect the 2000th secret number
    total = 0
    for idx, initial_secret in enumerate(initial_secrets, start=1):
        secret_2000 = simulate_buyer(initial_secret, steps=2000)
        print(f"Buyer {idx}: 2000th secret number = {secret_2000}")
        total += secret_2000

    # Output the sum of all 2000th secret numbers
    print(f"\nTotal sum of all 2000th secret numbers: {total}")

if __name__ == "__main__":
    main()
