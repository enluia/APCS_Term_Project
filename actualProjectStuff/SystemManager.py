from timetable import Timetable
from Block import Block
from Course import Course
from Student import Student
from ParserStudent import ParserStudent
from ParserCourse import ParserCourse
from Matrix import Matrix
import csv

class SystemManager:

    # students
    ParserStudent.parse_raw_csv("Data for Project/Cleaned Student Requests.csv")
    parsed_student_data = ParserStudent.read_parsed_csv("Data for Project/_parsedStudentData.csv")

    students = []

    for set_id, course_ids in parsed_student_data.items():
        students.append(Student(set_id, course_ids))

    for i in students:
        print(i)

    # blocks
    blocks = blocks = ['1A', '1B', '1C', '1D', '2A', '2B', '2C', '2D', '3A', '3B', '3C', '3D', '3E', '3F', '3G', '3H', '3I', '3J', '3K', '3L', '3M']

    # courses
    ParserCourse.parse_raw_csv("Data for Project/Course Information.csv")
    parsed_course_data = ParserCourse.read_parsed_csv("Data for Project/_parsedCourseData.csv")

    for i in parsed_course_data:
        print(i, parsed_course_data[i])

    # matrix
    Matrix.start(parsed_student_data, blocks, parsed_course_data)

    #hi
