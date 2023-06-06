import csv
import copy
import random
import time

"""
THINGS TO DO / FIX
- linearity
- simultaneous blocking
- filling spares
- iterating from there
"""

###
# VARIABLES
#

# final variables
RAW_STUDENT_FILE = "Data for Project/Cleaned Student Requests.csv"
RAW_COURSE_FILE = "Data for Project/Course Information.csv"
RAW_BLOCKING_FILE = "Data for Project/Course Blocking Rules.csv"
RAW_SEQUENCING_FILE = "Data for Project/Course Sequencing Rules.csv"
PARSED_STUDENT_FILE = "Data for Project/_parsedStudentData.csv"
PARSED_ALTERNATES_FILE = "Data for Project/_parsedAlternatesData.csv"
PARSED_COURSE_FILE = "Data for Project/_parsedCourseData.csv"
MATRIX_OUTPUT_FILE = "Data for Project/_matrixOutput.csv"
MATRIX_OUTPUT_STUDENT_FILE = "Data for Project/_matrixOutputStudents.csv"
COURSE_SHUFFLE_SEED = 40

bad_courses = ['XLEAD09---',    'MGE--11',    'MGE--12', 'MKOR-10---', 'MKOR-11---',
               'MKOR-12---', 'MIT--12---', 'MSPLG11---', 'MJA--10---', 'MJA--11---',
               'MJA--12---', 'MLTST10---', 'MLTST10--L']

outside_timetable = ['MDNC-12--L', 'MDNCM12--L', 'MGMT-12L--', 'MCMCC12--L', 'MIMJB12--L', 
                     'MMUOR12S-L', 'YCPA-2AX-L', 'YCPA-2AXE-', 'MGRPR12--L', 'YED--2DX-L', 
                     'YED--2FX-L', 'MWEX-2A--L', 'MWEX-2B--L', 'MCLC-12---',
                     
                     'MDNC-11--L', 'MDNCM11--L', 'MGMT-12L--', 'MCMCC11--L', 'MIMJB11--L',
                     'MMUOR11S-L', 'YCPA-1AX-L', 'YCPA-1AXE-', 'MGRPR11--L', 'YED--1EX-L',
                     'MWEX-2A--L', 'MWEX-2B--L',
                     
                     'YCPA-0AX-L', 'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-',
                     'MMUOR10S-L', 'MDNC-10--L', 'MIDS-0C---', 'MMUJB10--L',
                     
                     'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L']

blocks = ['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', '3A', '3B', '3C', '3D', '3E', '3F', '3G', '3H', '3I', '3J', '3K', '3L', '3M']

print('Starting Program')
t0 = time.time()

###
# PARSING
#

# writes dictionaries to a file
def write_dict_csv(headers, data, file_path):

    with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for set_data in data:
                values = data[set_data]
                if type(values) is dict:
                    values = list(data[set_data].values())
                writer.writerow([set_data] + values)

# read student requests data from file_path
def read_student_csv(file_path):
    data = {'requests':{},'alternates':{}}
    current_set = None
    alternate_set = []
    current_student = 0
    headers = ['ID', 'Courses']

    with open(file_path, 'r') as file:
        reader = csv.reader(file)

        for row in reader:

            # start of a new set
            if row[0].startswith("ID"):
                if current_set == None:
                    current_student = row[1]
                    current_set = []
                    continue
                data['requests'].setdefault(current_student, current_set)
                data['alternates'].setdefault(current_student, alternate_set)
                current_student = row[1]
                current_set = []
                alternate_set = []

            # skip headers
            elif row[0] == 'Course':
                continue
                
            # course data row
            else:
                course_id = row[0]
                if course_id in bad_courses:
                    continue

                if row[11] == 'N':
                    current_set.append(course_id)

                elif row[11] == 'Y':
                    alternate_set.append(course_id)

        # end of file
        data['requests'].setdefault(current_student, current_set)
        data['alternates'].setdefault(current_student, alternate_set)

    # verify results
    write_dict_csv(headers, data['requests'], PARSED_STUDENT_FILE)
    write_dict_csv(headers, data['alternates'], PARSED_ALTERNATES_FILE)

    return data

