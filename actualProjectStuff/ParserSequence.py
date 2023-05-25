import csv

class ParserSequence:

    def parse_raw_csv(file_path):
        data = []
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule"):
                    continue

                current_set = {row[2].split()[1]: row[2].split()[3:]}

                data.append(current_set)

        ParserSequence.write_parsed_to_csv(data, "Data for Project/_parsedCourseData.csv")

    # write to csv
    def write_parsed_to_csv(data, file_path):
        headers = ['ID', 'Name', 'Base Terms', 'Max Enrollment', 'Priority', 'Sections']

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for set_data in data:
                writer.writerow(list(set_data.values()))

    # read in parsed data, structure into array
    def read_parsed_csv(file_path):
        data = {}
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                data[row[0]] = {'name': row[1], 'base_terms': row[2], 'max_enroll': row[3], 'priority': row[4], 'sections': row[5]}

        return data
