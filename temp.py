from typing import List
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        D = {}
        for n in nums:
            D[n] = D.get(n,0) + 1
        res = []
        for key, _ in sorted(D.items(), key=lambda v:v[1], reverse=True):
            res.append(key)
            if len(res)>=k:
                break
        return res

X = Solution()
print(X.topKFrequent([3,3,2,3,5,2,7],1))
print(X.topKFrequent([3,3,2,3,5,2,7],2))
