def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    rules = []
    updates = []
    is_update_section = False

    for line in lines:
        line = line.strip()
        if line == '':
            is_update_section = True
            continue
        if not is_update_section:
            # Parse rules
            if '|' in line:
                x, y = line.split('|')
                rules.append((int(x), int(y)))
        else:
            # Parse updates
            update = [int(num.strip()) for num in line.split(',') if num.strip()]
            updates.append(update)

    return rules, updates

def check_update_order(update, rules):
    page_positions = {page: idx for idx, page in enumerate(update)}
    applicable_rules = []
    for x, y in rules:
        if x in page_positions and y in page_positions:
            applicable_rules.append((x, y))
            if page_positions[x] >= page_positions[y]:
                return False  # Rule violated
    return True  # All applicable rules are satisfied

def get_middle_page_number(update):
    middle_index = len(update) // 2
    return update[middle_index]

from collections import defaultdict, deque

def order_correctly(update, rules):
    import pprint as pp
    pp.pprint(update)

    # Build the graph
    page_set = set(update)
    applicable_rules = []
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Initialize in-degree for all pages in the update
    for page in update:
        in_degree[page] = 0
    
    # Build edges and update in-degree counts
    for x, y in rules:
        if x in page_set and y in page_set:
            graph[x].append(y)
            in_degree[y] += 1
    
    # Perform topological sort using Kahn's algorithm
    queue = deque([page for page in update if in_degree[page] == 0])
    sorted_pages = []
    visited_pages = set()
    
    pp.pprint(graph)
    pp.pprint(in_degree)
    while queue:
        current_page = queue.popleft()
        sorted_pages.append(current_page)
        visited_pages.add(current_page)
        for neighbor in graph[current_page]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0 and neighbor not in visited_pages:
                queue.append(neighbor)
    
    # Check if all pages are included
    if len(sorted_pages) != len(page_set):
        # There is a cycle; ordering not possible
        raise ValueError("Cycle detected; cannot reorder pages without violating rules.")
    
    # Return the sorted pages in the order they appear in the update
    # This ensures that we maintain the relative order where possible
    pp.pprint(sorted_pages)
    return sorted_pages


def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    print(file_path)

    file_path = directory+'input.txt'  # Replace with your input file path
    file_path = directory+'input2.txt'  # Replace with your input file path
    rules, updates = parse_input(file_path)
    incorrectly_ordered_updates = []
    corrected_updates = []
    middle_page_numbers = []
    
    for update in updates:
        if not check_update_order(update, rules):
            # Update is incorrectly ordered; reorder it
            try:
                corrected_update = order_correctly(update, rules)
                corrected_updates.append(corrected_update)
                middle_page_numbers.append(get_middle_page_number(corrected_update))
            except ValueError as e:
                print(f"Cannot reorder update {update}: {e}")
        else:
            continue  # We only consider incorrectly ordered updates for part two
    
    total = sum(middle_page_numbers)
    print(f"Sum of middle page numbers after correcting updates: {total}")

    # For debugging purposes, you can print the correctly ordered updates and their middle page numbers
    # print("Correctly Ordered Updates and their Middle Page Numbers:")
    # for update, middle_page in zip(correctly_ordered_updates, middle_page_numbers):
    #     print(f"Update: {update}, Middle Page: {middle_page}")

if __name__ == "__main__":
    main()
