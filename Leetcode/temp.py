from typing import List
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        iteration = len(matrix)
        m = matrix
        while iteration < n//2:
            for j in range(iteration, n-1-iteration, 1): #0->3 | 1
                i = iteration
                print((i,j))
                t1 = m[i][j]   # source
                for _ in range(4):
                    # print((i,j))
                    t2 = m[j][n-i-1] # save destination
                    i, j = j, n-i-1
                    m[i][j] = t1   # replace
                    t1 = t2        # source is the saved value
                print(m)
            iteration+=1
        pass

X = Solution()

m1 = [
  [1,2,3],
  [4,5,6],
  [7,8,9]
]
# t1 = m1[i][j]
# t2 = m1[j][n-i]
# m[j][n-i] = t1
# i = j
# j = n-i
m2 = [
  [ 5, 1, 9,11],
  [ 2, 4, 8,10],
  [13, 3, 6, 7],
  [15,14,12,16]
]
m = m2
n = 4
from itertools import product

iteration = 0
# (0,0), (0,1), (1,1)
# (0,0), (0,1), (0,2), (0,3), (1,1), (1,2)

# 7 4 1
# 8 5 2
# 9 6 3
# r1c1 -> r1c3
# r1c2 -> r2c3
# r1c3 -> r3c3

# r2c1 -> r1c2
# r2c2 -> r2c2
# r2c3 -> r3c2

# r3c1 -> r1c1
# r3c2 -> r2c1
# r3c3 -> r3c1
# i, j # row, columns

# i, j -> j, n-i

# X.rotate(m1)
# print(m1)

# m2 = [
#   [ 5, 1, 9,11],
#   [ 2, 4, 8,10],
#   [13, 3, 6, 7],
#   [15,14,12,16]
# ]
# X.rotate(m2)
# print(m2)
