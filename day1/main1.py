import numpy as np
import os

directory = os.path.dirname(__file__)+'\\'

# Using standard Python
arr1 = []
arr2 = []
with open(directory+'input.txt', 'r') as file:
    for line in file:
        # Split the line by whitespace and unpack the numbers
        left_num, right_num = map(int, line.strip().split())
        arr1.append(left_num)
        arr2.append(right_num)


#arr1 = [3, 4, 2, 1, 3, 3]
#arr2 = [4, 3, 5, 3, 9, 3]
#print(data)

def main(arr1, arr2):
    arr1 = np.array(arr1)
    arr2 = np.array(arr2)
    
    arr1_srt = np.sort(arr1)
    arr2_srt = np.sort(arr2)
    
    return np.sum(np.abs(arr1_srt - arr2_srt))

print(main(arr1, arr2))

import numpy as np

def calculate_total_distance_numpy(file_path):
    # Load data
    data = np.loadtxt(file_path, dtype=int)
    left_column = data[:, 0]
    right_column = data[:, 1]

    # Sort the arrays
    left_sorted = np.sort(left_column)
    right_sorted = np.sort(right_column)

    # Calculate distances
    distances = np.abs(left_sorted - right_sorted)
    total_distance = np.sum(distances)

    return total_distance

# Usage
total_distance = calculate_total_distance_numpy(directory+'input.txt')
print(f"Total distance using NumPy: {total_distance}")


from collections import Counter

def calculate_similarity_score(file_path):
    left_list = []
    right_list = []

    # Read data from the file
    with open(file_path, 'r') as file:
        for line in file:
            left_num, right_num = map(int, line.strip().split())
            left_list.append(left_num)
            right_list.append(right_num)

    # Count occurrences in the right list
    right_counts = Counter(right_list)

    # Calculate the total similarity score
    total_similarity_score = 0
    for num in left_list:
        count_in_right = right_counts.get(num, 0)
        total_similarity_score += num * count_in_right

    return total_similarity_score

# Usage
score = calculate_similarity_score(directory+'input.txt')
print(f"Total Similarity Score: {score}")


def calculate_similarity_numpy(file_path):
    # Load data
    data = np.loadtxt(file_path, dtype=int)
    arr1 = data[:, 0]
    arr2 = data[:, 1]

    from collections import Counter
    # Count occurrences in the right list
    right_counts = Counter(arr2)

    # Vectorized operation
    #counts = np.vectorize(lambda x: right_counts.get(x, 0))(arr1)
    counts_func = np.vectorize(lambda x: right_counts.get(x, 0))#(arr1)
    counts = counts_func(arr1)
    products = arr1 * counts

    total_similarity_score = np.sum(products)
    return total_similarity_score

# Usage
score = calculate_similarity_numpy(directory+'input.txt')
print(f"Total Similarity Score using NumPy: {score}")    