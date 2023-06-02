import csv
import copy

class Matrix:

    def __init__(self):
        self.matrix = {}

    # sets the value of a certain location in the reference to 1
    def assign(self, s_key, b, c_key):
        self.matrix[s_key][b][c_key] = 1

    # start the machine!!!
    def start(self, students_original, blocks, courses_original, sequence, non_simul):

        # copy arrays just in case
        students = copy.deepcopy(students_original)
        courses = copy.deepcopy(courses_original)

        # Sort courses by priority
        courses = dict(sorted(courses.items(), key=lambda x: x[1]['priority']))

        # Define the matrix variable as a nested dictionary
        outside_timetable = ['MDNC-12--L', 'MDNCM12--L', 'MGMT-12L--', 'MCMCC12--L', 'MIMJB12--L', 
                             'MMUOR12S-L', 'YCPA-2AX-L', 'YCPA-2AXE-', 'MGRPR12--L', 'YED--2DX-L', 
                             'YED--2FX-L', 'MWEX-2A--L', 'MWEX-2B--L', 'MCLC-12---',
                             
                             'MDNC-11--L', 'MDNCM11--L', 'MGMT-12L--', 'MCMCC11--L', 'MIMJB11--L',
                             'MMUOR11S-L', 'YCPA-1AX-L', 'YCPA-1AXE-', 'MGRPR11--L', 'YED--1EX-L',
                             'MWEX-2A--L', 'MWEX-2B--L',
                             
                             'YCPA-0AX-L', 'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-',
                             'MMUOR10S-L', 'MDNC-10--L', 'MIDS-0C---', 'MMUJB10--L',
                             
                             'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L']

        # Initialize the matrix
        for s_key in students:
            self.matrix[s_key] = {}
            for b in blocks:
                self.matrix[s_key][b] = {}
                for c_key in courses:
                    self.matrix[s_key][b][c_key] = 0

        # assign courses to students
        b_key = 0

        # start with courses that need prereq
        for prereq in sequence.keys():
            for s_key in students:
                if prereq not in students[s_key]:
                    continue

                # assign postreq
                postreq_count = 0
                for postreq in sequence[prereq]:
                    if postreq in students[s_key]:
                        postreq_count += 1
                        for b in blocks[4:8]:
                            if sum(self.matrix[s_key][b].values()) > 0:
                                continue
                            
                            self.assign(s_key, b, postreq)
                            students[s_key].remove(postreq)
                            break

                # assign prereq
                if postreq_count > 0:
                    for b in blocks[0:4]:
                        if sum(self.matrix[s_key][b].values()) > 0:
                            continue
                        self.assign(s_key, b, prereq)
                        students[s_key].remove(prereq)
                        break

        # then go through non-sequenced courses by priority
        for c_key in courses:
            for s_key in students:
                if c_key not in students[s_key]:
                    continue
                if c_key in outside_timetable:
                    b_key = 8
                else: 
                    b_key = 0

                # assign students requested course to next available block
                for b in blocks[b_key:b_key + 8]:
                    if sum(self.matrix[s_key][b].values()) > 0 or courses[c_key].get("sections") == 0:
                        continue

                    self.assign(s_key, b, c_key)

                    # add non simul courses
                    if non_simul.get(c_key):
                        for non_simul_course in non_simul.get(c_key):
                            if non_simul_course in students[s_key]:
                                self.assign(s_key, b, c_key)
                                students[s_key].remove(non_simul_course)
                            
                    break
        
        # count students in each course
        for c_key in courses:
            count = 0
            for s_key in students:
                for b in blocks:
                    if self.matrix[s_key][b][c_key] == 1:
                        count += 1
            print(c_key, count)

        # Loop through the matrix and print the location of the values of 1
        for s_key in students:
            for b in blocks:
                for c_key in courses:
                    if self.matrix[s_key][b][c_key] == 1:
                        #print(s_key, b, c_key, self.matrix[s_key][b][c_key])
                        pass
                    if c_key in students[s_key]:
                        pass


    # counts percentage of correct courses given to students
    def measure(self, students):


        score = 0
        total_requests = 0
        for s_key in students:
            for b in self.matrix[s_key]:
                for c_key in self.matrix[s_key][b]:
                    if self.matrix[s_key][b][c_key] == 1 and c_key in students[s_key]:
                        score += 1
            total_requests += len(students[s_key])

        print(score, "/", total_requests, "=", score / total_requests * 100)


    def export_to_csv(self, filename, courseData):
        # Collect all blocks and unique courses with assigned value 1
        blocks = sorted(set(b for s_key in self.matrix for b in self.matrix[s_key]))
        block_courses = {b: list(set(c_key for s_key in self.matrix for c_key in self.matrix[s_key][b] if self.matrix[s_key][b][c_key] == 1)) for b in blocks}

        # Collect all unique courses with assigned value 1
        courses = sorted(set(c_key for b in block_courses for c_key in block_courses[b]))

        # Open the CSV file for writing
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the top header row with block names
            writer.writerow(['Courses'] + blocks)

            # Iterate through the courses and write each row
            for c_key in courses:
                courseName = courseData[c_key]['name']
                row = [courseName if c_key in block_courses[b] else "" for b in blocks]
                writer.writerow([c_key] + row)
    
    def get_student_timetable(self, student, courseData):

        print("\nTimetable for Student", student)
        timetable = {}

        for b in self.matrix[student]:
            for c_key in self.matrix[student][b]:
                courseName = courseData[c_key]['name']
                if self.matrix[student][b][c_key] == 1:
                    timetable[b] = courseName
        
        print("\n".join("{}\t{}".format(k, v) for k, v in timetable.items()))
