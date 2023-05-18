from timetable import Timetable
from Block import Block
from Course import Course
from Student import Student
from Parser import Parser
from CourseParser import CourseParser
import csv

class SystemManager:

    Parser.parse_raw_csv("Data for Project/Cleaned Student Requests.csv")
    parsed_data = Parser.read_parsed_csv("Data for Project/_parsedStudentData.csv")

    students = []

    # Accessing the parsed data
    for set_id, course_ids in parsed_data.items():
        students.append(Student(set_id, course_ids))

    for i in students:
        print(i)

    CourseParser.parse_raw_csv("Data for Project/Course Information.csv")