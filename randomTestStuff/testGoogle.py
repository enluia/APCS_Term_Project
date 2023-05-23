from ortools.sat.python import cp_model

num_students = 4
num_blocks = 3
num_classes = 10
all_students = range(num_students)
all_blocks = range(num_blocks)
all_classes = range(num_classes)

model = cp_model.CpModel()

shifts = {}
for n in all_students:
    for d in all_classes:
        for s in all_blocks:
            shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))