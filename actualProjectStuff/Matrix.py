class Matrix:

    def start(students, blocks, courses):

        # Define the matrix variable as a nested dictionary
        matrix = {}

        # Initialize the nested dictionaries for each key
        for s_key in students:
            matrix[s_key] = {}
            for b in blocks:
                matrix[s_key][b] = {}
                for c_key in courses:
                    matrix[s_key][b][c_key] = 0

        # Loop through the matrix and print the values
        for s_key in students:
            for b in blocks:
                for c_key in courses:
                    print(s_key, b, c_key, matrix[s_key][b][c_key])
