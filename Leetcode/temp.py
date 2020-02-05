from typing import List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def rob(self, root: TreeNode) -> int:
        hMap = {}
        res = self.robSub(root, hMap)
        return res
    
    def robSub(self, root: TreeNode, hMap: dict):
        if root == None: return 0
        if root in hMap: return hMap[root]
        
        val = 0
        if root.left:
            val += self.robSub(root.left.left, hMap) + self.robSub(root.left.right, hMap)
        if root.right:
            val += self.robSub(root.right.left, hMap) + self.robSub(root.right.right, hMap)

        val = max(val + root.val, self.robSub(root.left, hMap) + self.robSub(root.right, hMap))
        
        hMap[root] = val
        
        return val
# class Solution:
#     def rob(self, root: TreeNode) -> int:
#         res = self.robSub(root)
#         return max(res[0], res[1])
    
#     def robSub(self, root: TreeNode):
#         if root == None:
#             return [0,0]
        
#         left = self.robSub(root.left)
#         right = self.robSub(root.right)

#         res = [max(left[0], left[1]) + max(right[0], right[1])]
#         res.append(root.val + left[0] + right[0])
        
#         return res

X = Solution()

t             = TreeNode(3)
t.left        = TreeNode(2)
t.right       = TreeNode(3)
t.left.right  = TreeNode(3)
t.right.right = TreeNode(1)
print(X.rob(t))

t             = TreeNode(3)
t.left        = TreeNode(4)
t.right       = TreeNode(5)
t.left.left   = TreeNode(1)
t.left.right  = TreeNode(3)
t.right.right = TreeNode(1)
print(X.rob(t))

t                    = TreeNode(1)
t.left               = TreeNode(0)
t.right              = TreeNode(0)
t.left.left          = TreeNode(1)
t.left.right         = TreeNode(1)
t.right.left         = TreeNode(0)
t.right.right        = TreeNode(0)
t.right.left.left    = TreeNode(1)
t.right.left.right   = TreeNode(1)
t.right.right.left   = TreeNode(1)
t.right.right.right  = TreeNode(1)

print(X.rob(t))