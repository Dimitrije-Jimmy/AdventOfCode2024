import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'
file_path = directory+'input.txt'
print(file_path)

import numpy as np

def is_report_safe(report):
    diffs = np.diff(report)
    is_increasing = np.all(diffs > 0)
    is_decreasing = np.all(diffs < 0)
    valid_direction = is_increasing or is_decreasing
    diffs_abs = np.abs(diffs)
    valid_diffs = np.all((diffs_abs >= 1) & (diffs_abs <= 3))
    return valid_direction and valid_diffs

def determine_safe_reports_with_dampener(reports):
    safe_reports = []
    unsafe_reports = []
    total_safe = 0
    
    for report in reports:
        if is_report_safe(report):
            safe_reports.append(report)
            total_safe += 1
        else:
            report_length = len(report)
            made_safe = False
            for i in range(report_length):
                modified_report = np.delete(report, i)
                if is_report_safe(modified_report):
                    safe_reports.append(report)
                    total_safe += 1
                    made_safe = True
                    break
            if not made_safe:
                unsafe_reports.append(report)
    return total_safe, safe_reports, unsafe_reports

def read_reports_variable_length(file_path):
    reports = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                levels = np.array(list(map(int, line.strip().split())))
                reports.append(levels)
    return reports

def main():
    file_path = directory+'input.txt'  # Replace with your input file path
    reports = read_reports_variable_length(file_path)
    
    # Part One: Safe reports without the Dampener
    safe_reports_initial = [report for report in reports if is_report_safe(report)]
    total_safe_initial = len(safe_reports_initial)
    print(f"Number of safe reports without Dampener: {total_safe_initial}")
    
    # Part Two: Safe reports with the Dampener
    total_safe_with_dampener, safe_reports, unsafe_reports = determine_safe_reports_with_dampener(reports)
    print(f"Number of safe reports with Dampener: {total_safe_with_dampener}")
    print(f"Number of safe reports with Dampener: {len(safe_reports)}")
    
    # Optionally, print safe reports
    print("\nSafe Reports:")
    #for i, report in enumerate(safe_reports, start=1):
    #    print(f"Report {i}: {' '.join(map(str, report))}")
    
    print("\nUnsafe Reports:")
    #for i, report in enumerate(unsafe_reports, start=1):
    #    print(f"Report {i}: {' '.join(map(str, report))}")

if __name__ == "__main__":
    main()


