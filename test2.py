class Solution:
    def longestCommonPrefix(strs):

        output = ""
        shortestLength = len(strs[0])
        shortestString = ""

        print(shortestLength)

        if len(strs) == 1:
            return strs[0]

        for i in strs:
            if len(i) <= shortestLength:
                shortestLength = len(i)
                shortestString = i

        print(shortestLength)
        print(shortestString)

        for i in range(len(shortestString)):
            for j in strs:
                if j[i] != shortestString[i]:
                    return output
            output += shortestString[i]

        return output

print(Solution.longestCommonPrefix(["cir", "car"]))