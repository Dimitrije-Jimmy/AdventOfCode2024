import sys
import os
sys.setrecursionlimit(10**7)

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

def step_through(stones, blinks):
    for i in range(blinks):
        new_stones = []
        for num in stones:
            step, new_num = make_step(num)
            new_stones.append(step)
            if new_num is not None:
                new_stones.append(new_num)
        stones = new_stones
        print(f"blink {i}, {len(stones)} stones")
    return stones


def main():
    directory = os.path.dirname(__file__) + '\\'
    # Example input
    input = [64554, 35, 906, 6, 6960985, 5755, 975820, 0]
    input2 = [0, 1, 10, 99, 999]
    input3 = [125, 17]

    input = input
    blinks = 75

    for number in input:
        result = step_through([number], blinks)
        print(result)
        print(len(result))
        with open(directory + 'output.txt', 'w') as f:
            f.write(str(len(result)))

if __name__ == "__main__":
    main()
