import os
from collections import defaultdict

def read_input(file_path):
    """Reads the input file contents."""
    with open(file_path, 'r') as f:
        #raw_lines = [line.rstrip('\n') for line in f
        raw_lines = [line.strip('\n') for line in f if line.strip()]
    
    return raw_lines
    
def parse_lock(lines):
    """
    Given 7 lines (each 5 characters wide) for a lock,
    return an array of 5 pin heights.
    We skip row0 (the very top, always #####) and row6 (the very bottom, always .....),
    then count consecutive '#' down from row1 to row5 in each column.
    """
    heights = [0]*5
    for col in range(5):
        h = 0
        # Check rows 1..5 downward
        for row in range(1, 6):  # row1 to row5
            if lines[row][col] == '#':
                h += 1
            else:
                break
        heights[col] = h
    return heights

def parse_key(lines):
    """
    Given 7 lines (each 5 characters wide) for a key,
    return an array of 5 key heights.
    We skip row6 (the very bottom, always #####) and row0 (the very top, always .....),
    then count consecutive '#' up from row5 to row1 in each column.
    """
    heights = [0]*5
    for col in range(5):
        h = 0
        # Check rows 5..1 upward
        for row in range(5, 0, -1):  # row5 down to row1
            if lines[row][col] == '#':
                h += 1
            else:
                break
        heights[col] = h
    return heights

def read_schematics_and_convert(filename):
    """
    Reads the entire puzzle input from a file (or you could adapt to read stdin).
    Splits the input into 7-line chunks.  Determines whether each chunk is a lock
    or a key, parses, and returns two lists: locks, keys.
    """

    raw_lines = read_input(filename)
    #print(raw_lines)
    
    # Each schematic = 7 lines; assume the total line count is multiple of 7
    locks = []
    keys = []
    for i in range(0, len(raw_lines), 7):
        block = raw_lines[i:i+7]
        # Identify if this block is a lock or a key
        # Lock: top row all '#' and bottom row all '.'
        # Key:  top row all '.' and bottom row all '#'
        top_row = block[0]
        bottom_row = block[-1]
        
        if top_row == '#####' and bottom_row == '.....':
            # It's a lock
            locks.append(parse_lock(block))
        elif top_row == '.....' and bottom_row == '#####':
            # It's a key
            keys.append(parse_key(block))
        else:
            # If the puzzle statement is guaranteed correct, we shouldn't get here
            raise ValueError("Unrecognized schematic:\n" + "\n".join(block))
    
    return locks, keys

def count_fitting_pairs(locks, keys):
    """
    Given lists of 5-element arrays (locks and keys),
    count how many (lock, key) pairs fit with no overlap.
    A pair fits if for each column i, lock[i] + key[i] <= 5.
    """
    count = 0
    for lock in locks:
        for key in keys:
            # Check column by column
            if all(lock[i] + key[i] <= 5 for i in range(5)):
                count += 1
    return count

def main():
    directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')

    # Read data
    locks, keys = read_schematics_and_convert(file_path)
    
    # Count how many pairs
    answer = count_fitting_pairs(locks, keys)
    print("Number of unique lock/key pairs that fit:", answer)

if __name__ == "__main__":
    main()
