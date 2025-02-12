import itertools
from time import perf_counter


def evaluate_equation(nums: list[int], ops: tuple[str, ...]) -> int:
    """
    Evaluate an equation using the given numbers and operators, left to right.
    """
    res = nums[0]
    current = 1
    for op in ops:
        if op == "+":
            res += nums[current]
        elif op == "*":
            res *= nums[current]
        else:
            res = int(str(res) + str(nums[current]))
        current += 1
    return res


def parse_input(file_path: str) -> list[tuple[int, list[int]]]:
    """
    Parse the input file into a list of equations.
    
    Args:
        file_path (str): Path to the input file.

    Returns:
        list: A list of tuples where the first element is the target result
              and the second element is a list of numbers.
    """
    with open(file_path, "r") as file:
        equations = [
            (int(line.split(":")[0]), [int(num) for num in line.split(":")[1].split()])
            for line in file if line.strip()
        ]
    return equations


def solve_equations(equations: list[tuple[int, list[int]]], operators: tuple[str, ...]) -> int:
    """
    Solve equations by evaluating all combinations of given operators.

    Args:
        equations (list): List of equations as tuples (target_result, numbers).
        operators (tuple): Tuple of operators to use for evaluation.

    Returns:
        int: The sum of all valid target results.
    """
    total = 0
    for target_result, numbers in equations:
        possibilities = itertools.product(operators, repeat=len(numbers) - 1)
        for p in possibilities:
            if target_result == evaluate_equation(numbers, p):
                total += target_result
                break
    return total


def main():
    import os
    # Determine the directory of the current script
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join(directory, 'input.txt')  # Ensure your input file is named 'input.txt' and located in the same directory as this script
    #file_path = os.path.join(directory, 'input2.txt')
    equations = parse_input(file_path)

    # Part One
    p1_start = perf_counter()
    part_one_result = solve_equations(equations, operators=("+", "*"))
    p1_end = perf_counter()

    # Part Two (Including || as concatenation)
    p2_start = perf_counter()
    part_two_result = solve_equations(equations, operators=("+", "*", "||"))
    p2_end = perf_counter()

    # Results and Timing
    print(f"Part One: {part_one_result}")
    print(f"Elapsed Time (Part One): {p1_end - p1_start:0.2f}s")

    print(f"Part Two: {part_two_result}")
    print(f"Elapsed Time (Part Two): {p2_end - p2_start:0.2f}s")


if __name__ == "__main__":
    main()
