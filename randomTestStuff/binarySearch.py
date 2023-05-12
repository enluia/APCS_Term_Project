def binarySearch(arr, low, high, x):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == x:
        return x
    if arr[mid] > x:
        return binarySearch(arr, low, mid - 1, x)
    return binarySearch(arr, mid + 1, high, x)
           
# Test Case 1: Target is present in the middle of the array
arr = [1, 2, 3, 4, 5, 6, 7]
target = 4
print(binarySearch(arr, 0, len(arr) - 1, target))  # Expected output: 4

# Test Case 2: Target is present at the beginning of the array
arr = [1, 2, 3, 4, 5, 6, 7]
target = 1
print(binarySearch(arr, 0, len(arr) - 1, target))  # Expected output: 1

# Test Case 3: Target is present at the end of the array
arr = [1, 2, 3, 4, 5, 6, 7]
target = 7
print(binarySearch(arr, 0, len(arr) - 1, target))  # Expected output: 7

# Test Case 4: Target is not present in the array
arr = [1, 2, 3, 4, 5, 6, 7]
target = 8
print(binarySearch(arr, 0, len(arr) - 1, target))  # Expected output: -1

# Test Case 5: Array contains only one element and it is the target
arr = [5]
target = 5
print(binarySearch(arr, 0, len(arr) - 1, target))  # Expected output: 5

# Test Case 6: Array contains only one element and it is not the target
arr = [5]
target = 2
print(binarySearch(arr, 0, len(arr) - 1, target))  # Expected output: -1

# Test Case 7: Empty array
arr = []
target = 5
print(binarySearch(arr, 0, len(arr) - 1, target))  # Expected output: -1