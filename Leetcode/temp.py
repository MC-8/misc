from typing import List

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        result = []
        
        return result

n = 10
edges = [[0, 3], [1, 3], [2, 3], [4, 3], [5, 4],[2,8],[2,7],[7,9]]

# values that share one node are at the same height
# aim for distance root to node = n - shared edges (TBD) (Hypotesis)

# Cut all leafs.
# Repeat until you have exactly 2 or 1 nodes
from collections import defaultdict
H = defaultdict(int)
for edge in edges:
    H[edge[0]] += 1
    H[edge[1]] += 1

from copy import deepcopy
working_edges = deepcopy(edges)

to_remove = []

for (key, value) in list(H.items()):
    if value==1:
        to_remove.append(key)

for rem in to_remove:
     for edge in working_edges:
         if rem in edge:
             working_edges.remove(edge)
print(working_edges)
print(H)