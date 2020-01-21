from typing import List
from collections import deque
from itertools import product
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        solution_set = set()
        couples_set = set()
        x_set = set()
        idx = 0
        D = {}
        for i in range(len(nums)):
            D[nums[i]] = D.get(nums[i],0) + 1
        while idx < len(nums)-2:
            idy = idx+1
            x = nums[idx]
            if x in x_set:
                idx+=1
                continue
            while idy < len(nums)-1:
                y = nums[idy]
                if (x,y) in couples_set or (y,x) in couples_set:
                    idy+=1
                    continue
                z = -(x+y)
                if ((z in D and ((z != x) and (z != y))) or 
                   (((z==x) and (z==y)) and D.get(z)>2) or
                   (((z==x) and (z!=y)) and D.get(z)>1) or 
                   (((z!=x) and (z==y)) and D.get(z)>1)):
                    sol = tuple(sorted([x,y,z]))
                    couples_set.add((x,y))
                    solution_set.add(sol)
                    x_set.add(x)
                idy+=1
            idx+=1
            
        return [list(x) for x in solution_set]    

t1 = [-1, 0, 1, 2, -1, -4]
X = Solution()
print(X.threeSum(t1))

t2 = [-2,0,0,2,2]
print(X.threeSum(t2))
