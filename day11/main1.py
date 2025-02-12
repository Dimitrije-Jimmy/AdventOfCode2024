import numpy as np
import os


def make_step(num):
    if num == 0:
        return 1, None
    elif len(str(num)) % 2 == 0:
        str_num = str(num)
        half = len(str_num) // 2
        return int(str_num[:half]), int(str_num[half:])
    else:
        return num*2024, None


def step_through(input, blinks):
    for _ in range(blinks):
        new_sez = input.copy()
        for i, num in enumerate(input):
            step, new_num = make_step(num)
            print(step, new_num)
            new_sez[i] = step
            if new_num is not None:
                new_sez[:i] + [new_num] + new_sez[i:]
                #new_sez.append(new_num)
    
    return new_sez

def main():
    directory = os.path.dirname(__file__)+'\\'
    
    input = [64554, 35, 906, 6, 6960985, 5755, 975820, 0]
    input2 = [0, 1, 10, 99, 999]
    input3 = [125, 17]

    input = input3

    blinks = 6

    output = step_through(input, blinks)   

    print(output)
    print(len(output))



if __name__ == "__main__":
    main()