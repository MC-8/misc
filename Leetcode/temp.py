from typing import List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
class Solution:
    def constructMaximumBinaryTree(self, nums: List[int]) -> TreeNode:
        # Can be optimised avoiding slicing of input vector. Just use indexes
        if nums==[] or nums==None:
            return None
        T = TreeNode(max(nums))
        T.left  = self.constructMaximumBinaryTree(nums[:nums.index(max(nums))])   # [idx 0 to pivot)
        T.right = self.constructMaximumBinaryTree(nums[nums.index(max(nums))+1:]) # (pivot to last]
        return T

X = Solution()
sol = X.constructMaximumBinaryTree([3,2,1,6,0,5])
print(sol)
# Input: [3,2,1,6,0,5]
# Output: return the tree root node representing the following tree:

#       6
#     /   \
#    3     5
#     \    / 
#      2  0   
#        \
#         1

# 1) Find higher value. That is the root.
# 2) left part of array will have all elements to the left of that root
# 3) Right part of array will have all elements to the right of that root
# Apply logic recursively
