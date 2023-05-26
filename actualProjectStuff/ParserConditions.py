import csv

class ParserConditions:

    def parse_sequence_csv(file_path):
        data = []
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule"):
                    continue

                current_set = {row[2].split()[1]: row[2].split(' before ')[1].split(', ')}

                data.append(current_set)

        return data
