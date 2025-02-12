import numpy as np
import os

def read_grid(file_path):
    """
    Reads the grid from the input file and returns it as a list of strings.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list: A list of strings, where each string represents a row of the grid.
    """
    with open(file_path, 'r') as f:
        #grid = [line.strip() for line in f if line.strip()]
        data = f.read()
        print(type(data))
    return data


def iterate(data):
    refactored_data = ''
    index = 0
    for i in range(len(data)):
        multiplier = int(data[i])
        if i % 2 == 0:
            #for j in range(int(data[i])):
            #    refactored_data += j
            refactored_data += str(index) * multiplier
            index += 1
        else:
           refactored_data += '.' * multiplier 
    
    return refactored_data

def move(data):
    new_data = ''
    for i in range(len(data)):
        if data[i] == '.':
            new_data += data[i]
            #data.replace('.', )
        elif data[i] != '.':
            new_data += data[-1]
            data.remove(-1)
    return new_data



def checksum(data):
    total = 0
    for i in range(len(data)):
        total += i*data[i]
    return total

def main():
    import os
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(directory, 'input.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    file_path = os.path.join(directory, 'input2.txt')

    #with open(file_path, "r") as file:
    #    data = file.read()
    data = read_grid(file_path)
    print(data)
    data2 = iterate(data)
    print(data2)
    data3 = move(data2)
    print(data3)

    #result = function_for_part1(data)
    #print(f"Result part 1: {result}")


# Example usage with your input
if __name__ == "__main__":
    main()
