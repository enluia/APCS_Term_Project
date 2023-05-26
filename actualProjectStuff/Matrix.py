class Matrix:

    def __init__(self):
        self.matrix = {}

    def start(self, students, blocks, courses, sequence, non_simul):

        # Sort courses by priority
        courses = sorted(courses, key=lambda d: courses[d]['priority'])

        # Define the matrix variable as a nested dictionary
        outside_timetable = ['MDNC-12--L', 'MDNCM12--L', 'MGMT-12L--', 'MCMCC12--L', 'MIMJB12--L', 
                             'MMUOR12S-L', 'YCPA-2AX-L', 'YCPA-2AXE-', 'MGRPR12--L', 'YED--2DX-L', 
                             'YED--2FX-L', 'MWEX-2A--L', 'MWEX-2B--L', 'MDNC-11--L', 'MDNCM11--L', 
                             'YCPA-1AX-L', 'YCPA-1AXE-', 'MGRPR11--L', 'MCMCC11--L', 'MMUOR11S-L', 
                             'YCPA-0AX-L', 'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'MMUOR10S-L', 
                             'MDNC-10--L', 'MIDS-0C---', 'MMUJB10--L', 'XC---09--L', 'MDNC-09C-L', 
                             'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L']

        # Initialize the nested dictionaries for each key
        for s_key in students:
            self.matrix[s_key] = {}
            for b in blocks:
                self.matrix[s_key][b] = {}
                for c_key in courses:
                    self.matrix[s_key][b][c_key] = 0


        # for every student
        for s_key in students:
            b_key = 0
            ec_key = 8

            # for every course
            for c_key in courses:

                # if course is requested by student
                if c_key in students[s_key]:

                    # assign outside timetable courses
                    if c_key in outside_timetable:
                        self.matrix[s_key][blocks[ec_key]][c_key] = 1
                        ec_key += 1
                    else:
                        self.matrix[s_key][blocks[b_key]][c_key] = 1
                        b_key += 1

        sum = 0
        # Loop through the matrix and print the values
        for s_key in students:
            for b in blocks:
                for c_key in courses:
                    if self.matrix[s_key][b][c_key] == 1:
                        print(s_key, b, c_key, self.matrix[s_key][b][c_key])
                        sum += 1
        print(sum)

    # counts percentage of correct course given to students
    # count number of correctly assigned courses
    def measure(self, students):

        score = 0
        temp = 0
        # go through student array
        # matrix[s_key][blocks[b_key]][c_key]
        for s_key in students:
            for b in self.matrix[s_key]:
                for c_key in self.matrix[s_key][b]:
                    #print(c_key, students[s_key])
                    if self.matrix[s_key][b][c_key] == 1 and c_key in students[s_key]:
                        score += 1
            temp += len(students[s_key])

        print(score, "/", temp)