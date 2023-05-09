class Solution(object):
    def twoSum(self, nums, target):

        for i in range(len(nums) - 1):
            if (nums[i] + nums[i + 1] == target):
                print("[", i, ",", i + 1, "]")
                break

    twoSum(Solution, [3, 4, 5, 7], 7)