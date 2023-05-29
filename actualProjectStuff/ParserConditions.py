import csv

class ParserConditions:

    # course sequencing
    def parse_sequence_csv(file_path):
        data = []
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule"):
                    continue

                # dictionary based on prereqs
                current_set = {row[2].split()[1]: row[2].split(' before ')[1].split(', ')}

                data.append(current_set)

        return data

    # non simultaneous blocking
    def parse_non_simul_csv(file_path):
        data = {}
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule"):
                    continue

                # only add those in nonsimul
                current_set = row[2].split('Schedule')[1].split(' in a NotSimultaneous')[0].split(', ')

                # create dictionary with every course blocked nonsimul-ly
                for ns_key in current_set:
                    data[ns_key] = current_set
                    data[ns_key].remove(ns_key)

        return data
    
    def parse_simul_csv(file_path):
        data = {}
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule"):
                    continue

                # only add those in nonsimul
                current_set = row[2].split('Schedule')[1].split(' in a Simultaneous')[0].split(', ')

                # create dictionary with every course blocked nonsimul-ly
                for ns_key in current_set:
                    data[ns_key] = current_set
                    data[ns_key].remove(ns_key)

        return data
