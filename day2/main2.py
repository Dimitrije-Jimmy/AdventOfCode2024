import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)

def read_reports_variable_length(file_path):
    reports = []
    with open(file_path, 'r') as file:
        for line in file:
            levels = np.array(list(map(int, line.strip().split())))
            reports.append(levels)
    return reports

def determine_safe_reports_variable_length(reports):
    safe_reports = []
    unsafe_reports = []
    for report in reports:
        diffs = np.diff(report)
        is_increasing = np.all(diffs > 0)
        is_decreasing = np.all(diffs < 0)
        valid_direction = is_increasing or is_decreasing
        diffs_abs = np.abs(diffs)
        valid_diffs = np.all((diffs_abs >= 1) & (diffs_abs <= 3))
        if valid_direction and valid_diffs:
            safe_reports.append(report)
        else:
            unsafe_reports.append(report)
    return safe_reports, unsafe_reports

def main():
    file_path = directory+'input.txt'  # Replace with your input file path
    reports = read_reports_variable_length(file_path)
    safe_reports, unsafe_reports = determine_safe_reports_variable_length(reports)

    print(f"Number of safe reports: {len(safe_reports)}")
    print(f"Number of unsafe reports: {len(unsafe_reports)}")

    # Optionally, print safe reports
    for i, report in enumerate(safe_reports, start=1):
        print(f"Safe Report {i}: {' '.join(map(str, report))}")

if __name__ == "__main__":
    main()

