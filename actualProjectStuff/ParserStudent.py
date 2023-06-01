import csv

class ParserStudent:

    def parse_raw_csv(file_path):
        data = []
        current_set = None

        bad_courses = ['XLEAD09---',    'MGE--11',    'MGE--12', 'MKOR-10---',
                       'MKOR-11---', 'MKOR-12---', 'MIT--12---', 'MSPLG11---',
                       'MJA--10---', 'MJA--11---', 'MJA--12---',
                       
                       'MLTST10---', 'MLTST10--L']

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                # Start of a new set
                if row[0].startswith("ID"):
                    if current_set is not None:
                        data.append(current_set)
                    current_set = {'ID': row[1]}

                # Skip headers and alternates
                elif row[0] == 'Course' or row[11] == 'Y':
                    continue
                    
                # Course data row
                else:
                    course_id = row[0]
                    if course_id in bad_courses:
                        continue
                    current_set.setdefault('CourseIDs', []).append(course_id)

            if current_set is not None:
                data.append(current_set)

        ParserStudent.write_parsed_to_csv(data, "Data for Project/_parsedStudentData.csv")

    # write to csv
    def write_parsed_to_csv(data, file_path):
        headers = ['ID', 'CourseIDs']

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for set_data in data:
                set_id = set_data['ID']
                course_ids = set_data.get('CourseIDs', [])

                writer.writerow([set_id, ','.join(course_ids)])

    # read in parsed data, structure into array
    def read_parsed_csv(file_path):
        data = {}

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                set_id = row[0]
                course_ids = row[1].split(",")
                data[set_id] = course_ids

        return data
