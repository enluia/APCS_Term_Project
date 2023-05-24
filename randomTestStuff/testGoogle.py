from ortools.sat.python import cp_model

def main():
    # Create the model.
    model = cp_model.CpModel()

    num_teachers = 3
    num_subjects = 3
    num_classrooms = 3
    num_timeslots = 3

    # Create the variables.
    x = {}
    for t in range(num_teachers):
        for s in range(num_subjects):
            for c in range(num_classrooms):
                for ts in range(num_timeslots):
                    x[(t, s, c, ts)] = model.NewBoolVar('t%is%ic%its%i' % (t, s, c, ts))

    # Each timeslot, each classroom has one subject and one teacher.
    for c in range(num_classrooms):
        for ts in range(num_timeslots):
            model.Add(sum(x[(t, s, c, ts)] for t in range(num_teachers) for s in range(num_subjects)) == 1)

    # Each timeslot, each teacher teaches one subject in one classroom.
    for t in range(num_teachers):
        for ts in range(num_timeslots):
            model.Add(sum(x[(t, s, c, ts)] for s in range(num_subjects) for c in range(num_classrooms)) == 1)

    # Each timeslot, each subject is taught by one teacher in one classroom.
    for s in range(num_subjects):
        for ts in range(num_timeslots):
            model.Add(sum(x[(t, s, c, ts)] for t in range(num_teachers) for c in range(num_classrooms)) == 1)

    # Solve the problem.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        for c in range(num_classrooms):
            for ts in range(num_timeslots):
                for t in range(num_teachers):
                    for s in range(num_subjects):
                        if solver.Value(x[(t, s, c, ts)]) == 1:
                            print('Classroom %i in timeslot %i has subject %i taught by teacher %i' % (c, ts, s, t))

if __name__ == '__main__':
    main()