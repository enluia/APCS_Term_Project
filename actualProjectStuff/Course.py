class Course:
    def __init__(self, courseID, baseTerms, maxEnrollment, priority, sections):
        self.courseID = courseID
        self.baseTerms = baseTerms
        self.maxEnrollment = maxEnrollment
        self.priority = priority
        self.sections = sections

    def __str__(self):
        return f"{self.courseID}: maxEnrollment: {self.maxEnrollment}"