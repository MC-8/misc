""" grid = [[ 1 ,0, 1], [1, 0, 0]]
"""

grid = [[ 1 ,0, 1], [ 1 ,0, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1,1]]

from collections import namedtuple, deque
from typing import List
from itertools import product

def get_number_of_letters(grid: List[List[int]]) -> int:
    result = 0
    if not grid:
        return result
        
    state = namedtuple('state', 'x y')
    have_been = set()

    
    cols = len(grid[0])
    rows = len(grid)
    current_row, current_col = 0, 0
    
    while len(have_been) < cols*rows:
        
        for row, column in product(range(current_row, rows), range(current_col, cols)):
            current_row, current_col = row, col
            
            if grid[row][column] == 1 and state(row, col) not in have_been:
                have_been.add(state(row, col))
                result += 1
                break
            have_been.add(state(row, col))
            
        Q = deque()
        initial_state = state(current_row, current_col)
        Q.append(initial_state)
        have_been.add(initial_state)
        
        while Q:
            s = Q.popleft()
            for dx, dy in ((1,0),(0,1),(-1,0),(0,-1)):
                new_x, new_y = s.x + dx, s.y + dy
                new_state = state(new_x, new_y)
                if grid[new_x][new_y] and (new_state not in have_been) and (0 <= new_x < cols) and (0 <= new_y < rows):
                    Q.append(new_state)
                have_been.add(new_state)
                
    return result            
            
