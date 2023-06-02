from ortools.sat.python import cp_model

def main():
    # Create the model.
    model = cp_model.CpModel()

    # Suppose we have 5 students and 7 courses
    num_students = 1
    num_courses = 1
    num_blocks = 1

    # Suppose students have the following preferences (0-indexed)
    preferences = [[0, 1, 2], [2, 3, 4], [1, 2, 4, 5], [3, 5, 6], [0, 2, 6]]
    
    # Variables
    x = {}
    for i in range(num_students):
        for j in range(num_courses):
            for k in range(num_blocks):
                x[i, j, k] = model.NewBoolVar('x[%i,%i,%i]' % (i, j, k))

    # Each block has at most one course
    for i in range(num_students):
        for k in range(num_blocks):
            model.Add(sum(x[i, j, k] for j in range(num_courses)) <= 1)

    # Each course should be in the preference list of the student
    for i in range(num_students):
        for j in range(num_courses):
            if j not in preferences[i]:
                for k in range(num_blocks):
                    model.Add(x[i, j, k] == 0)

    # Each student should attend 8 courses (8 blocks)
    for i in range(num_students):
        model.Add(sum(x[i, j, k] for j in range(num_courses) for k in range(num_blocks)) == num_blocks)

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        for i in range(num_students):
            for k in range(num_blocks):
                for j in range(num_courses):
                    if solver.Value(x[i, j, k]) == 1:
                        print('Student', i, 'takes course', j, 'at block', k)

        if status == cp_model.FEASIBLE:
            for i in range(num_students):
                for k in range(num_blocks):
                    for j in range(num_courses):
                        if solver.Value(x[i, j, k]) == 1:
                            print('Student', i, 'takes course', j, 'at block', k)
    else:
        print('Solver status:', status)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    print('Solver status: ', solver.StatusName(status))
    print('Number of branches: ', solver.NumBranches())
    print('Number of conflicts: ', solver.NumConflicts())

if __name__ == '__main__':
    main()


