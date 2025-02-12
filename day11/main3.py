import os
from concurrent.futures import ThreadPoolExecutor

def make_step(num):
    if num == 0:
        return [1]
    num_str = str(num)
    if len(num_str) % 2 == 0:
        half = len(num_str)//2
        left_part = int(num_str[:half])
        right_part = int(num_str[half:])
        return [left_part, right_part]
    else:
        return [num*2024]

def process_chunk(chunk, blink_idx, chunk_idx, directory):
    # Process a list of stones and write the output to a file
    output_path = os.path.join(directory, f"chunk_{blink_idx}_{chunk_idx}.txt")
    with open(output_path, 'w') as f:
        for stone in chunk:
            transformed = make_step(stone)
            for t in transformed:
                f.write(str(t) + "\n")
    return output_path

def merge_files(file_paths, output_path):
    with open(output_path, 'w') as out:
        for fp in file_paths:
            with open(fp, 'r') as inp:
                for line in inp:
                    out.write(line)
    # Cleanup
    for fp in file_paths:
        os.remove(fp)

def step_through_threaded(stones, blinks, directory, num_threads=4, chunk_size=10000):
    input_file = os.path.join(directory, "current_stones.txt")
    # Write initial stones
    with open(input_file, 'w') as f:
        for s in stones:
            f.write(str(s) + "\n")

    for i in range(blinks):
        # Read the current stones in chunks
        # For each chunk, spawn a thread to process
        output_paths = []
        with open(input_file, 'r') as fin:
            chunk = []
            chunk_idx = 0
            futures = []
            executor = ThreadPoolExecutor(max_workers=num_threads)
            
            for line in fin:
                num = int(line.strip())
                chunk.append(num)
                if len(chunk) >= chunk_size:
                    # Process this chunk
                    c = chunk
                    chunk = []
                    futures.append(executor.submit(process_chunk, c, i, chunk_idx, directory))
                    chunk_idx += 1
            
            # Process remaining chunk
            if chunk:
                futures.append(executor.submit(process_chunk, chunk, i, chunk_idx, directory))

            executor.shutdown(wait=True)
            for future in futures:
                output_paths.append(future.result())

        # Merge all output chunks
        merged_file = os.path.join(directory, "next_stones.txt")
        merge_files(output_paths, merged_file)

        # Move merged file to current_stones.txt for next iteration
        os.remove(input_file)
        os.rename(merged_file, input_file)

        # Count stones (optional, might be expensive)
        count = 0
        with open(input_file, 'r') as f:
            for _ in f:
                count += 1
        print(f"After blink {i+1}: {count} stones")

    # Final count
    final_count = 0
    with open(input_file, 'r') as f:
        for _ in f:
            final_count += 1
    return final_count

def main():
    directory = os.path.dirname(__file__)
    stones = [64554, 35, 906, 6, 6960985, 5755, 975820, 0]
    blinks = 75
    final_count = step_through_threaded(stones, blinks, directory)
    print("Final count:", final_count)

if __name__ == "__main__":
    main()
