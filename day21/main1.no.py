import time
from collections import deque, defaultdict

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read().splitlines()

def find_key(key, pad):
    for y, row in enumerate(pad):
        for x, char in enumerate(row):
            if char == key:
                return x, y
    return -1, -1

def get_moves(keys, keypad):
    keypad_moves = {}

    for i, c1 in enumerate(keys):
        x1, y1 = find_key(c1, keypad)
        for j, c2 in enumerate(keys):
            x2, y2 = find_key(c2, keypad)

            # Perform BFS to find the shortest path
            queue = deque([(x1, y1, 0, "")])
            visited = set()
            options = set()

            while queue:
                cx, cy, cost, path = queue.popleft()

                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))

                if (cx, cy) == (x2, y2):
                    options.add(path)
                    continue

                for dx, dy, direction in [
                    (1, 0, '>'), (-1, 0, '<'), (0, 1, 'v'), (0, -1, '^')
                ]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < len(keypad[0]) and 0 <= ny < len(keypad) and keypad[ny][nx] != ' ':
                        queue.append((nx, ny, cost + 1, path + direction))

            keypad_moves[(c1, c2)] = list(options)

    return keypad_moves

def get_sequences(entry_code, keypad_moves):
    sequences = [""]
    prev_key = 'A'

    for key in entry_code:
        new_sequences = []
        moves = keypad_moves.get((prev_key, key), [])

        for seq in sequences:
            for move in moves:
                new_sequences.append(seq + move + 'A')

        sequences = new_sequences
        prev_key = key

    return sequences

def shortest_moves(current, level, stop_at_level, result_cache, all_moves):
    if current == "":
        return 0

    if (level, current) in result_cache:
        return result_cache[(level, current)]

    if level == stop_at_level:
        result = min(len(seq) for seq in get_sequences(current, all_moves))
        result_cache[(level, current)] = result
        return result

    first_a = current.find('A')
    first_part = current[:first_a + 1]
    second_part = current[first_a + 1:]

    shortest = float('inf')

    possibilities = get_sequences(first_part, all_moves)
    for seq in possibilities:
        count = shortest_moves(seq, level + 1, stop_at_level, result_cache, all_moves)
        shortest = min(shortest, count)

    if second_part:
        shortest += shortest_moves(second_part, level, stop_at_level, result_cache, all_moves)

    result_cache[(level, current)] = shortest
    return shortest

def run(filepath, is_test):
    start_time = time.time()
    supposed_answer1 = 126384
    supposed_answer2 = 154115708116294

    lines = read_file(filepath)
    answer1 = 0
    answer2 = 0

    num_keypad = ["789", "456", "123", " 0A"]
    dir_keypad = [" ^A", "<v>"]
    num_keys = "0123456789A"
    dir_keys = "<^>vA"

    num_keypad_moves = get_moves(num_keys, num_keypad)
    dir_keypad_moves = get_moves(dir_keys, dir_keypad)
    all_moves = {**num_keypad_moves, **dir_keypad_moves}

    result_cache1 = {}
    result_cache2 = {}

    for line in lines:
        num_part = int(line[:3])
        entry_code = line[3:]

        la1 = shortest_moves(entry_code, 0, 2, result_cache1, all_moves)
        answer1 += la1 * num_part

        la2 = shortest_moves(entry_code, 0, 25, result_cache2, all_moves)
        answer2 += la2 * num_part

    print(f"Answer 1: {answer1} (Expected: {supposed_answer1}, Test: {is_test})")
    print(f"Answer 2: {answer2} (Expected: {supposed_answer2}, Test: {is_test})")
    print(f"Duration: {time.time() - start_time:.2f} seconds")

# Example usage
run("C:\\Programming\\Personal Projects\\AdventOfCode2024\\day21\\input2.txt", True)
#run("C:\\Programming\\Personal Projects\\AdventOfCode2024\\day21\\input2.txt", False)
