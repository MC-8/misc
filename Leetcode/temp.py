class Solution:
    def generateParenthesis(self, n: int) -> [str]:
        T = Tree()
        T.generate_subtree(T.root, 1, 0, n)
        T.backtrack('', T.root, n*2)
        return list(T.solutions)

class Node(object):
    def __init__(self, x: str):
        self.val    = x
        self.left   = None
        self.right  = None

class Tree(object):
    def __init__(self):
        self.root = Node('(')
        self.solutions = set()
    
    def create_node(self, x:str):
        return Node(x)

    def generate_subtree(self, node, opened, closed, depth):
        if depth==opened:
            node.left  = None

        if opened==closed:
            node.right = None

        if opened < depth:
            node.left = Node('(')
            self.generate_subtree(node.left, opened+1, closed, depth)

        if closed < opened:
            node.right = Node(')')
            self.generate_subtree(node.right, opened, closed+1, depth)
    
    def backtrack(self, s, node, length):
        if not node:
            if len(s)==length: 
                self.solutions.add(s)
            return
        s += node.val
        self.backtrack(s, node.left, length)
        self.backtrack(s, node.right, length)

X = Solution()
print(X.generateParenthesis(4))
            



