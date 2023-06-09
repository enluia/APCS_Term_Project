# APCS Final Project: Timetables
# by Daniel, Jason, and William

import csv
import copy
import random
import time

print('\nStarting Program')
t0 = time.time()


###
# VARIABLES
#

# final variables
RAW_STUDENT_FILE = "Data for Project/Cleaned Student Requests.csv"
RAW_COURSE_FILE = "Data for Project/Better Course Information.csv"
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

blocks = ['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', 'Outside']


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
    temp_num_req = [0] * 10
    temp_num_ec = 0

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
                temp_num_req[len(current_set) - temp_num_ec] += 1

                current_student = row[1]
                current_set = []
                alternate_set = []
                temp_num_ec = 0

            # skip headers
            elif row[0] == 'Course':
                continue
                
            # course data row
            else:
                course_id = row[0]
                if course_id in bad_courses:
                    continue

                # temp
                if course_id in outside_timetable:
                    temp_num_ec += 1

                if row[11] == 'N':
                    current_set.append(course_id)

                elif row[11] == 'Y':
                    alternate_set.append(course_id)

        # end of file
        data['requests'].setdefault(current_student, current_set)
        data['alternates'].setdefault(current_student, alternate_set)
        temp_num_req[len(current_set) - temp_num_ec] += 1

    # verify results
    write_dict_csv(headers, data['requests'], PARSED_STUDENT_FILE)
    write_dict_csv(headers, data['alternates'], PARSED_ALTERNATES_FILE)

    #print(temp_num_req)

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
                v = {"block": None, "students": []}
                
                # linear
                if int(row[7]) == 1:
                    v = {"block": None, "block2": None, "students": []}
                current_set.setdefault(i, v)

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
            
            if row[1] == "" or row[1].startswith("Rule") or (" " + blocking_type) not in row[2]:
                continue

            # only add those in blocks
            current_set = row[2].split('Schedule ')[1].split(' in a ' + blocking_type)[0].split(', ')

            if blocking_type == "Terms":
                # haha its course sequencing now
                data[current_set[0]] = current_set[1]

            else:
                # create dictionary with every course blocked simul-ly
                for blocking_key in current_set:

                    if data.get(blocking_key) is None:
                        data[blocking_key] = copy.deepcopy(current_set)
                        data[blocking_key].remove(blocking_key)
                    else:
                        for blocking_value in current_set:
                            if blocking_value not in data[blocking_key] and blocking_value != blocking_key:
                                data[blocking_key] += [blocking_value]

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
def matrix_assign(s_key, b, c_key, section_num, is_linear_and_not_ot = False):

    # assign course to block for student
    matrix[s_key][b][c_key] = 1

    # add student to class lists and remove active request from student
    if c_key in requests[s_key] and not is_linear_and_not_ot:
        courses[c_key][section_num]['students'].append(s_key)
        requests[s_key].remove(c_key)

    # simul
    if simul.get(c_key):
        for simul_course in simul.get(c_key):
            if simul_course in requests[s_key] and not is_linear_and_not_ot:
                if courses[simul_course].get(section_num):
                    courses[simul_course][section_num]['students'].append(s_key)
                requests[s_key].remove(simul_course)

# add non simul courses
def matrix_assign_non_simuls(s_key, b, c_key, i, the_block = 'block', is_linear_and_not_ot = False):
        
    if non_simul.get(c_key):
        for non_simul_course in non_simul[c_key]:

            if non_simul_course in requests[s_key]:
                matrix_assign(s_key, b, non_simul_course, i, is_linear_and_not_ot)
                courses[non_simul_course][i][the_block] = b

# assign students requested course to next available block if possible
def matrix_try_assign(c_key, s_key, b_key, b_key_range):

    for b in blocks[b_key:b_key + b_key_range]:

        if sum(matrix[s_key][b].values()) > 0:
            continue

        successful_assignment = False
        for i in range(int(courses[c_key]['sections'])):

            # unassigned section
            if courses[c_key][i]['block'] == None:
                courses[c_key][i]['block'] = b

                # simul
                if simul.get(c_key):
                    for simul_course in simul.get(c_key):
                        if courses[simul_course].get(i):
                            courses[simul_course][i]['block'] = b

            # class with space in correct block
            if courses[c_key][i]['block'] == b and len(courses[c_key][i]['students']) < int(courses[c_key]['max_enroll']):
                matrix_assign(s_key, b, c_key, i)
                successful_assignment = True
                
                # add non simul courses
                matrix_assign_non_simuls(s_key, b, c_key, i)
                break
        
        # student has space but course in block does not
        if not successful_assignment:
            continue
        break

