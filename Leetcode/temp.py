from typing import List
from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        D = {}
        for x in strs:
            print(x)
            D.setdefault(''.join(sorted(x)),[]).append(x)
        return list(D.values())

X = Solution()

print(X.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# Input: 
# Output:
# [
#   ["ate","eat","tea"],
#   ["nat","tan"],
#   ["bat"]
# ]
# 1 create a dictionary where keys are sorted elements, 
# 2 value is list of entries (unsorted string)


