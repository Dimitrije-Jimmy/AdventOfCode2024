import os
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define models
def exp_model(b, p0, p1):
    # ln(length) = p0 + p1*b
    # length = exp(p0 + p1*b)
    return math.e**(p0 + p1*b)

def quadratic_model(b, p0, p1, p2):
    # ln(length) = p0 + p1*b + p_2*b^2
    # length = exp(p0 + p1*b + p2*b^2)
    return math.e**(p0 + p1*b + p2*(b**2))

def cubic_model(b, p0, p1, p2, p3):
    # ln(length) = p0 + p1*b + p2*b^2 + p3*b^3
    return math.e**(p0 + p1*b + p2*(b**2) + p3*(b**3))

# We'll fit the models to ln(length) directly using curve_fit by passing transformed data
def fit_model(blink_nums, lengths, model_type='exp'):
    # Convert to log for fitting
    ln_lengths = [math.log(l) for l in lengths]

    if model_type == 'exp':
        # ln(L) = p0 + p1*b
        # initial guess
        p0_guess = math.log(lengths[0])
        p1_guess = 0.1
        def func(b, p0, p1):
            return p0 + p1*b
        popt, pcov = curve_fit(func, blink_nums, ln_lengths, p0=[p0_guess, p1_guess])
        # popt are the parameters for ln(L) = p0 + p1*b
        # Return a lambda that computes length from b
        return lambda b: math.e**(popt[0] + popt[1]*b), popt

    elif model_type == 'quad':
        # ln(L) = p0 + p1*b + p2*b^2
        p0_guess = math.log(lengths[0])
        p1_guess = 0.1
        p2_guess = 0.001
        def func(b, p0, p1, p2):
            return p0 + p1*b + p2*(b**2)
        popt, pcov = curve_fit(func, blink_nums, ln_lengths, p0=[p0_guess, p1_guess, p2_guess])
        return lambda b: math.e**(popt[0] + popt[1]*b + popt[2]*b*b), popt

    elif model_type == 'cubic':
        # ln(L) = p0 + p1*b + p2*b^2 + p3*b^3
        p0_guess = math.log(lengths[0])
        p1_guess = 0.1
        p2_guess = 0.001
        p3_guess = 0.00001
        def func(b, p0, p1, p2, p3):
            return p0 + p1*b + p2*b*b + p3*b*b*b
        popt, pcov = curve_fit(func, blink_nums, ln_lengths, p0=[p0_guess, p1_guess, p2_guess, p3_guess])
        return lambda b: math.e**(popt[0] + popt[1]*b + popt[2]*b*b + popt[3]*b*b*b), popt

def main():
    directory = os.path.dirname(__file__)
    data_file = os.path.join(directory, 'growth_data.txt')
    if not os.path.exists(data_file):
        print("growth_data.txt not found. Please run your simulation first.")
        return

    # Read data
    blink_nums = []
    lengths = []
    with open(data_file, 'r') as f:
        header = f.readline() # skip header
        for line in f:
            line=line.strip()
            if line:
                b,l = line.split(',')
                b = int(b)
                l = int(l)
                blink_nums.append(b)
                lengths.append(l)

    # Fit different models
    models = ['exp', 'quad', 'cubic']
    fitted_functions = {}
    parameters = {}
    for m in models:
        func, popt = fit_model(blink_nums, lengths, model_type=m)
        fitted_functions[m] = func
        parameters[m] = popt

    # Predict for 75 blinks
    blink_to_predict = 75
    predictions = {}
    for m in models:
        predictions[m] = fitted_functions[m](blink_to_predict)

    # Print predictions
    print("Predictions for 75 blinks:")
    for m in models:
        print(f"{m} model: {predictions[m]} stones")

    # Plot data and all fits
    plt.figure(figsize=(10,6))
    # Plot raw data
    plt.scatter(blink_nums, lengths, color='black', label='Data Points')

    # Create a range for plotting fits
    max_blink = max(blink_nums)
    extended_blinks = range(1, max_blink+1)  # plot only up to last blink we have data for

    colors = {'exp':'red', 'quad':'green', 'cubic':'blue'}
    for m in models:
        fit_vals = [fitted_functions[m](b) for b in extended_blinks]
        plt.plot(extended_blinks, fit_vals, color=colors[m], label=f'{m} fit')

    plt.xlabel('Blink Number')
    plt.ylabel('Number of Stones')
    plt.title('Stone Count Growth: Data vs. Multiple Models')
    plt.yscale('log')  # log scale to visualize growth
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()



# 167643797620648.12     <-- exponential in log 35 blinks

# 177203674740267.56     <-- exponential in log 35 blinks



# cubic model: 34089507951331.18 stones in 40 blinks
# HERE IN THE MIDDLE!!!!!
# quad model: 349127113450407.44 stones
#this one is close cause no hint for up or down 

# 382923257720065.3     <-- quadratic in log 40 blinks
# quad model: 349127113450407.44 stones
# cubic model: 48054389090008.31 stones
# 525011662850739.8     <-- quadratic in log 35 blinks