# start filling the matrix using a modified greedy algorithm
def matrix_start():

    # outside the timetable courses
    for c_key in courses:

        if c_key not in outside_timetable:
            continue

        # only requested by students
        for s_key in requests:
            if c_key not in requests[s_key]:
                continue

            # assign outside timetable
            matrix_assign(s_key, blocks[8], c_key, 0)
                
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
                    matrix_try_assign(postreq, s_key, 4, 8)

            # assign prereq
            if postreq_count > 0:
                matrix_try_assign(prereq, s_key, 0, 4)
    
    # linearity stuff
    for c_key in courses:

        if courses[c_key]['base_terms'] == '1':

            for s_key in requests:
                if c_key not in requests[s_key]:
                    continue

                for b in reversed(blocks[0:4]):

                    if sum(matrix[s_key][b].values()) > 0:
                        continue

                    successful_assignment = False
                    for i in range(int(courses[c_key]['sections'])):

                        both_fit = False

                        # unassigned section
                        if courses[c_key][i]['block'] == None:
                            courses[c_key][i]['block'] = b

                        # class with space in correct block
                        if courses[c_key][i]['block'] == b and len(courses[c_key][i]['students']) < int(courses[c_key]['max_enroll']):
                            
                            for b2 in reversed(blocks[4:8]):

                                if sum(matrix[s_key][b2].values()) > 0:
                                    continue

                                # unassigned section (block2)
                                if courses[c_key][i]['block2'] == None:
                                    courses[c_key][i]['block2'] = b2
                                    
                                if courses[c_key][i]['block2'] == b2:
                                    both_fit = True
                                    matrix_assign(s_key, b, c_key, i)
                                    matrix_assign(s_key, b2, c_key, i)
                                    successful_assignment = True

                                    # add non simul courses
                                    matrix_assign_non_simuls(s_key, b, c_key, i, 'block', True)
                                    matrix_assign_non_simuls(s_key, b2, c_key, i, 'block2')

                                    break
                                
                                continue
                                    
                        if not both_fit:
                            courses[c_key][i]['block'] = None

                    # student has space but course in block does not
                    if not successful_assignment:
                        continue
                    break

    # then go through non-sequenced non-linear courses by priority
    for c_key in courses:

        for s_key in requests:
            if c_key not in requests[s_key]:
                continue

            # assign students requested course to next available block
            matrix_try_assign(c_key, s_key, 0, 8)

    return matrix

# measure scheduling successes
def matrix_measure(matrix):

    # percentage of total requests received
    coursesPlaced = 0
    coursesWithAlts = 0
    total_requests = 0
    for s_key in STUDENTS:
        for b in blocks:
            for c_key in courses:
                if matrix[s_key][b][c_key] == 1:
                    if c_key in STUDENTS[s_key]:
                        coursesPlaced += 1
                    elif c_key in ALTERNATES[s_key]:
                        coursesWithAlts += 1
        total_requests += len(STUDENTS[s_key])

    print_percent(coursesPlaced, total_requests, "fulfilled requests sans alternates")
    print_percent(coursesPlaced + coursesWithAlts, total_requests + num_alternates, "fulfilled requests with alternates")
    print()

    # number of students with full timetables
    fullTimetable = 0
    seven = 0
    six = 0
    fullWithAlts = 0
    sevenWithAlts = 0
    sixWithAlts = 0

    for s_key in STUDENTS:
        coursesGiven = 0
        altsGiven = 0
        for b in matrix[s_key]:
            for c_key in matrix[s_key][b]:
                if matrix[s_key][b][c_key] == 1:
                    if c_key in STUDENTS[s_key]:
                        if courses[c_key]["base_terms"] == "1" and c_key not in outside_timetable:
                            coursesGiven += 0.5
                        else:
                            coursesGiven += 1
                    elif c_key in ALTERNATES[s_key]:
                        altsGiven += 1

        if coursesGiven >= len(STUDENTS[s_key]):
            fullTimetable += 1
        elif coursesGiven == len(STUDENTS[s_key]) - 1:
            seven += 1
        elif coursesGiven == len(STUDENTS[s_key]) - 2:
            six += 1
        
        if coursesGiven + altsGiven >= len(STUDENTS[s_key]):
            fullWithAlts += 1
        elif coursesGiven + altsGiven == len(STUDENTS[s_key]) - 1:
            sevenWithAlts += 1
        elif coursesGiven + altsGiven == len(STUDENTS[s_key]) - 2:
            sixWithAlts += 1

    print_percent(fullTimetable, len(STUDENTS), "students got all requested courses")
    print_percent(seven, len(STUDENTS), "students got all but one requested courses")
    print_percent(six, len(STUDENTS), "students got all but two requested courses")
    print_percent(fullTimetable + seven + six, len(STUDENTS), "is the sum of the above three (sans alternates)")
    print()

    print_percent(fullWithAlts, len(STUDENTS), "students got all requested courses")
    print_percent(sevenWithAlts, len(STUDENTS), "students got all but one requested or alternate courses")
    print_percent(sixWithAlts, len(STUDENTS), "students got all but two requested or alternate courses")
    print_percent(fullWithAlts + sevenWithAlts + sixWithAlts, len(STUDENTS), "is the sum of the above three (with alternates)")
    print()

    print_percent(len(STUDENTS) - fullWithAlts - sevenWithAlts - sixWithAlts, len(STUDENTS), "students with 3-8 requested or alternate courses unfulfilled")
    print()

