import csv

# Open the CSV file
with open('Data for Project/Updated Course Information.csv', 'r') as file:
    # create the csv reader
    reader = csv.reader(file)
    
    # Skip the header row
    next(reader)
    
    # create the dictionary
    course_dict = {}

    for row in reader:
        course_number = row[1].strip()  # Assuming Course Number is second column
        section_count = row[13].strip()  # Assuming Section Count is last column
        
        # Only process rows where both fields are not empty
        if course_number is not "\'\'" and section_count is not "\'\'":  
            course_dict[course_number] = int(section_count)  # Try to convert section_count to int

    print(course_dict)