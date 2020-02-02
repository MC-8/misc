from typing import List
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        return sorted(nums)[-k]

X = Solution()

print(X.findKthLargest( [3,2,3,1,2,4,5,5,6],4))
print(X.findKthLargest( [3,2,3,1,2,4,5,5,6],4))