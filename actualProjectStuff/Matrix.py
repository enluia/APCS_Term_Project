class Matrix:

    def start(students, blocks, courses):

        # Sort courses by priority
        courses = sorted(courses, key=lambda d: courses[d]['priority'])

        # Define the matrix variable as a nested dictionary
        matrix = {}
        outside_timetable = ['MDNC-12--L', 'MDNCM12--L', 'MGMT-12L--', 'MCMCC12--L', 'MIMJB12--L', 
                             'MMUOR12S-L', 'YCPA-2AX-L', 'YCPA-2AXE-', 'MGRPR12--L', 'YED--2DX-L', 
                             'YED--2FX-L', 'MWEX-2A--L', 'MWEX-2B--L', 'MDNC-11--L', 'MDNCM11--L', 
                             'YCPA-1AX-L', 'YCPA-1AXE-', 'MGRPR11--L', 'MCMCC11--L', 'MMUOR11S-L', 
                             'YCPA-0AX-L', 'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'MMUOR10S-L', 
                             'MDNC-10--L', 'MIDS-0C---', 'MMUJB10--L', 'XC---09--L', 'MDNC-09C-L', 
                             'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L']

        # Initialize the nested dictionaries for each key
        for s_key in students:
            matrix[s_key] = {}
            for b in blocks:
                matrix[s_key][b] = {}
                for c_key in courses:
                    matrix[s_key][b][c_key] = 0

        # for every course
        for c_key in courses:

            # for every student
            for s_key in students:
                b_key = 0
                ec_key = 8

                # if course is requested by student
                if c_key in students[s_key]:

                    # assign outside timetable courses
                    if c_key in outside_timetable:
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

    def measure():
        print()