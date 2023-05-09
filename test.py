import random

class ww:
    def myMeth(x):
        print(x)

x = []
sum = 0

for i in range(10):
    temp = []
    for j in range(10):
        temp.append(random.randrange(1, 10))
    x.append(temp)

for i in range(len(x)):
    for j in range(len(x[i])):
        print(x[i][j], end = " ")
        sum += x[i][j]
    print()

print(sum)

ww.myMeth("ur mom")