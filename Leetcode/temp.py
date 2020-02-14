# Definition for a binary tree node.
from typing import List
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        res = []
        if root:
            res += self.inorderTraversal(root.left)
            res.append(root.val)
            res += self.inorderTraversal(root.right)
        return res

input = [1, None, 2, 3]

tree = TreeNode(1)
tree.left = None
tree.right = TreeNode(2)
tree.right.left = TreeNode(3)

X = Solution()
print(X.inorderTraversal(tree))