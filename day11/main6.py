import sys
import os
sys.setrecursionlimit(10**7)
from collections import Counter, defaultdict

def make_step(num):
    # Rule 1: If stone is 0 -> becomes stone with number 1
    if num == 0:
        return 1, None
    # Rule 2: If the stone number has an even number of digits -> split
    elif len(str(num)) % 2 == 0:
        str_num = str(num)
        half = len(str_num) // 2
        left_part = int(str_num[:half])
        right_part = int(str_num[half:])
        return left_part, right_part
    # Rule 3: Otherwise, multiply by 2024
    else:
        return num * 2024, None

def make_step2(num):
    if num == 0:
        return [1]
    s = str(num)
    if len(s) % 2 == 0:
        half = len(s)//2
        left = int(s[:half])
        right = int(s[half:])
        return [left, right]
    else:
        return [num * 2024]

def smart_evolve(stones, blinks):
    # Convert initial list of stones to a Counter (value->count)
    counts = Counter(stones)

    for _ in range(blinks):
        new_counts = defaultdict(int)
        for stone_val, stone_count in counts.items():
            #step, new_num = make_step(stone_val)
            #result = [step, new_num]
            result = make_step2(stone_val)
            # result is a list of one or two stones
            for r in result:
                new_counts[r] += stone_count
        counts = new_counts

    # After all blinks, sum up counts
    return sum(counts.values())

def smart_evolve2(nums, k):
    """Key is to note that on a given day we have tons of stones with the 
    same number so we can group them to save tons of time and space."""
    counts = Counter(nums)
    
    for _ in range(k):
        vals = list(counts.keys())
        new_counts = defaultdict(int)
        for x in vals:
            appearances = counts[x]
            a, b = make_step(x)
            new_counts[a] += appearances
            if b is not None:
                new_counts[b] += appearances
        counts = new_counts
    
    total_stones = sum(counts.values())
    return total_stones

def main():
    directory = os.path.dirname(__file__) + '\\'
    # Example input
    input = [64554, 35, 906, 6, 6960985, 5755, 975820, 0]
    input2 = [0, 1, 10, 99, 999]
    input3 = [125, 17]

    input = input
    blinks = 75

    result = smart_evolve2(input, blinks)
    print(result)
    #print(sum(result.values()))
    #print(len(result))

if __name__ == "__main__":
    main()
