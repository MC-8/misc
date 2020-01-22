from typing import Counter, List
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        zflag = False
        counter = 0
        for x in nums[-2::-1]:
            if zflag and (x>0 and x>counter):
                zflag = False
            if x==0 and not zflag:
                zflag = True
            counter = counter + 1 if zflag else 0

        return not zflag


X = Solution()
print(X.canJump([2,3,1,1,4]))
print(X.canJump([3,2,1,0,4]))
print(X.canJump([2,0,0]))




# 1 start from the end
# If I find one or more zeros, keep looking until you find a value that is N#zeros+1,
# if reach beginning without finding it return false
# No zeros, end reachable