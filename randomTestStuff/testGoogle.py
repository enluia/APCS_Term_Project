from ortools.sat.python import cp_model
import random
import csv
from collections import defaultdict

def main():
    # Create the model.
    model = cp_model.CpModel()

    # Create list of subjects
    subjects = ["Math", "English", "History", "Science", "Art", "PE",
                "Biology", "Chemistry", "Physics", "Geography", "Spanish",
                "French", "German", "Music", "Drama", "Computer Science",
                "Health", "Social Studies", "Physical Education", "Business",
                "Economics", "Psychology", "Statistics", "Calculus", "Algebra",
                "Geometry", "Latin", "Japanese", "Chinese", "Italian",
                "Art History", "Literature", "Creative Writing", "Philosophy",
                "Ethics", "Sociology", "Astronomy", "Geology", "Meteorology",
                "Political Science", "Human Rights", "Law", "Marketing",
                "Accounting", "Anthropology", "Archeology", "Communication",
                "Journalism", "Design", "Film Studies"]

    num_subjects = len(subjects)
    num_timeslots = 4  # 4 blocks per day
    num_students = 100

    # Create the variables.
    x = {}
    for s in range(num_subjects):
        for ts in range(num_timeslots):
            x[(s, ts)] = model.NewBoolVar('s%its%i' % (s, ts))

    # Define the valid blocks for each subject
    subject_blocks = {
        "Math": [0, 1],
        "English": [1, 2],
        "Science": [0, 3],
        # Add more subject-block mappings as needed
    }

    # Student course requests
    student_requests = {}
    for st in range(num_students):
        requests = random.sample(range(num_subjects), 5)
        student_requests[st] = requests

    for s in range(num_subjects):
        for ts in range(num_timeslots):
            if ts not in subject_blocks.get(subjects[s], []):
                model.Add(x[(s, ts)] == 0)  # Subject can't be scheduled in invalid blocks

    for st, requests in student_requests.items():
        for s in requests:
            model.Add(sum(x[(s, ts)] for ts in range(num_timeslots)) >= 1)

    # Solve the problem.
    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter()
    status = solver.SearchForAllSolutions(model, solution_printer)

    # Get the best solution, whether feasible or not
    best_solution = solution_printer.get_best_solution()

    # Write the best solution to the CSV file
    with open('timetable.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject", "Blocks"])
        if best_solution is not None:
            for subject, blocks in best_solution.items():
                writer.writerow([subject, blocks])
        else:
            for subject in subjects:
                writer.writerow([subject, ""])

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.best_solution = None

    def OnSolutionCallback(self):
        num_subjects = len(subjects)
        num_timeslots = 4
        timetable = defaultdict(list)
        for ts in range(num_timeslots):
            for s in range(num_subjects):
                if self.BooleanValue(x[(s, ts)]):
                    timetable[subjects[s]].append(ts)
        if self.best_solution is None or len(timetable) > len(self.best_solution):
            self.best_solution = timetable

    def get_best_solution(self):
        return self.best_solution

if __name__ == '__main__':
    main()
