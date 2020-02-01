from typing import List
class Solution:
    def countBits(self, num: int) -> List[int]:
        arr = [0]*(num+1)
        i=1
        idx = 0
        ipass = 1
        while i <= num:
            arr[i] = arr[idx] + 1
            i+=1
            idx+=1
            if idx>=ipass: 
                idx = 0
                ipass *= 2
        return arr

X = Solution()
print(X.countBits(2))
print("---------")
print(X.countBits(5))
print("---------")
print(X.countBits(16))

