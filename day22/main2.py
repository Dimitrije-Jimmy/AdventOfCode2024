def next_secret(secret):
    """
    Given the current secret number, compute the next secret number by performing:
    1. Multiply by 64, XOR with current secret, prune.
    2. Divide by 32 (floor), XOR with current secret, prune.
    3. Multiply by 2048, XOR with current secret, prune.
    """
    # Step 1: Multiply by 64, XOR with current secret, prune
    temp = secret * 64
    secret = (secret ^ temp) % 16777216  # Prune by modulo 16,777,216

    # Step 2: Divide by 32 (floor division), XOR with current secret, prune
    temp = secret // 32
    secret = (secret ^ temp) % 16777216

    # Step 3: Multiply by 2048, XOR with current secret, prune
    temp = secret * 2048
    secret = (secret ^ temp) % 16777216

    return secret

def simulate_buyer(initial_secret, steps=2000):
    """
    Simulate the generation of 'steps' secret numbers for a buyer starting with 'initial_secret'.
    Returns a tuple of (prices, changes).
    - prices: List of prices (last digits of secret numbers), including the initial price.
    - changes: List of price changes between consecutive prices.
    """
    prices = []
    changes = []

    # Generate the initial price
    secret = initial_secret
    initial_price = secret % 10
    prices.append(initial_price)

    # Generate 'steps' new secret numbers
    for _ in range(steps):
        secret = next_secret(secret)
        price = secret % 10
        prices.append(price)
        change = price - prices[-2]  # Current price minus previous price
        changes.append(change)

    return prices, changes

def main():
    import os
    from collections import defaultdict

    # Define the filename (ensure it's in the same directory as the script)
    filename = 'day22/input.txt'
    #filename = 'day22/input2.txt'
    filename = 'day22/input3.txt'

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

    # Initialize a dictionary to map sequences to their total sum of prices
    sum_p = defaultdict(int)

    # Process each buyer
    for idx, initial_secret in enumerate(initial_secrets, start=1):
        prices, changes = simulate_buyer(initial_secret, steps=2000)

        # Check if there are enough changes to form a sequence of four
        if len(changes) < 4:
            continue  # Not enough changes to form a sequence

        # Set to keep track of sequences already seen for this buyer
        sequences_seen = set()

        # Iterate through the changes with a sliding window of four
        for j in range(len(changes) - 3):
            # Extract the sequence of four consecutive changes
            sequence = tuple(changes[j:j+4])

            # If this sequence hasn't been seen before for this buyer
            if sequence not in sequences_seen:
                sequences_seen.add(sequence)
                # The price at which the sequence completes is the price after the fourth change
                # Which corresponds to prices[j + 4] (since j starts at 0)
                if (j + 4) < len(prices):
                    p_i = prices[j + 4]
                    sum_p[sequence] += p_i

    # After processing all buyers, find the sequence with the maximum total sum
    if not sum_p:
        print("No sequences of four price changes were found across all buyers.")
        return

    # Find the sequence with the highest total sum of prices
    optimal_sequence, max_sum = max(sum_p.items(), key=lambda item: item[1])

    # Output the result
    print(f"The optimal sequence of four price changes is: {optimal_sequence}")
    print(f"Total bananas collected using this sequence: {max_sum}")

if __name__ == "__main__":
    main()
