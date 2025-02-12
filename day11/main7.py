import sys
import os
sys.setrecursionlimit(10**7)

def make_step(num):
    # Rule 1: If stone is 0 -> becomes stone with number 1
    if num == 0:
        return (1, None)
    # Rule 2: If the stone number has an even number of digits -> split
    s = str(num)
    if len(s) % 2 == 0:
        half = len(s) // 2
        left_part = int(s[:half])
        right_part = int(s[half:])
        return (left_part, right_part)
    # Rule 3: Otherwise, multiply by 2024
    else:
        return (num * 2024, None)

def build_initial_counts(stones):
    """Build a dictionary {stone_value: count} from the initial list of stones."""
    counts = {}
    for st in stones:
        if st in counts:
            counts[st] += 1
        else:
            counts[st] = 1
    return counts

def smart_evolve_no_collections(stones, blinks):
    # Convert initial list of stones to a dict (value->count)
    counts = build_initial_counts(stones)

    for _ in range(blinks):
        new_counts = {}
        # Iterate over current stones and apply rules
        for stone_val, stone_count in counts.items():
            a, b = make_step(stone_val)
            
            # Add 'a' to new_counts
            if a in new_counts:
                new_counts[a] += stone_count
            else:
                new_counts[a] = stone_count
            
            # If b exists, add it as well
            if b is not None:
                if b in new_counts:
                    new_counts[b] += stone_count
                else:
                    new_counts[b] = stone_count
        
        # Move to next iteration
        counts = new_counts

    # After all blinks, sum up counts
    total_stones = 0
    for c in counts.values():
        total_stones += c
    return total_stones

def main():
    directory = os.path.dirname(__file__) + '\\'
    # Example input
    input_stones = [64554, 35, 906, 6, 6960985, 5755, 975820, 0]
    blinks = 75

    result = smart_evolve_no_collections(input_stones, blinks)
    print(result)

if __name__ == "__main__":
    main()
