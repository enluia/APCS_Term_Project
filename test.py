import random

class ww:
    def myMeth(x):
        print(x)

    def twoSum(target, nums):
        for i in range(len(nums)):
            for j in range(len(nums) - i - 1):
                if nums[i] + nums[j + i + 1] == target:
                    return [i, j + i + 1]
                
    def isPalindrome(num):
        myStr = str(num)
        for i in range(int(len(myStr) / 2)):
            if myStr[i] != myStr[-i - 1]:
                return False
        return True
    
    def findMed(nums1, nums2):
        mergedLength = len(nums1) + len(nums2)
        temp1 = 0
        isFinished1 = False
        temp2 = 0
        isFinished2 = False
        median = 0

        if mergedLength % 2 == 0:
            for i in range(int(mergedLength / 2) + 1):
                temp = 0
                if isFinished1:
                    temp = nums2[temp2]
                elif isFinished2:
                    temp = nums1[temp1]
                else:
                    temp = min(nums1[temp1], nums2[temp2])
                if isFinished2 or nums1[temp1] < nums2[temp2]:
                    temp1 += 1
                else:
                    temp2 += 1
                if i == int(mergedLength / 2) - 1:
                    median = temp
                elif i == int(mergedLength / 2):
                    median = (median + temp)/2
                if temp1 >= len(nums1):
                    isFinished1 = True
                if temp2 >= len(nums2):
                    isFinished2 = True
        else:
            for i in range(int(mergedLength / 2) + 1):
                temp = 0
                if i == int(mergedLength / 2):
                    if isFinished1:
                        temp = nums2[temp2]
                    elif isFinished2:
                        temp = nums1[temp1]
                    else:
                        temp = min(nums1[temp1], nums2[temp2])
                if isFinished2 or nums1[temp1] < nums2[temp2]:
                    temp1 += 1
                else:
                    temp2 += 1
                if temp1 >= len(nums1):
                    isFinished1 = True
                if temp2 >= len(nums2):
                    isFinished2 = True
        return median

print(ww.findMed([1, 2], [3, 4, 7]))   
#print(ww.isPalindrome(13531))
#print(ww.twoSum(9, [1, 34, 5, 2, 7, 3]))

x = []
sum = 0

for i in range(10):
    temp = []
    for j in range(10):
        temp.append(random.randrange(1, 10))
    x.append(temp)

for i in range(len(x)):
    for j in range(len(x[i])):
#        print(x[i][j], end = " ")
        sum += x[i][j]
    #print()

#print(sum)

#ww.myMeth("ur mom")

#yes