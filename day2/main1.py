import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)

import numpy as np

def read_reports(file_path):
    """
    Reads reports from a file into a NumPy array.
    Each line in the file represents a report.
    """
    # Load data into a 2D NumPy array
    data = np.loadtxt(file_path, dtype=int)
    return data

# Load data
data = read_reports(file_path)


#data = [[7, 6, 4, 2, 1],
#        [1, 2, 7, 8, 9],
#        [9, 7, 6, 2, 1],
#        [1, 3, 2, 4, 5],
#        [8, 6, 4, 4, 1],
#        [1, 3, 6, 7, 9]]
#data = np.array(data)

def compute_differences(data):
    """
    Computes the differences between adjacent levels for each report.
    """
    # Calculate differences along each report (row-wise)
    diffs = np.diff(data, axis=1)
    return diffs


def check_direction(diffs):
    """
    Checks if the levels in each report are all increasing or all decreasing.
    Returns a boolean array where True indicates a consistent direction.
    """
    is_increasing = np.all(diffs > 0, axis=1)
    is_decreasing = np.all(diffs < 0, axis=1)
    valid_direction = is_increasing | is_decreasing
    return valid_direction, is_increasing, is_decreasing


def validate_differences(diffs):
    """
    Checks if the absolute differences are between 1 and 3 (inclusive).
    Returns a boolean array where True indicates all differences are valid.
    """
    diffs_abs = np.abs(diffs)
    valid_diffs = np.all((diffs_abs >= 1) & (diffs_abs <= 3), axis=1)
    return valid_diffs

def determine_safe_reports(data):
    """
    Determines which reports are safe based on the given conditions.
    Returns the indices of safe reports.
    """
    diffs = compute_differences(data)
    valid_direction, _, _ = check_direction(diffs)
    valid_diffs = validate_differences(diffs)
    safe_reports_mask = valid_direction & valid_diffs
    return safe_reports_mask

safe_reports_mask = determine_safe_reports(data)
safe_reports = data[safe_reports_mask]
unsafe_reports = data[~safe_reports_mask]

print(f"Number of safe reports: {safe_reports.shape[0]}")
print(f"Number of unsafe reports: {unsafe_reports.shape[0]}")

def main():
    file_path = directory+'input.txt'  # Replace with your input file path
    data = read_reports(file_path)
    safe_reports_mask = determine_safe_reports(data)
    safe_reports = data[safe_reports_mask]
    unsafe_reports = data[~safe_reports_mask]

    print(f"Number of safe reports: {safe_reports.shape[0]}")
    print(f"Number of unsafe reports: {unsafe_reports.shape[0]}")

    # Optionally, print safe reports
    for i, report in enumerate(safe_reports, start=1):
        print(f"Safe Report {i}: {' '.join(map(str, report))}")


if __name__ == "__main__":
    #main()
    print("Done")