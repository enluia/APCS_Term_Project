import csv
import copy

class Matrix:

    def __init__(self):
        self.matrix = {}

    def start(self, students_original, blocks, courses, sequence, non_simul):

        # copy students just in case
        students = copy.deepcopy(students_original)

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

                            self.matrix[s_key][b][postreq] = 1
                            students[s_key].remove(postreq)
                            break

                # assign prereq
                if postreq_count > 1:
                    for b in blocks[0:4]:
                        if sum(self.matrix[s_key][b].values()) > 0:
                            continue

                        self.matrix[s_key][b][prereq] = 1
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
                    if sum(self.matrix[s_key][b].values()) > 0:
                        continue

                    self.matrix[s_key][b][c_key] = 1

                    # add non simul courses
                    if non_simul.get(c_key):
                        for non_simul_course in non_simul.get(c_key):
                            if non_simul_course in students[s_key]:
                                self.matrix[s_key][b][non_simul_course] = 1
                                students[s_key].remove(non_simul_course)
                            
                    break

        my_sum = 0
        # Loop through the matrix and print the values
        for s_key in students:
            for b in blocks:
                for c_key in courses:
                    if self.matrix[s_key][b][c_key] == 1:
                        print(s_key, b, c_key, self.matrix[s_key][b][c_key])
                        my_sum += 1
        print(my_sum)

    # counts percentage of correct course given to students
    def measure(self, students):

        """TEMPORARY: COURSES NOT GIVEN"""
        for s_key in students:
            for c_key in students[s_key]:
                course_freq = 0
                for b in self.matrix[s_key]:
                    if self.matrix[s_key][b].get(c_key) == None:
                        print("Course code not found:")
                        break
                    course_freq += self.matrix[s_key][b][c_key] 
                if course_freq == 0:
                    print(s_key, c_key)
        """============================"""

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

        print(score/7130*100, '%')
        

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
