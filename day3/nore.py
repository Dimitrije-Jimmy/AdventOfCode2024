import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)

def calculate_mul_sum_without_regex(input_string):
    total_sum = 0
    is_enabled = True
    i = 0
    length = len(input_string)
    
    while i < length:
        # Check for 'do()'
        if input_string[i:i+4] == 'do()':
            is_enabled = True
            print("do() encountered: mul instructions enabled")
            i += 4
        # Check for "don't()"
        elif input_string[i:i+7] == "don't()":
            is_enabled = False
            print("don't() encountered: mul instructions disabled")
            i += 7
        # Check for 'mul('
        elif input_string[i:i+4] == 'mul(':
            i += 4  # Move past 'mul('
            # Extract first number
            num1 = ''
            while i < length and input_string[i].isdigit():
                num1 += input_string[i]
                i += 1
            # Check for ','
            if i < length and input_string[i] == ',':
                i += 1  # Move past ','
            else:
                continue  # Invalid format, skip
            # Extract second number
            num2 = ''
            while i < length and input_string[i].isdigit():
                num2 += input_string[i]
                i += 1
            # Check for ')'
            if i < length and input_string[i] == ')':
                i += 1  # Move past ')'
            else:
                continue  # Invalid format, skip
            # Process the mul instruction
            if num1 and num2:
                x = int(num1)
                y = int(num2)
                product = x * y
                if is_enabled:
                    total_sum += product
                    print(f"mul({x},{y}) = {product} (Enabled)")
                else:
                    print(f"mul({x},{y}) = {product} (Disabled)")
        else:
            i += 1  # Move to the next character
    
    print(f"\nTotal Sum: {total_sum}")
    return total_sum

# Example usage
input_string = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
with open(file_path, 'r') as file:
    input_string = file.read()
calculate_mul_sum_without_regex(input_string)
