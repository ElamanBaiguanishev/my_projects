from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head

        while curr and curr.next:
            if curr.val == curr.next.val:
                curr.next = curr.next.next
            else:
                curr = curr.next

        return head


solution = Solution()

result = solution.deleteDuplicates(
    ListNode(1, ListNode(1, ListNode(2, ListNode(3, ListNode(3, ListNode(3, ListNode(4, ListNode(4)))))))))

while result:
    print(result.val, end=" ")
    result = result.next
