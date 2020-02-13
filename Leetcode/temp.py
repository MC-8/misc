from typing import List
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        sol = []
        N = len(nums)
        for idx in range(2**N):
            sol.append([])
            for n_bit in range(N):
                if idx & (1 << n_bit):
                    sol[idx].append(nums[n_bit])
        return sol

X = Solution()

print(X.subsets([1,2,3]))