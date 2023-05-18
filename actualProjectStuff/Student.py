class Student:
    def __init__(self, studentID, coursePreferences):
        self.studentID = studentID
        self.coursePreferences = coursePreferences

    def __str__(self):
        return f"{self.studentID}: {self.coursePreferences}"