# get a student's timetable
def matrix_get_student_timetable(student):

    student = str(student)
    output = "Timetable for Student " + student
    timetable = []

    for b in matrix[student]:
        for c_key in matrix[student][b]:
            course_name = courses[c_key]['name']
            if matrix[student][b][c_key] == 1:
                timetable.append({"block": b, "course": course_name})

    return output + "\n" + ("\n".join("{}\t{}".format(i["block"], i["course"]) for i in timetable)) + '\n'

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

# number of courses that are sad :(
def numCoursesSad(threshold):
    
    for c_key in courses:
        for i in range(int(courses[c_key]['sections'])):

            if len(courses[c_key][i]['students']) <= threshold:
                print(c_key, courses[c_key][i]['students'])

# randomness of courses maker
def shuffle_dict(dictionary, num_shuffles):
    keys = list(dictionary.keys())
    shuffled_dict = dictionary.copy()
    for _ in range(num_shuffles):
        random.shuffle(keys)
        shuffled_dict = {key: shuffled_dict[key] for key in keys}
    return shuffled_dict

def check_timetable_feasibility():
    
    for i in STUDENTS:
        print(i)
    
def matrix_courses_per_block():
    coursesPerBlock = {}
    one_a_sample = []
    for b in blocks[0:8]:

        num_courses = 0
        for c_key in courses:

            for i in range(int(courses[c_key]['sections'])):
                if courses[c_key][i]['block'] == b:

                    if c_key in simul:
                        is_found = 'initial'
                        for simul_key in simul:
                            if c_key in simul[simul_key]:
                                is_found = 'as_value'
                                break
                            if simul_key == c_key:
                                is_found = 'as_key'
                                break

                        if is_found == 'as_key':
                            num_courses += 1
                            if b == '1A':
                                one_a_sample.append(c_key)
                            continue

                    num_courses += 1
                    if b == '1A':
                        one_a_sample.append(c_key)

        coursesPerBlock[b] = num_courses
    
    #print(one_a_sample)
    return coursesPerBlock


###
# EVOLUTIONARY
#

def mutate(matrix):
    """
    Mutate a timetable by randomly changing a course assignment.

    Args:
        matrix (dict): The timetable to mutate.
        num_blocks (int): The total number of blocks.
        courses (dict): The courses dictionary.
    """
    num_mutations = random.randint(1, len(STUDENTS)*len(blocks))

    for _ in range(num_mutations):
        student_key = random.choice(list(matrix.keys()))
        block_index = random.choice(range(len(blocks)))
        course_key = random.choice(range(len(courses)))
        matrix[student_key][block_index][course_key] = random.choice(courses)

    return matrix

 #   randomBlockKey = random.randint(0, len(courses))
  #  print("random", randomBlockKey, len(courses))
#
 #   randomBlocks = []
  #  for i in range(COURSE_SHUFFLE_SEED):
   #     print(courses)
    #    random.randint(0, len(courses))
#
 #       randomBlocks.append(courses[random.randint(0, len(courses))])
  #      print(randomBlocks[i])
#
 #   
  #  for block_key in matrix[1000]:
   #     for course_key in matrix[1000][block_key]:
    #        print(course_key)
            

def crossover(matrix1, matrix2):
    """
    Perform a crossover operation on two timetables.

    Args:
        matrix1 (dict): The first timetable.
        matrix2 (dict): The second timetable.
        
    Returns:
        dict: A new timetable that is a result of the crossover.
    """
    if matrix1 is None: print("1 none")
    if matrix2 is None: print("2 none")
    if matrix1 is None or matrix2 is None:
        raise ValueError("Both matrices must be not None")

    # Determine the number of crossover points
    num_crossovers = random.randint(1, len(blocks)-1)
    crossover_points = sorted(random.sample(range(len(blocks)), num_crossovers))

    child = dict(matrix1)

    # Alternate between segments from parent1 and parent2
    for i in range(len(crossover_points) + 1):
        start = crossover_points[i-1] if i > 0 else 0
        end = crossover_points[i] if i < len(crossover_points) else len(blocks)

        for student in STUDENTS:
            print(student)
            for block_index in range(start, end):
                if block_index in matrix1[student] and block_index in matrix2[student]:
                    if i % 2 == 0:
                        child[student][block_index] = matrix1[student][block_index]
                    else:
                        child[student][block_index] = matrix2[student][block_index]

    return child    

