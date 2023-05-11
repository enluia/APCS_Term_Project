inputFile = open("studentData.csv", "r")

inputArray = []

for line in inputFile:
    inputArray = line

for line in inputArray:
    print(inputArray[line], end = "")