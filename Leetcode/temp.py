from typing import List
from itertools import product
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        valid = True
        
        # Do cells
        for csr, csc in product(range(0, 7, 3), range(0, 7, 3)):
            S = set()
            # Add values
            num_counter = 0
            for dr, dc in product(range(3), range(3)):
                if (val := board[csr+dr][csc+dc]) != ".":
                    S.add(int(val))
                    num_counter += 1
            if len(S)!=num_counter: return False
            
        # Do rows
        for csr in range(9):
            S = set()
            # Add values
            num_counter = 0
            for dc in range(9):
                if (val := board[csr][dc]) != ".":
                    S.add(int(val))
                    num_counter += 1
            if len(S)!=num_counter: return False
        
        # Do columns
        for csc in range(9):
            S = set()
            # Add values
            num_counter = 0
            for dr in range(9):
                if (val := board[dr][csc]) != ".":
                    S.add(int(val))
                    num_counter += 1
            if len(S)!=num_counter: return False
        
        return valid