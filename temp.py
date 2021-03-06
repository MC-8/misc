# 64. Minimum path sum
from collections import deque, namedtuple
from typing import List, Union
from copy import deepcopy
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> Union[int, None]:
        Q = deque()

        state = namedtuple('state', 'coord sumpath')

        initial_state = state((0,0), [grid[0][0]])
        best_solution = float('inf')
        Q.append(initial_state)

        ymax = len(grid[0])-1
        xmax = len(grid)-1

        while Q:
            s = Q.pop()
            x,y = s.coord
            
            if (new_x := x + 1) <= xmax:
                np = deepcopy(s.sumpath)
                np.append(grid[new_x][y])
                if sum(s.sumpath) < best_solution: 
                    Q.append(state((new_x, y), np))

            if (new_y := y + 1) <= ymax:
                np = deepcopy(s.sumpath)
                np.append(grid[x][new_y])
                if sum(s.sumpath) < best_solution: 
                    Q.append(state((x, new_y), np))

            if (x,y)==(xmax,ymax):
                sol = sum(s.sumpath)
                if sol < best_solution:
                    best_solution = sol

        return int(best_solution)

grid = [
  [1,3,1],
  [1,5,1],
  [4,2,1]
]

grid = [[1,2,5],[3,2,1]]

X = Solution()
print(X.topKFrequent([3,3,2,3,5,2,7],1))
print(X.topKFrequent([3,3,2,3,5,2,7],2))
from queue import Empty
