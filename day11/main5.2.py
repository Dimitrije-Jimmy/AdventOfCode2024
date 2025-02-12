import sys
import os
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sys.setrecursionlimit(10**7)

def make_step(num):
    if num == 0:
        return 1, None
    elif len(str(num)) % 2 == 0:
        s = str(num)
        half = len(s)//2
        left_part = int(s[:half])
        right_part = int(s[half:])
        return left_part, right_part
    else:
        return num * 2024, None

def step_through(stones, blinks, directory):
    data_file = os.path.join(directory, 'growth_data.txt')
    with open(data_file, 'w') as f:
        f.write("blink,length\n")  # header
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

def read_data(directory):
    data_file = os.path.join(directory, 'growth_data.txt')
    blink_nums = []
    lengths = []
    with open(data_file, 'r') as f:
        f.readline() # skip header
        for line in f:
            if line.strip():
                b,l = line.strip().split(',')
                blink_nums.append(int(b))
                lengths.append(int(l))
    return blink_nums, lengths

def quadratic_model(b, p0, p1, p2):
    # p0 + p1*b + p2*b^2 = ln(length)
    return p0 + p1*b + p2*(b**2)

def fit_quadratic_in_log(blink_nums, lengths):
    ln_lengths = [math.log(L) for L in lengths]
    # Initial guesses for p0, p1, p2
    p0 = math.log(lengths[0])
    p1 = 0.1
    p2 = 0.001
    popt, pcov = curve_fit(quadratic_model, blink_nums, ln_lengths, p0=[p0,p1,p2])
    return popt

def estimate_length(b, p0, p1, p2):
    ln_est = p0 + p1*b + p2*b*b
    return math.exp(ln_est)

def plot_data_and_fit(blink_nums, lengths, p0, p1, p2):
    plt.figure(figsize=(10,6))
    plt.scatter(blink_nums, lengths, color='blue', label='Data Points')

    fit_blinks = range(1, max(blink_nums)+1)
    fit_values = [estimate_length(b, p0, p1, p2) for b in fit_blinks]

    plt.plot(fit_blinks, fit_values, color='red', label='Quadratic Log-Fit')
    plt.xlabel('Blink Number')
    plt.ylabel('Number of Stones')
    plt.title('Stone Count Growth: Data vs. Quadratic Log-Fit')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')  # log scale to better see exponential growth
    plt.show()

def main():
    directory = os.path.dirname(__file__)
    stones = [64554, 35, 906, 6, 6960985, 5755, 975820, 0]

    blinks_for_data = 42
    # Run simulation for 35 blinks and save data
    step_through(stones, blinks_for_data, directory)

    blink_nums, lengths = read_data(directory)
    # Fit a quadratic model to ln(length)
    p0, p1, p2 = fit_quadratic_in_log(blink_nums, lengths)
    print("Fitted parameters for ln(length) = p0 + p1*b + p2*b^2:")
    print(f"p0 = {p0}, p1 = {p1}, p2 = {p2}")

    # Plot the data and the fit
    plot_data_and_fit(blink_nums, lengths, p0, p1, p2)

    # Estimate for 75 blinks using the quadratic model
    estimated_75 = estimate_length(75, p0, p1, p2)
    print(f"Estimated count for 75 blinks (quadratic model): {estimated_75}")

if __name__ == "__main__":
    main()

# 167643797620648.12     <-- exponential in log 35 blinks

# 177203674740267.56     <-- exponential in log 35 blinks



# cubic model: 34089507951331.18 stones in 40 blinks
# HERE IN THE MIDDLE!!!!!
# 382923257720065.3     <-- quadratic in log 40 blinks

# 525011662850739.8     <-- quadratic in log 35 blinks
