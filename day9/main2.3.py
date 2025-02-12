import os

def read_grid(file_path):
    """
    Reads the disk map from the input file and returns it as a string.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: The disk map string.
    """
    with open(file_path, 'r') as f:
        data = f.read().strip()
    return data

def iterate(data):
    """
    Converts the compact disk map into a list representation with file IDs and free spaces.

    Args:
        data (str): The compact disk map string.

    Returns:
        list: A list representing the disk blocks with file IDs and free spaces.
    """
    refactored_data = []
    index = 0  # File ID starts at 0
    for i, char in enumerate(data):
        multiplier = int(char)
        if i % 2 == 0:
            # File blocks: append file ID as string
            refactored_data.extend([str(index)] * multiplier)
            index += 1
        else:
            # Free space blocks: append '.'
            refactored_data.extend(['.'] * multiplier)
    return refactored_data

def find_files(data):
    """
    Identifies all files in the disk, returning their file IDs, start indices, and sizes.

    Args:
        data (list): The list representing disk blocks.

    Returns:
        list of tuples: Each tuple contains (file_id, start_index, size).
    """
    files = []
    current_file = None
    start_index = 0
    for i, block in enumerate(data):
        if block != '.':
            file_id = int(block)
            if current_file != file_id:
                if current_file is not None:
                    # Append the previous file if size > 0
                    size = i - start_index
                    if size > 0:
                        files.append((current_file, start_index, size))
                # Start a new file
                current_file = file_id
                start_index = i
        else:
            if current_file is not None:
                # End of the current file
                size = i - start_index
                if size > 0:
                    files.append((current_file, start_index, size))
                current_file = None
    # Handle the last file if the disk doesn't end with free space
    if current_file is not None:
        size = len(data) - start_index
        if size > 0:
            files.append((current_file, start_index, size))
    return files

def find_free_spans(data):
    """
    Identifies all free spans in the disk.

    Args:
        data (list): The list representing disk blocks.

    Returns:
        list of tuples: Each tuple contains (start_index, length).
    """
    free_spans = []
    in_free_span = False
    start_index = 0
    for i, block in enumerate(data):
        if block == '.' and not in_free_span:
            in_free_span = True
            start_index = i
        elif block != '.' and in_free_span:
            in_free_span = False
            free_spans.append((start_index, i - start_index))
    # Handle the last free span if the disk ends with free space
    if in_free_span:
        free_spans.append((start_index, len(data) - start_index))
    return free_spans

def move_files(data):
    """
    Compacts the disk by moving entire files to the leftmost suitable free spans,
    ensuring the free span is to the left of the file's current position.
    """
    # Identify all files
    files = find_files(data)
    if not files:
        return data  # No files to move

    # Sort files in decreasing order of file ID
    files_sorted = sorted(files, key=lambda x: x[0], reverse=True)

    for file_id, file_start, file_size in files_sorted:
        if file_size == 0:
            # A file with size 0 doesn't occupy blocks and doesn't need to move
            continue

        # Find all free spans on the updated disk
        free_spans = find_free_spans(data)
        # Sort free spans by start index (left to right)
        free_spans_sorted = sorted(free_spans, key=lambda x: x[0])

        # Find the first free span that can fit the file entirely to the left
        suitable_span = None
        #for span_start, span_length in free_spans_sorted:
        for span_start, span_length in free_spans:
            if span_length >= file_size and (span_start + file_size) <= file_start:
                suitable_span = (span_start, span_length)
                break

        # If no suitable span is found, the file does not move
        if suitable_span is None:
            continue

        span_start, span_length = suitable_span

        # If the file is already at the correct position (extremely unlikely under these conditions),
        # then no move needed.
        if file_start == span_start:
            continue

        # Move the file to the new position
        # 1. Write the file blocks into the new position
        for i in range(span_start, span_start + file_size):
            data[i] = str(file_id)

        # 2. Mark the old position as free space
        for i in range(file_start, file_start + file_size):
            data[i] = '.'

    return data

def checksum(data):
    """
    Calculates the filesystem checksum.

    Args:
        data (list): The compacted list representing disk blocks.

    Returns:
        int: The checksum value.
    """
    total = 0
    for position, block in enumerate(data):
        if block != '.':
            total += position * int(block)
    return total

def main():
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))

    # Replace 'input2.txt' with your actual input file name
    file_path = os.path.join(directory, 'input.txt')
    file_path = os.path.join(directory, 'input2.txt')

    # Read the disk map from the input file
    data = read_grid(file_path)
    print(f"Original Disk Map: {data}")

    # Convert the disk map into a list with file IDs and free spaces
    data_expanded = iterate(data)
    print(f"Expanded Disk Blocks: {''.join(data_expanded)}")

    # Compact the disk by moving entire files to the left
    data_compacted = move_files(data_expanded.copy())
    print(f"Compacted Disk Blocks: {''.join(data_compacted)}")

    # Calculate the filesystem checksum
    result = checksum(data_compacted)
    print(f"Filesystem Checksum: {result}")

if __name__ == "__main__":
    main()