# read course information data from file_path
def read_course_csv(file_path):
    
    data = {}
    current_set = None
    headers = ['ID', 'Name', 'Base Terms', 'Max Enrollment', 'Priority', 'Sections']

    with open(file_path, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            
            # skip headers
            if row[0] == "Greater Victoria" or row[0].startswith("Page") or row[0] == "" or row[9] == "0":
                continue

            # data points
            current_set = {'name': row[2], 'base_terms': row[7], 'max_enroll': row[9], 'priority': row[12], 'sections': row[14]}

            # space for each section
            for i in range(int(row[14])):
                current_set.setdefault(i, {"block": None, "students": []})

            data.setdefault(row[0], current_set)

    # verify result
    write_dict_csv(headers, data, PARSED_COURSE_FILE)

    # sort by priority
    data = dict(sorted(data.items(), key=lambda x: x[1]['priority']))

    return data

# read course sequencing data from file_path
def read_sequencing_csv(file_path):
    data = {}

    with open(file_path, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            
            if row[1] == "" or row[1].startswith("Rule"):
                continue

            # dictionary based on prereqs
            data[row[2].split()[1]] = row[2].split(' before ')[1].split(', ')

    return data

# read blocking data from file_path
def read_blocking_csv(file_path, blocking_type):
    data = {}
    current_set = None

    with open(file_path, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            
            if row[1] == "" or row[1].startswith("Rule") or blocking_type not in row[2]:
                continue

            # only add those in blocks
            current_set = row[2].split('Schedule')[1].split(' in a ' + blocking_type)[0].split(', ')

            if blocking_type == "Terms":
                # haha its course sequencing now
                data[current_set[0]] = current_set[1]

            else:
                # create dictionary with every course blocked simul-ly
                for blocking_key in current_set:
                    data[blocking_key] = current_set
                    data[blocking_key].remove(blocking_key)

    return data


###
# MATRIX
#

# initialize the matrix
def matrix_init():
    for s_key in STUDENTS:
        matrix[s_key] = {}
        for b in blocks:
            matrix[s_key][b] = {}
            for c_key in courses:
                matrix[s_key][b][c_key] = 0

# assign student to course
def matrix_assign(s_key, b, c_key, section_num):

    # assign a course to a block for a student
    matrix[s_key][b][c_key] = 1

    # add student to class list
    courses[c_key][section_num]['students'].append(s_key)

    # remove class from student's active requests
    requests[s_key].remove(c_key)

# start filling the matrix using a modified greedy algorithm
def matrix_start():

    # start with courses that need prereq
    for prereq in sequencing.keys():
        for s_key in requests:
            if prereq not in requests[s_key]:
                continue

            # assign postreq
            postreq_count = 0
            for postreq in sequencing[prereq]:
                if postreq in requests[s_key]:
                    postreq_count += 1
                    for b in blocks[4:8]:
                        if sum(matrix[s_key][b].values()) > 0:
                            continue
                        
                        save_i = None
                        global courses
                        for i in range(int(courses[postreq]['sections'])):
                            # unassigned section
                            if courses[postreq][i]['block'] == None:
                                courses[postreq][i]['block'] = b

                            # class with space in correct block
                            if courses[postreq][i]['block'] == b and len(courses[postreq][i]['students']) < int(courses[postreq]['max_enroll']):
                                matrix_assign(s_key, b, postreq, i)
                                save_i = i
                                break

                        # student has space but course in block does not
                        if save_i is None:
                            continue
                        break

            # assign prereq
            if postreq_count > 0:
                for b in blocks[0:4]:
                    if sum(matrix[s_key][b].values()) > 0:
                        continue

                    save_i = None
                    for i in range(int(courses[prereq]['sections'])):
                            
                        # unassigned section
                        if courses[prereq][i]['block'] == None:
                            courses[prereq][i]['block'] = b

                        # class with space in correct block
                        if courses[prereq][i]['block'] == b and len(courses[prereq][i]['students']) < int(courses[prereq]['max_enroll']):
                            matrix_assign(s_key, b, prereq, i)
                            save_i = i
                            break

                    # student has space but course in block does not
                    if save_i is None:
                        continue
                    break

    # then go through non-sequenced courses by priority
    b_key = 0
    
    courses = shuffle_dict(courses, COURSE_SHUFFLE_SEED)

    for c_key in courses:

        for s_key in requests:
            if c_key not in requests[s_key]:
                continue
            if c_key in outside_timetable:
                b_key = 8
            else: 
                b_key = 0

            # assign students requested course to next available block
            for b in blocks[b_key:b_key + 8]:
                if sum(matrix[s_key][b].values()) > 0:
                    continue

                save_i = None
                for i in range(int(courses[c_key]['sections'])):

                    # unassigned section
                    if courses[c_key][i]['block'] == None:
                        courses[c_key][i]['block'] = b

                    # class with space in correct block
                    if courses[c_key][i]['block'] == b and len(courses[c_key][i]['students']) < int(courses[c_key]['max_enroll']):
                        matrix_assign(s_key, b, c_key, i)
                        save_i = i
                        break

                # add non simul courses if they exist and blockee was added
                if non_simul.get(c_key) and save_i is not None:
                    for non_simul_course in non_simul.get(c_key):
                        if non_simul_course in requests[s_key]:
                            matrix_assign(s_key, b, non_simul_course, save_i)
                            courses[non_simul_course][save_i]['block'] = b
                
                # student has space but course in block does not
                if save_i is None:
                    continue
                break

# measure scheduling successes
def matrix_measure():

    # percentage of total requests received
    coursesPlaced = 0
    total_requests = 0
    for s_key in STUDENTS:
        for b in matrix[s_key]:
            for c_key in matrix[s_key][b]:
                if matrix[s_key][b][c_key] == 1 and c_key in STUDENTS[s_key]:
                    coursesPlaced += 1
        total_requests += len(STUDENTS[s_key])

    print_percent(coursesPlaced, total_requests, "fulfilled requests sans alternates")
    print_percent(coursesPlaced, total_requests + num_alternates, "fulfilled requests with alternates")

    # number of students with full timetables
    # accounting for ecs?
    fullTimetable = 0
    i = 0
    for s_key in STUDENTS:
        coursesGiven = 0
        for b in matrix[s_key]:
            for c_key in matrix[s_key][b]:
                if matrix[s_key][b][c_key] == 1 and c_key in STUDENTS[s_key]:
                    coursesGiven += 1
        if coursesGiven == 8:
            fullTimetable += 1
            if i < 3:
                #matrix_get_student_timetable(str(s_key))
                i += 1
    print_percent(fullTimetable, len(STUDENTS), "students got 8/8 requested courses")
    print_percent(fullTimetable, len(STUDENTS), "students got 8/8 requested or alternate courses")

    # number of students with over 5 courses
    coursesOver5 = 0
    for s_key in STUDENTS:
        if count_student_courses(s_key) > 5:
            coursesOver5 += 1
    
    print_percent(coursesOver5, len(STUDENTS), "students got more than 5 courses")

# get a student's timetable
def matrix_get_student_timetable(student):

    student = str(student)
    print("\nTimetable for Student", student)
    timetable = {}

    for b in matrix[student]:
        for c_key in matrix[student][b]:
            course_name = courses[c_key]['name']
            if matrix[student][b][c_key] == 1:
                timetable[b] = course_name

    print("\n".join("{}\t{}".format(k, v) for k, v in timetable.items()))

def count_student_courses(student):

    counter = 0
    student = str(student)
    timetable = {}

    for b in matrix[student]:
        for c_key in matrix[student][b]:
            course_name = courses[c_key]['name']
            if matrix[student][b][c_key] == 1:
                counter += 1

    return counter

# export matrix to csv
def matrix_export_to_csv(filename):

    # Collect all blocks and unique courses with assigned value 1
    collected_blocks = sorted(set(b for s_key in matrix for b in matrix[s_key]))
    block_courses = {b: list(set(c_key for s_key in matrix for c_key in matrix[s_key][b] if matrix[s_key][b][c_key] == 1)) for b in collected_blocks}

    # Collect all unique courses with assigned value 1
    collected_courses = sorted(set(c_key for b in block_courses for c_key in block_courses[b]))

    # Open the CSV file for writing
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the top header row with block names
        writer.writerow(['Courses'] + collected_blocks)

        # Iterate through the courses and write each row
        for c_key in collected_courses:
            course_name = courses[c_key]['name']
            row = [course_name if c_key in block_courses[b] else "" for b in blocks]
            writer.writerow([c_key] + row)

# exprt student schedules to csv
def matrix_export_students(filename):
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID'] + blocks)

        for s_key in STUDENTS:
            stud_sched = [s_key] + [None] * len(blocks)
            for b_key in range(len(blocks)):
                stud_sched_block = ""
                for c_key in courses:
                    if matrix[s_key][blocks[b_key]][c_key] == 1:
                        stud_sched_block += '\n' + courses[c_key]['name']
                stud_sched[b_key + 1] = stud_sched_block[1:]
            writer.writerow(stud_sched)


###
# AUXILIARY
#

# format number as fraction and percent
def print_percent(a, b, desc):
    print(a, "/", b, "=", str(a / b * 100)[:5] + '%', desc)

# count alternates
def count_alternates():
    tot = 0
    for s_key in ALTERNATES:
        tot += len(ALTERNATES[s_key])
    return tot

 # randomness of courses maker
def shuffle_dict(dictionary, num_shuffles):
    keys = list(dictionary.keys())
    shuffled_dict = dictionary.copy()
    for _ in range(num_shuffles):
        random.shuffle(keys)
        shuffled_dict = {key: shuffled_dict[key] for key in keys}
    return shuffled_dict


###
# MAIN
#

matrix = {}

STUDENTS = read_student_csv(RAW_STUDENT_FILE).get('requests')
ALTERNATES = read_student_csv(RAW_STUDENT_FILE).get('alternates')
requests = copy.deepcopy(STUDENTS)
num_alternates = count_alternates()
courses = read_course_csv(RAW_COURSE_FILE)

sequencing = read_sequencing_csv(RAW_SEQUENCING_FILE)
sequencing.update(read_blocking_csv(RAW_BLOCKING_FILE, "Terms"))
non_simul = read_blocking_csv(RAW_BLOCKING_FILE, "NotSimultaneous")
simul = read_blocking_csv(RAW_BLOCKING_FILE, "Simultaneous")

print('File Reading Complete')

matrix_init()
matrix_start()
matrix_measure()
matrix_export_to_csv(MATRIX_OUTPUT_FILE)
matrix_export_students(MATRIX_OUTPUT_STUDENT_FILE)
#matrix_get_student_timetable(1780)

print('Program Terminated')
t1 = time.time()
print(t1-t0)