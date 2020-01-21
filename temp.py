class Solution:
    def spiralOrder(self, matrix):
        out_matrix = []
        M = len(matrix)
        N = len(matrix[0])
        
        # Move right N, N = N-1
        # move down M-1, M = M-1
        # move left N, N = N - 1
        # move up M-1, M = M-1
        # 1   2   3   4
        # 10  11  12  5
        # 9   8   7   6
        r,c = 0,0
        
        c0 = 0
        cend = N
        r0 = 0
        rend = M

        while len(out_matrix) < M*N:
            
            r = r0
            for c in range(c0, cend):
                out_matrix.append(matrix[r][c])
            r0 += 1
            if len(out_matrix) == M*N: return out_matrix
            
            for r in range(r0, rend):
                out_matrix.append(matrix[r][cend-1])
            cend -= 1
            
            if len(out_matrix) == M*N: return out_matrix
            r = rend-1
            for c in range(cend-1, c0-1, -1):
                out_matrix.append(matrix[r][c])
            rend -= 1
            
            if len(out_matrix) == M*N: return out_matrix
            c = c0
            for r in range(rend-1, r0-1, -1):
                out_matrix.append(matrix[r][c])
            c0 += 1
            if len(out_matrix) == M*N: return out_matrix
            
        return out_matrix
        
X = Solution()
# print(X.spiralOrder([[1, 2], [3, 4], [5, 6]]))
s = [
  [1, 2, 3, 4],
  [5, 6, 7, 8],
  [9,10,11,12]
]

print(X.spiralOrder(s))
