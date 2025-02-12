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

def order_correctly(update, rules):
    page_positions = {page: idx for idx, page in enumerate(update)}
    applicable_rules = []
    for x, y in rules:
        if x in page_positions and y in page_positions:
            applicable_rules.append((x, y))
            #i = page_positions[x]
            #j = page_positions[y]
            if page_positions[x] >= page_positions[y]:
                # Rule violated
                page_positions[x], page_positions[y] = page_positions[y], page_positions[x]
    
    correct_update = [update[i] for i in sorted(page_positions.values())]
    return correct_update

def main():
    import os

    directory = os.path.dirname(__file__)+'\\'
    file_path = directory+'input.txt'
    print(file_path)

    file_path = directory+'input.txt'  # Replace with your input file path
    #file_path = directory+'input2.txt'  # Replace with your input file path
    rules, updates = parse_input(file_path)
    correctly_ordered_updates = []
    incorrectly_ordered_updates = []
    middle_page_numbers = []
    middle_page_numbers_incorrectly_ordered = []

    for update in updates:
        if check_update_order(update, rules):
            correctly_ordered_updates.append(update)
            middle_page_numbers.append(get_middle_page_number(update))
        else:
            incorrectly_ordered_updates.append(update)
            update2 = get_middle_page_number(update)
            middle_page_numbers_incorrectly_ordered.append(get_middle_page_number(update2))

    total = sum(middle_page_numbers)
    print(f"Sum of middle page numbers from correctly ordered updates: {total}")

    total_incorrectly_ordered_correctly_ordered = sum(middle_page_numbers_incorrectly_ordered)
    print(f"Sum of middle page numbers from correctly ordered updates: {total_incorrectly_ordered_correctly_ordered}")

    # For debugging purposes, you can print the correctly ordered updates and their middle page numbers
    # print("Correctly Ordered Updates and their Middle Page Numbers:")
    # for update, middle_page in zip(correctly_ordered_updates, middle_page_numbers):
    #     print(f"Update: {update}, Middle Page: {middle_page}")

if __name__ == "__main__":
    main()
