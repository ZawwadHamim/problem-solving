# Trees (DFS and BFS), in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** Recursion.
**One sentence:** Solve a tree problem by deciding what one node needs from its children (DFS), or by processing it one level at a time (BFS).

## Executive summary
- **DFS (depth-first search):** recursion or an explicit stack. The order decides when you handle the node:
  - **preorder** (node, left, right): the node first, like copying a tree
  - **inorder** (left, node, right): gives a BST in sorted order
  - **postorder** (left, right, node): children first, used for heights and sizes
- **BFS (breadth-first search):** a queue, one level at a time. Use it for level order, right side view, and the minimum depth.
- **The recursive question:** "If I knew the answer for the left and right subtrees, how do I get the answer for this node?" Answer that, then add the base case `if not root`.
- **Two value flows:** values going **down** as parameters (bounds, path sums), and values coming **up** as return values (height, balanced or not).
- **Cost:** O(n) time. O(h) stack space for DFS, where h is the height. O(width) queue space for BFS.

---

## 0. Helpers for local testing
```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(vals):
    """Build from a LeetCode-style level-order list, e.g. [3,9,20,None,None,15,7]."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root
```

## 1. Maximum Depth (LC 104): information flowing up
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```
Trace `[3,9,20,None,None,15,7]`: depth(9) = 1, depth(15) = depth(7) = 1, depth(20) = 2, depth(3) = 1 + max(1, 2) = **3**.

## 2. Traversals: Binary Tree Inorder (LC 94)
Recursive version:
```python
def inorder(root):
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res
```
Iterative version, which interviewers often ask for:
```python
def inorderTraversal(root):
    res, st, cur = [], [], root
    while cur or st:
        while cur:                  # go as far left as possible
            st.append(cur)
            cur = cur.left
        cur = st.pop()              # the leftmost node not yet visited
        res.append(cur.val)
        cur = cur.right             # then its right subtree
    return res
```
For preorder or postorder, move the `append(node.val)` line before or after the recursive calls.

## 3. Invert Binary Tree (LC 226)
```python
def invertTree(root):
    if root:
        root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

## 4. BFS level order (LC 102)
```python
def levelOrder(root):
    if not root:
        return []
    q = deque([root])
    res = []
    while q:
        level = []
        for _ in range(len(q)):     # exactly the nodes of this level
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
```
**Invariant:** at the start of each `while` iteration, the queue holds exactly one full level.
Variations: right side view (LC 199, the last value of each level) and minimum depth (LC 111, the first leaf found by BFS).

## 5. Validate BST (LC 98): information flowing down
```python
def isValidBST(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return (isValidBST(root.left, lo, root.val) and
            isValidBST(root.right, root.val, hi))
```
**The classic bug:** only checking `left.val < node.val < right.val`. Tree `[5,4,6,None,None,3,7]` passes that check, but 3 is in 5's right subtree, so it's invalid. Every node must fit the bounds of **all** its ancestors, which is why the bounds are passed down.
Alternative: an inorder traversal must be strictly increasing.

## 6. Diameter (LC 543): return one thing, track another
```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r)     # the longest path passing through this node
        return 1 + max(l, r)        # what the parent needs
    height(root)
    return best
```
This "return height, update a global best" shape also solves Balanced Binary Tree (LC 110) and Binary Tree Maximum Path Sum (LC 124).

## 7. Lowest Common Ancestor of a BST (LC 235)
```python
def lowestCommonAncestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root             # p and q split here, or one of them is this node
```

## 8. Decision table
| Question | Approach |
|---|---|
| Height, size, balanced, diameter | Postorder DFS: the answer comes up from the children |
| BST valid, path sum from the root | Preorder DFS: pass bounds or a running sum down |
| Sorted output from a BST, k-th smallest | Inorder |
| Level by level, right view, nearest leaf | BFS with a queue |
| Very deep tree (risk of recursion limit) | Iterative with a stack |

## 9. Common bugs
1. A missing `if not root` base case, causing an `AttributeError` on None.
2. BST validation that only compares with the direct children.
3. BFS without the `for _ in range(len(q))` loop, which mixes levels together.
4. Python's recursion limit (about 1000) on a skewed tree. Use an iterative version or `sys.setrecursionlimit`.
5. Collecting paths with `path` instead of `path[:]` (same bug as in backtracking).

## 10. Edge cases
- Empty tree, and a single node
- A completely skewed tree (a linked list in disguise, height n)
- Duplicate values (read the problem's BST rule: `<` or `<=`)
- Negative values in path-sum problems

## 11. Interview prep
- **Purpose:** process hierarchical data by breaking it into subtrees.
- **Control flow:** base case, recurse into the children, combine the results, return. For BFS: queue, level loop, add the children.
- **Complexity:** O(n) time. Space is O(h) for DFS: O(log n) if balanced, O(n) if skewed. O(w) for BFS, where w is the widest level.
- **What a strong candidate says:** "I'll define what each call returns, here the subtree's height. The answer at a node combines its children's heights, and the diameter through a node is left plus right. Each node is visited once, so it's O(n) time and O(h) stack space."
- **Likely follow-ups:** Serialize/Deserialize (LC 297), build a tree from preorder and inorder (LC 105), Kth Smallest in a BST (LC 230), LCA of a general binary tree (LC 236).
