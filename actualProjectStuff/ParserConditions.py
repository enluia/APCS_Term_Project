import csv

class ParserConditions:

    # course sequencing
    def parse_sequence_csv(file_path):
        data = {}

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule"):
                    continue

                # dictionary based on prereqs
                data[row[2].split()[1]] = row[2].split(' before ')[1].split(', ')

        return data

    # non simultaneous blocking
    def parse_non_simul_csv(file_path):
        data = {}
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule") or "NotSimultaneous" not in row[2]:
                    continue

                # only add those in nonsimul
                current_set = row[2].split('Schedule')[1].split(' in a NotSimultaneous')[0].split(', ')

                # create dictionary with every course blocked nonsimul-ly
                for ns_key in current_set:
                    data[ns_key] = current_set
                    data[ns_key].remove(ns_key)

        return data
    
    # simultaneous blocking
    def parse_simul_csv(file_path):
        data = {}
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule") or "Simultaneous" not in row[2]:
                    continue

                # only add those in simul
                current_set = row[2].split('Schedule')[1].split(' in a Simultaneous')[0].split(', ')

                # create dictionary with every course blocked simul-ly
                for simul_key in current_set:
                    data[simul_key] = current_set
                    data[simul_key].remove(simul_key)

        return data
  
    # terms blocking
    def parse_terms_csv(file_path):
        data = {}
        current_set = None

        with open(file_path, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                
                if row[1] == "" or row[1].startswith("Rule") or "Terms" not in row[2]:
                    continue

                # only add those in terms
                current_set = row[2].split('Schedule')[1].split(' in a Terms')[0].split(', ')

                # haha its course sequencing now
                data[current_set[0]] = current_set[1]

        return data