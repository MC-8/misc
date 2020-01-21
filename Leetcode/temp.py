from typing import List
from collections import deque
from itertools import product
class Solution:
    def numIslands(self, grid: List[str]) -> int:
        if grid == []: return 0
        S = set()
        x,y = 0,0
        Q = deque()
        land_counter = 0
        for xx,yy in product(range(len(grid)), range(len(grid[0]))):
            
            if (xx,yy) in S: continue # We already visited this cell
            if grid[xx][yy] == '1': # land!
                land_counter += 1
                Q.append((xx,yy))
                while(Q):
                    x,y = Q.popleft()
                    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]): continue # Out of bounds
                    if (x,y) in S: continue # If we have already visited this cell
                    S.add((x,y))            # Visit the cell
                    if grid[x][y] == '0': continue # If it's water, stop expanding visit
                    for dx,dy in [(0,1), (1,0), (-1,0), (0,-1)]: # Otherwise we are on a landmass, so keep exploring
                        Q.append((x+dx, y+dy))
            else:
                S.add((xx,yy)) # Just mark the cell as visited
        return land_counter    

X = Solution()
t1 = ['11110',
      '11010',
      '11000',
      '00000'] # One land

t2 = ['11000',
      '11000',
      '00100',
      '00011'] # Three lands

print("T1")
print(X.numIslands(t1))
print("T2")
print(X.numIslands(t2))