def calculate_fitness(matrix):
    """
    Evaluate the fitness of a given timetable.

    This function should evaluate the fitness of a timetable based
    on your specific requirements. It should return a higher score for
    more suitable timetables.

    Args:
        matrix (dict): The timetable to evaluate.
        
    Returns:
        float: The fitness score of the timetable.
    """
    # Implement your fitness calculation here
    print("yes")
    if matrix_measure(matrix) == None:
        return 0
    return matrix_measure(matrix)

def selection(population, scores):
    """
    Select the fittest individuals for reproduction.
    
    Args:
        population (list): The population of timetables.
        scores (list): The fitness scores for the population.
        
    Returns:
        list: The selected parents for reproduction.
    """
    # Zip together the population and scores, sort by scores
    sorted_population = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)

    # Select the top half of the population
    selected = sorted_population[:len(sorted_population)//2]

    # Return only the individuals, not their scores
    return [individual for individual, score in selected]

def evolutionary_algorithm(population_size, num_generations):
    # Initialize a population
    print(population_size)
    population = [matrix_start() for _ in range(population_size)]
    print("WHY ISNT IT WORKING")
    print(population_size)
    for generation in range(num_generations):
        # Calculate the fitness scores for the population
        scores = [calculate_fitness(matrix) for matrix in population]

        # Perform selection
        parents = selection(population, scores)
        # Crossover and mutation
        next_generation = []
        for i in range(population_size // 2):
            if parents is None: print("parents none")
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            if parent1 is None: print("parent1 none")
            if parent2 is None: print("parent2 none")
            child1 = crossover(parent1, parent2)  # ignoring the third (and subsequent) values
            #print(child1)
            #print(child2)
            next_generation.append(mutate(child1))
            #next_generation.append(mutate(child2))

        population = next_generation
    
    # Return the best timetable in the last generation
    scores = [calculate_fitness(matrix) for matrix in population]
    best_index = scores.index(max(scores))
    return population[best_index]

def zero_student_shuffle():
    
    coursesPerBlock = matrix_courses_per_block()

    for b in blocks[0:8]:
        for c_key in courses:
            for i in range(int(courses[c_key]['sections'])):
                if courses[c_key][i]['block'] == b and len(courses[c_key][i]['students']) == 0:
                    courses[c_key][i]['block'] == None
                    temp = 0
                    temp = min(coursesPerBlock.values())
                    print(coursesPerBlock, temp)
                    for block in coursesPerBlock:
                        if temp == coursesPerBlock[block] and block != 'Outside':
                            courses[c_key][i]['block'] = block
                            print(block, b)
                            coursesPerBlock = matrix_courses_per_block()
                            break
###
# MAIN
#

# variable declarations
matrix = {}

STUDENTS_CSV = read_student_csv(RAW_STUDENT_FILE)
STUDENTS = STUDENTS_CSV.get('requests')
ALTERNATES = STUDENTS_CSV.get('alternates')
requests = copy.deepcopy(STUDENTS)
num_alternates = count_alternates()
courses = read_course_csv(RAW_COURSE_FILE)

sequencing = read_sequencing_csv(RAW_SEQUENCING_FILE)
sequencing.update(read_blocking_csv(RAW_BLOCKING_FILE, "Terms"))
non_simul = read_blocking_csv(RAW_BLOCKING_FILE, "NotSimultaneous")
simul = read_blocking_csv(RAW_BLOCKING_FILE, "Simultaneous")

print('File Reading Complete\n')

# matrix operations
matrix_init()
matrix_start()

requests = copy.deepcopy(ALTERNATES)
matrix_start()

matrix_measure(matrix)

zero_student_shuffle()

matrix_export_to_csv(MATRIX_OUTPUT_FILE)
matrix_export_students(MATRIX_OUTPUT_STUDENT_FILE)
print(matrix_get_student_timetable(1284))

#numCoursesSad(5)
print(matrix_courses_per_block())

# done!
print('Program Terminated')
t1 = time.time()
print("Time Elapsed: ", t1 - t0, "seconds\n")

#matrix = selection()
#matrix = crossover(matrix)
#matrix = mutate(matrix)
#matrix_measure()

#evolutionary_algorithm(10, 10)
