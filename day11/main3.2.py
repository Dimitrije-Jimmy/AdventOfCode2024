import os
import sys
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

sys.setrecursionlimit(10**7)

def make_step(num):
    # Rule 1: If stone is 0 -> becomes stone with number 1
    if num == 0:
        return [1]
    s = str(num)
    # Rule 2: If even number of digits -> split
    if len(s) % 2 == 0:
        half = len(s) // 2
        left_part = int(s[:half])
        right_part = int(s[half:])
        return [left_part, right_part]
    # Rule 3: Otherwise multiply by 2024
    else:
        return [num * 2024]

def process_chunk(chunk, blink_idx, chunk_idx, directory):
    """Process a single chunk of stones and write to a separate file."""
    output_path = os.path.join(directory, f"chunk_{blink_idx}_{chunk_idx}.txt")
    with open(output_path, 'w') as f:
        for stone in chunk:
            transformed = make_step(stone)
            for t in transformed:
                f.write(str(t) + "\n")
    return output_path

def worker_thread(queue, blink_idx, directory):
    """Worker thread function: take tasks from the queue and process them."""
    while True:
        item = queue.get()
        if item is None:
            # No more tasks
            queue.task_done()
            break
        (chunk, chunk_idx) = item
        output_file = process_chunk(chunk, blink_idx, chunk_idx, directory)
        queue.task_done()

def merge_files(file_paths, output_path):
    """Merge multiple chunk files into a single file."""
    with open(output_path, 'w') as out:
        for fp in file_paths:
            with open(fp, 'r') as inp:
                for line in inp:
                    out.write(line)
    # Cleanup chunk files
    for fp in file_paths:
        os.remove(fp)

def step_through_threaded(stones, blinks, directory, num_threads=4, chunk_size=10000):
    input_file = os.path.join(directory, "current_stones.txt")
    # Write initial stones to input file
    with open(input_file, 'w') as f:
        for s in stones:
            f.write(str(s) + "\n")

    for i in range(blinks):
        output_paths = []
        # We'll read the current_stones.txt and create chunks
        with open(input_file, 'r') as fin:
            chunks_queue = Queue()
            # Start worker threads
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                for _ in range(num_threads):
                    executor.submit(worker_thread, chunks_queue, i, directory)
                
                chunk = []
                chunk_idx = 0
                for line in fin:
                    num = int(line.strip())
                    chunk.append(num)
                    if len(chunk) >= chunk_size:
                        chunks_queue.put((chunk, chunk_idx))
                        chunk = []
                        chunk_idx += 1
                        
                # If there's a leftover chunk
                if chunk:
                    chunks_queue.put((chunk, chunk_idx))

                # Signal no more tasks
                for _ in range(num_threads):
                    chunks_queue.put(None)

                # Wait for all tasks to complete
                chunks_queue.join()

            # Now all chunks processed, collect chunk files
            # The chunk files are named chunk_{blink_idx}_{chunk_idx}.txt
            # We can list them by checking the directory
            for fname in os.listdir(directory):
                if fname.startswith(f"chunk_{i}_") and fname.endswith(".txt"):
                    output_paths.append(os.path.join(directory, fname))

        # Merge all output chunks
        merged_file = os.path.join(directory, "next_stones.txt")
        merge_files(output_paths, merged_file)

        # Replace old file with merged file
        os.remove(input_file)
        os.rename(merged_file, input_file)

        # Count stones
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
    blinks = 75  # For demonstration; adjust as needed
    final_count = step_through_threaded(stones, blinks, directory)
    print("Final count:", final_count)

if __name__ == "__main__":
    main()
