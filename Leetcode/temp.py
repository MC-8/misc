
class Solution:
    def isValid(self, s: str) -> bool:
        D = {'(':')',
             '[':']',
             '{':'}'}
        from collections import deque
        S = deque()
        for c in s:
            if c in D:
                S.append(D[c])
            else:
                if len(S)==0 or not S.pop()==c:
                    return False
        if len(S)==0:
            return True
        else:
            return False


X = Solution()
print(X.isValid('()[]'))
print(X.isValid('([)]]'))