import sys
import os
import math
import matplotlib.pyplot as plt

sys.setrecursionlimit(10**7)

def make_step(num):
    # Rule 1: If stone is 0 -> becomes stone with number 1
    if num == 0:
        return 1, None
    # Rule 2: If the stone number has an even number of digits -> split
    elif len(str(num)) % 2 == 0:
        str_num = str(num)
        half = len(str_num) // 2
        left_part = int(str_num[:half])
        right_part = int(str_num[half:])
        return left_part, right_part
    # Rule 3: Otherwise, multiply by 2024
    else:
        return num * 2024, None

def step_through(stones, blinks, directory):
    data_file = os.path.join(directory, 'growth_data.txt')
    with open(data_file, 'w') as f:
        f.write("blink,length\n")  # Header

        for b in range(blinks):
            new_stones = []
            for num in stones:
                step, new_num = make_step(num)
                new_stones.append(step)
                if new_num is not None:
                    new_stones.append(new_num)
            stones = new_stones
            f.write(f"{b+1},{len(stones)}\n")

    return stones

def fit_exponential_curve(directory):
    # Read the collected data
    data_file = os.path.join(directory, 'growth_data.txt')
    blink_nums = []
    lengths = []
    with open(data_file, 'r') as f:
        header = f.readline()  # skip header
        for line in f:
            line = line.strip()
            if not line:
                continue
            b, l = line.split(',')
            b = int(b)
            l = int(l)
            blink_nums.append(b)
            lengths.append(l)

    # We want to fit ln(length) = ln(A) + b*ln(r)
    ln_lengths = [math.log(x) for x in lengths]

    n = len(blink_nums)
    sum_b = sum(blink_nums)
    sum_lnL = sum(ln_lengths)
    sum_blnL = sum(b * lnL for b, lnL in zip(blink_nums, ln_lengths))
    sum_b2 = sum(b*b for b in blink_nums)

    numerator = sum_blnL - (sum_b * sum_lnL / n)
    denominator = sum_b2 - (sum_b * sum_b / n)
    slope = numerator / denominator
    intercept = (sum_lnL / n) - slope * (sum_b / n)

    A = math.exp(intercept)
    r = math.exp(slope)

    return A, r, blink_nums, lengths

def estimate_for_blink(blink_number, A, r):
    return A * (r ** blink_number)

def plot_data_and_fit(blink_nums, lengths, A, r):
    # Plot the actual data points
    plt.figure(figsize=(10,6))
    plt.scatter(blink_nums, lengths, color='blue', label='Data Points')

    # Plot the fitted curve
    # We'll generate some smooth blink values for plotting
    max_blink = max(blink_nums)
    fit_blinks = range(1, max_blink+1)
    fit_values = [estimate_for_blink(b, A, r) for b in fit_blinks]

    plt.plot(fit_blinks, fit_values, color='red', label='Fitted Exponential Curve')

    plt.xlabel('Blink Number')
    plt.ylabel('Number of Stones')
    plt.title('Stone Count Growth: Data vs. Exponential Fit')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')  # optional: use log scale to visualize exponential growth better
    plt.show()

def main():
    directory = os.path.dirname(__file__)
    # Given input
    stones = [64554, 35, 906, 6, 6960985, 5755, 975820, 0]
    blinks_for_data = 40

    # Run simulation for 35 blinks and record data
    step_through(stones, blinks_for_data, directory)

    # Fit exponential curve to the data
    A, r, blink_nums, lengths = fit_exponential_curve(directory)
    print("Fitted exponential parameters:")
    print(f"A = {A}, r = {r}")

    # Plot the results
    plot_data_and_fit(blink_nums, lengths, A, r)

    # Estimate count for 75 blinks
    estimated_75 = estimate_for_blink(75, A, r)
    print(f"Estimated count for 75 blinks: {estimated_75}")

if __name__ == "__main__":
    main()
