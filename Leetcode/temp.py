# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        l3 = None
        lh = None
        while l1 or l2:
            if not l2 or (l1 and l1.val < l2.val):
                if l3:
                    l3.next = ListNode(l1.val)
                    l3 = l3.next
                else:
                    l3 = ListNode(l1.val)
                    lh = l3
                l1 = l1.next
            elif l2:
                if l3:
                    l3.next = ListNode(l2.val)
                    l3 = l3.next
                else:
                    l3 = ListNode(l2.val)
                    lh = l3
                l2 = l2.next
        
        return lh

l1 = ListNode(1)
l1.next = ListNode(2)
l1.next.next = ListNode(4)
l2 = ListNode(1)
l2.next = ListNode(3)
l2.next.next = ListNode(4)
x = Solution()
y = x.mergeTwoLists(l1,l2)

while y:
    print(y.val)
    y = y.next