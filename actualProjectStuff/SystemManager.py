from timetable import Timetable
from Block import Block
from Course import Course
from Student import Student
from Parser import Parser
from CourseParser import CourseParser
import csv

class SystemManager:

    # students
    Parser.parse_raw_csv("Data for Project/Cleaned Student Requests.csv")
    parsed_data = Parser.read_parsed_csv("Data for Project/_parsedStudentData.csv")

    students = []

    for set_id, course_ids in parsed_data.items():
        students.append(Student(set_id, course_ids))

    for i in students:
        print(i)

    # courses
    CourseParser.parse_raw_csv("Data for Project/Course Information.csv")
    parsed_course_data = CourseParser.read_parsed_csv("Data for Project/_parsedCourseData.csv")

    courses = []

    for name, base_terms, max_enroll, priority, sections in parsed_course_data.items():
        courses.append(Course(name, base_terms, max_enroll, priority, sections))

    for i in courses:
        print(i)
