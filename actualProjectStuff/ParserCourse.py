import csv

class ParserCourse:

    def parse_raw_csv(file_path):
        data = {}
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[0] == "Greater Victoria" or row[0].startswith("Page") or row[0] == "" or row[9] == "0":
                    continue

                current_set = {'name': row[2]}
                current_set.setdefault('base_terms', row[7])
                current_set.setdefault('max_enroll', row[9])
                current_set.setdefault('priority', row[12])
                current_set.setdefault('sections', row[14])

                for i in range(int(row[14])):
                    current_set.setdefault(i, {"block": None, "students": []})

                data.setdefault(row[0], current_set)

        ParserCourse.write_parsed_to_csv(data, "Data for Project/_parsedCourseData.csv")
        return data

    # write to csv
    def write_parsed_to_csv(data, file_path):
        headers = ['ID', 'Name', 'Base Terms', 'Max Enrollment', 'Priority', 'Sections']

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for set_data in data:
                writer.writerow([set_data] + list(data[set_data].values()))

    # read in parsed data, structure into array
    def read_parsed_csv(file_path):
        data = {}

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                data[row[0]] = {'name': row[1], 'base_terms': row[2], 'max_enroll': row[3], 'priority': row[4], 'sections': row[5]}

        return data
