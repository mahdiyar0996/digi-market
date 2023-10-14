# # from typing import Tuple
from memory_profiler import profile, memory_usage
# # import tracemalloc
# # class Solution:
# #     # @profile
# #     def twoSum(self, nums: list[int], target: int) -> list[int]:
# #         dist = {}
# #         for i, v in enumerate(nums):
# #             if v in dist:
# #                 return dist[v], i
# #                 # return dist.index(v), i
# #
# #             else:
# #                 dist[i] = v
# #                 # dist.append(target-v)
# #
# #     #please upvote me it would encourage me alot
# #
# #
# # array = [3,2,3, 5 , 7, 7,8,8]
# # s = Solution().twoSum(array,12)
# #
# #
# #
# # class Solution:
# #     def isPalindrome(self, x: int) -> bool:
# #         s = str(x) # convert it to string to avoid negative numbers
# #         return s == s[::-1] # check if s is equal to reversed s
# #
# #
# # s = Solution().isPalindrome(-121)
# # print(s)
# #
# #
# # class Solution:
# #     def romanToInt(self, s: str) -> int:
# #         romanValues = {
# #             'I': 1,
# #             'V': 5,
# #             'X': 10,
# #             'L': 50,
# #             'C': 100,
# #             'D': 500,
# #             'M': 1000
# #         }
# #         result = 0
# #         for i in s:
# #             if i in romanValues.keys():
# #                 result += romanValues[i]
# #         return result
# #
# # s = Solution().romanToInt("MCMXCIV")
# # print(s)
# #
# #
# #
# # class Solution:
# #     def longestCommonPrefix(self, strs: list[str]) -> str:
# #         prefix = ''
# #         if strs[0] == "":
# #             return ""
# #         v = sorted(strs)
# #         first = v[0]
# #         last = v[-1]
# #         for i in range(len(min(first, last))):
# #             if first[i] != last[i]:
# #                 return prefix
# #             prefix += first[i]
# #         return prefix
# #
# # s = Solution().longestCommonPrefix([""])
# # print(s)
# #
# # s = {'name': 1}
# #
# # class Solution:
# #     def mergeTwoLists(self, list1, list2):
# #         result = []
# #         if list2 is not None:
# #             for l1, l2 in zip(list1, list2):
# #                 result.extend([l1, l2])
# #             return sorted(result)
# #
# # s = Solution().mergeTwoLists([1,2,6], [])
# # print(s)
# # class Solution:
# #     # @profile
# #     def removeDuplicates(self, nums: list[int]) -> int:
# #         count = 1
# #         for i in range(1, len(nums)):
# #             if nums[i] != nums[i - 1]:
# #                 nums[i-1] = nums[i]
# #                 count +=1
# #         print(nums)
# #         return count
# # s = Solution().removeDuplicates([1,1,2])
# # print(s)
# # s = 'sadas'
# #
# #
# # class Solution:
# #     def climbStairs(self, n: int) -> int:
# #         if n == 0 or n == 1:
# #             return 1
# #         return self.climbStairs(n - 1) + self.climbStairs(n - 2)
# #
# #
# # s = Solution().climbStairs(3)
# # print(s)
# #
# #
# #
# #
# # def rotate(s, n):
# #     double_string = s + s
# #     if n <= len(s):
# #         return double_string[n:n+len(s)]
# #     else:
# #         return double_string[n-len(s): n]
# #
# # s = rotate('hello', 9)
# # print(s)
# #
# #
# #
# # def search_range(array, number):
# #     result = []
# #     for i, v in enumerate(array):
# #         if v == number:
# #             result.append(i)
# #     if len(result) < 1:
# #         return [None, None]
# #     return [result[0], result[-1]]
# #
# # s = search_range([1,3,3,4,5,7,7], 5)
# #
# # print(s)
# #
# #
# # def binary_search(array, element):
# #     low = 0
# #     high = len(array) - 1
# #
# #     while low <= high:
# #         mid = (high + low) // 2
# #         val = array[mid]
# #         if val == element:
# #             return mid
# #         elif val < element:
# #             low = mid+1
# #         else:
# #             high = mid-1
# #     return None
# #
# #
# # def binary_search(array, element):
# #     low,high = 0, len(array) -1
# #     while low < high:
# #         mid = (high + low) // 2
# #         val = array[mid]
# #         if val == element:
# #             return mid
# #         elif val < element:
# #             low = mid + 1
# #         else:
# #             high = mid -1
# #     return None
# # s = binary_search([1,2,5,8,9], 8)
# # print(s)
# #
# #
# # # Function to rotate string left and right by d length
# #
# #
# #
# # # def rotate(text ,num):
# # #     i = text + text
# # #     # if num > len(i):
# # #         # num = len(i)
# # #     if num <= len(text):
# # #         return i[num: num+len(text)]
# # #     else:
# # #         return i[num-len(text):num]
# # #
# # # s= rotate('hello', 9)
# # # print(s)
# #
#
# class Solution:
#     def searchInsert(self, nums: list[int], target: int) -> int:
#         low, high = 0, len(nums) - 1
#         if target <= nums[0]:
#             return 0
#         elif target > nums[-1]:
#             return high + 1
#         while low <= high:
#             mid = (high + low) // 2
#             if nums[mid] >= target and nums[mid - 1] < target:
#                 break
#             elif nums[mid] < target:
#                 low = mid + 1
#             else:
#                 high = mid - 1
#         return mid
# s = Solution().searchInsert([1,3,5,6], target = 1)
# print(s)
#
#
# # class Solution:
# #     def searchInsert(self, nums: list[int], target: int) -> int:
# #         l=0
# #         r=len(nums)-1
# #         while l<=r:
# #             mid=(l+r)>>1
# #             if nums[mid]==target:
# #                 return mid
# #             elif nums[mid]<target:
# #                 l=mid+1
# #             else:
# #                 r=mid-1
# #         if r==mid:
# #             return mid+1
# #         else:
# #             return mid
# # s = Solution().searchInsert([1,3,5,6], target = 0)
# # print(s)
#
# class Solution:
#     def missingNumber(self, nums: list[int]) -> int:
#         s = [i for i in range(0, len(nums) + 1) if i not in nums]
#         if s:
#             return s[0]
#         return 0
# s = Solution().missingNumber([0,1])
# print(s)
# set().intersection()
#
# # class Solution:
# #     def arrangeCoins(self, n: int) -> int:
# #         table = []
# #         for i in range(0,n):
# #             if not table:
# #                 table.append(i+1)
# #             elif table[i] < table[i+1]:
# #                 return table[i-1]
# # s = Solution().arrangeCoins(8)
# # print(s)
#
#
import time

class Solution:
    @profile
    def intToRoman(self, num: int) -> str:
        s = time.time()
        roman = {
             1000: "M",
             900: "CM",
             500: "D",
             400: "CD",
             100: "C",
             90: "XC",
             50: "L",
             40: "XL",
             10: "X",
             9: "IX",
             5: "V",
             4: "IV",
             1: "I"
        }
        result = ""
        while num > 0:
            for i in roman.keys():
                if num >= i:
                    num -= i
                    result += roman[i]
                    break
        end = time.time()
        print(end-s)
        return result
s = Solution().intToRoman(4220)
print(s)