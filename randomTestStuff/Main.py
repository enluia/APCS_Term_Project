temp = {}

for i in range(int(input())):
    temp[i] = input()

currentMax = 0
max = 0
maxDays = {}

for i in range(5):
    for j in range(len(temp)):
        if temp[j][i] == "Y":
            currentMax += 1    
    maxDays[i] = currentMax
    currentMax = 0