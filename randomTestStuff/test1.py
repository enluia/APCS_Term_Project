import csv

def parse_csv(file_path):
    data = []
    current_set = None
    headers = None

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
                headers = row
                current_set['Headers'] = headers
                is_course_header = False

            else:
                # Course data row
                course_id = row[0]
                course_data = {headers[i]: row[i] for i in range(1, len(headers))}
                current_set[course_id] = course_data

        if current_set is not None:
            data.append(current_set)

    return data

# Example usage
csv_file_path = 'studentData.csv'
parsed_data = parse_csv(csv_file_path)

# Accessing and using the parsed data
for set_data in parsed_data:
    set_id = set_data['ID']
    descriptor = set_data['Descriptor']
    print(f"Set ID: {set_id}, Descriptor: {descriptor}")

    headers = set_data.get('Headers', [])
    description_header_index = headers.index('Description') if 'Description' in headers else -1

    for course_id, course_data in set_data.items():
        if course_id not in ['ID', 'Descriptor', 'Headers']:
            course_description = course_data.get(headers[description_header_index]) if description_header_index != -1 else ''
            recommended = course_data['Recommended']
            alternate = course_data['Alternate']
            credit = course_data['Credit']
            print(f"Course ID: {course_id}, Description: {course_description}, Recommended: {recommended}, Alternate: {alternate}, Credit: {credit}")
