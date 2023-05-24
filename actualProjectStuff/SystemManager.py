from timetable import Timetable
from Block import Block
from Course import Course
from Student import Student
from Parser import Parser
from CourseParser import CourseParser
from Matrix import Matrix
import csv

class SystemManager:

    # students
    Parser.parse_raw_csv("Data for Project/Cleaned Student Requests.csv")
    parsed_student_data = Parser.read_parsed_csv("Data for Project/_parsedStudentData.csv")

    students = []

    for set_id, course_ids in parsed_student_data.items():
        students.append(Student(set_id, course_ids))

    for i in students:
        print(i)

    # blocks
    blocks = ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J']

    # courses
    CourseParser.parse_raw_csv("Data for Project/Course Information.csv")
    parsed_course_data = CourseParser.read_parsed_csv("Data for Project/_parsedCourseData.csv")

    for i in parsed_course_data:
        print(i, parsed_course_data[i])

    # matrix
    Matrix.start(parsed_student_data, parsed_course_data)
