import csv

class Parser:

    def parse_raw_csv(file_path):
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
                    current_set = {'ID': row[1]}
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

        Parser.write_parsed_to_csv(data, "Data for Project/_parsedStudentData.csv")

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