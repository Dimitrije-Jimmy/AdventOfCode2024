def next_secret(secret):
    """
    Given the current secret number, compute the next secret number by performing:
    1. Multiply by 64, XOR with current secret, prune.
    2. Divide by 32 (floor), XOR with current secret, prune.
    3. Multiply by 2048, XOR with current secret, prune.
    """
    # Step 1
    temp = (secret * 64) & 0xFFFFFFFF  # Ensure we handle large numbers correctly
    secret = (secret ^ temp) % 16777216

    # Step 2
    temp = secret // 32
    secret = (secret ^ temp) % 16777216

    # Step 3
    temp = (secret * 2048) & 0xFFFFFFFF
    secret = (secret ^ temp) % 16777216

    return secret

def simulate_buyer(initial_secret, steps=2000):
    """
    Simulate the generation of 'steps' secret numbers for a buyer starting with 'initial_secret'.
    Returns the 2000th secret number.
    """
    secret = initial_secret
    for _ in range(steps):
        secret = next_secret(secret)
    return secret

def main():
    import sys

    # Read input: list of initial secret numbers, one per line
    initial_secrets = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            initial_secrets.append(int(line))

    # For each buyer, simulate 2000 steps and collect the 2000th secret number
    total = 0
    for initial_secret in initial_secrets:
        secret_2000 = simulate_buyer(initial_secret, steps=2000)
        total += secret_2000

    # Output the sum of all 2000th secret numbers
    print(total)

if __name__ == "__main__":
    main()
