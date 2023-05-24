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

    # Student course requests
    student_requests = {}
    for st in range(num_students):
        requests = random.sample(range(num_subjects), 5)
        student_requests[st] = requests

    for s in range(num_subjects):
        model.Add(sum(x[(s, ts)] for ts in range(num_timeslots)) >= 1)

    for st, requests in student_requests.items():
        for s in requests:
            model.Add(sum(x[(s, ts)] for ts in range(num_timeslots)) >= 1)

    # Solve the problem.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # If a solution is found, store it in a dictionary, then write into a CSV file.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        timetable = defaultdict(list)
        for ts in range(num_timeslots):
            for s in range(num_subjects):
                if solver.Value(x[(s, ts)]) == 1:
                    timetable[subjects[s]].append(ts)

        with open('timetable.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Subject", "Blocks"])
            for subject, blocks in timetable.items():
                writer.writerow([subject, blocks])
    else:
        print("No feasible solution found!")

if __name__ == '__main__':
    main()
