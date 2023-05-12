def mergeSort(arr):
    
    if len(arr) > 1:

        mid = len(arr) // 2

        left = arr[:mid]

        right = arr[mid:]

        mergeSort(left)
        mergeSort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i+= 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

# Test Case 1: Random array
arr = [8, 3, 1, 7, 5, 6, 2, 4]
mergeSort(arr)
print(arr)  # Expected output: [1, 2, 3, 4, 5, 6, 7, 8]

# Test Case 2: Already sorted array
arr = [1, 2, 3, 4, 5, 6, 7, 8]
mergeSort(arr)
print(arr)  # Expected output: [1, 2, 3, 4, 5, 6, 7, 8]

# Test Case 3: Array with duplicate elements
arr = [4, 2, 1, 3, 2, 4, 1, 3]
mergeSort(arr)
print(arr)  # Expected output: [1, 1, 2, 2, 3, 3, 4, 4]

# Test Case 4: Array with negative numbers
arr = [6, -2, 8, -5, 1, 3, -4, 7]
mergeSort(arr)
print(arr)  # Expected output: [-5, -4, -2, 1, 3, 6, 7, 8]

# Test Case 5: Empty array
arr = []
mergeSort(arr)
print(arr) # Expected output: []

# Test Case 6: Array with a single element
arr = [5]
mergeSort(arr)
print(arr)  # Expected output: [5]
