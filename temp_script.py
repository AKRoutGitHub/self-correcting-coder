# Create a list with 10 elements
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

try:
    # Try to print the 10th element
    print(numbers[9])
except IndexError as e:
    # Print an error message if index is out of range
    print("Error: Index out of range")

# Corrected code to only print available elements
available_indices = [i for i in range(len(numbers)) if i < len(numbers)]
print([numbers[i] for i in available_indices])