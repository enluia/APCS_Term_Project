class Matrix:

    def start(students, blocks, courses):

        # Define the matrix variable as a nested dictionary
        matrix = {}
        outside_timetable = []

        # Initialize the nested dictionaries for each key
        for s_key in students:
            matrix[s_key] = {}
            for b in blocks:
                matrix[s_key][b] = {}
                for c_key in courses:
                    matrix[s_key][b][c_key] = 0

        # Assign value of 1 for students chosen courses
        for s_key in students:
            b_key = 0
            ec_key = 8

            # for every couse a student has requested
            for c_key in students[s_key]:
                if (c_key in outside_timetable):
                    matrix[s_key][blocks[ec_key]][c_key] = 1
                    ec_key += 1
                else:
                    matrix[s_key][blocks[b_key]][c_key] = 1
                    b_key += 1





        # Loop through the matrix and print the values
        for s_key in students:
            for b in blocks:
                for c_key in courses:
                    if matrix[s_key][b][c_key] == 1:
                        print(s_key, b, c_key, matrix[s_key][b][c_key])
