from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# class Solution:
#     def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
#         result = []
#
#         def traverse(node):
#             if node:
#                 traverse(node.left)
#                 result.append(node.val)
#                 traverse(node.right)
#
#         traverse(root)
#
#         return result


# Создаем бинарное дерево:       1
#                               / \
#                              2   3
#                             / \
#                            4   5


# class Solution:
#     def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
#         def traverse(node1, node2):
#             if node1 and node2:
#                 if node1.val == node2.val:
#                     return traverse(node1.left, node2.left) and traverse(node1.right, node2.right)
#                 else:
#                     return False
#             elif not node1 and not node2:
#                 return True
#             else:
#                 return False
#
#         return traverse(p, q)

# class Solution:
#     def isSymmetric(self, root: Optional[TreeNode]) -> bool:
#         def traverse(left: Optional[TreeNode], right: Optional[TreeNode]):
#             if left and right:
#                 if left.val == right.val:
#                     return traverse(left.left, right.right) and traverse(left.right, right.left)
#                 else:
#                     return False
#             elif not left and not right:
#                 return True
#             else:
#                 return False
#
#         if not root:
#             return True
#
#         return traverse(root.left, root.right)


# class Solution:
#     def maxDepth(self, root: Optional[TreeNode]) -> int:
#         if not root:
#             return 0
#
#         max_depth = 0
#         stack = [(root, 1)]
#
#         while stack:
#             current, depth = stack.pop()
#             print(current.val)
#             max_depth = max(max_depth, depth)
#
#             if current.right:
#                 stack.append((current.right, depth + 1))
#             if current.left:
#                 stack.append((current.left, depth + 1))
#
#         return max_depth

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        n = len(nums)

        if not n:
            return None

        mid = (n - 1) // 2
        root = TreeNode(nums[mid])

        root.left = (self.sortedArrayToBST(nums[:mid]))
        root.right = (self.sortedArrayToBST(nums[mid + 1:]))

        return root


solution = Solution()

root = TreeNode(val=3)
root.left = TreeNode(val=9)
root.right = TreeNode(val=2, left=TreeNode(15), right=TreeNode(7))

nums = [-10, -3, 0, 5, 9]

result = solution.sortedArrayToBST(nums)

while result:
    print(f"{result.val}")
    result = result.left
