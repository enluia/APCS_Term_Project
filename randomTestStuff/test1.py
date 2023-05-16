import csv

# read in student data and parse it
def parse_csv(file_path):
    data = []
    current_set = None

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        is_course_header = False

        for row in reader:
            if row[0].startswith("ID"):
                # Start of a new set
                if current_set is not None:
                    data.append(current_set)
                current_set = {'ID': row[0], 'Descriptor': row[1]}
                is_course_header = True

            elif is_course_header:
                # Course headers row
                is_course_header = False

            else:
                # Course data row
                course_id = row[0]
                current_set.setdefault('CourseIDs', []).append(course_id)

        if current_set is not None:
            data.append(current_set)

    return data

# count occurences of each course
def count_course_occurrences(parsed_data):
    course_occurrences = {}

    for set_data in parsed_data:
        for course_id in set_data.get('CourseIDs', []):
            course_occurrences[course_id] = course_occurrences.get(course_id, 0) + 1

    sorted_occurrences = sorted(course_occurrences.items(), key=lambda x: x[1], reverse=True)
    return sorted_occurrences

# output and format to a csv
def write_course_occurrences_to_csv(sorted_occurrences, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CourseID', 'Occurrences'])
        for course_id, occurrences in sorted_occurrences:
            writer.writerow([course_id, occurrences])

# parse course information
def parse_csv(filename):
    course_data = []

    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        found_header = False

        for row in reader:
            if not found_header:
                if 'Course Schedule Attributes' in row:
                    found_header = True
                continue

            if len(row) >= 2:
                course_id = row[1].strip()
                max_enrollment = row[9].strip()
                sections = row[14].strip()

                if course_id and max_enrollment and sections:
                    course_data.append((course_id, max_enrollment, sections))

    return course_data

# Usage example:
filename = 'Data for project/Course Information.csv'
courses = parse_csv(filename)

for course in courses:
    print(f"Course ID: {course[0]}")
    print(f"Max Enrollment: {course[1]}")
    print(f"Sections: {course[2]}")
    print()


# Main
csv_file_path = 'studentData.csv'
parsed_data = parse_csv(csv_file_path)
courseOccurrences = count_course_occurrences(parsed_data)
write_course_occurrences_to_csv(courseOccurrences, "courseOccurrences.csv")

