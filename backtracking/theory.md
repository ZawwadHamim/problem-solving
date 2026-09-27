# Backtracking, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** Explore.
**One sentence:** Build an answer one choice at a time: make a choice, go deeper, then undo the choice, so you visit every possible answer exactly once.

## Executive summary
- **The decision tree:** each level is one decision. Each branch is one option. Each leaf is one complete answer.
- **The three steps:** **choose** (add to `path`), **explore** (recurse), **un-choose** (`path.pop()`).
- **Three kinds of problem:**
  - **subsets:** each element is in or out, giving 2ⁿ answers
  - **permutations:** order matters, giving n! answers
  - **combinations / combination sum:** order doesn't matter, so use a `start` index so you never look back
- **Duplicates in the input:** sort, then skip `nums[i] == nums[i-1]` at the same level of the tree.
- **Pruning:** stop a branch early when it can't lead to a valid answer. That's what makes backtracking fast enough in practice.
- **Always append `path[:]`,** a copy, never `path` itself.

---

## 1. The template
```python
def backtrack_template(choices):
    res = []
    path = []
    def dfs(state):
        if is_complete(state):
            res.append(path[:])          # copy!
            return
        for choice in options(state):
            if not valid(choice):
                continue                 # prune
            path.append(choice)          # choose
            dfs(next_state(state, choice))   # explore
            path.pop()                   # un-choose
    dfs(initial_state)
    return res
```
(This is a shape to follow, not runnable code. The problems below fill it in.)

## 2. Subsets (LC 78): include or exclude
```python
def subsets(nums):
    res, path = [], []
    def dfs(i):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i])             # include nums[i]
        dfs(i + 1)
        path.pop()
        dfs(i + 1)                       # exclude nums[i]
    dfs(0)
    return res
```
Decision tree for `[1, 2]`:
```
                 dfs(0) []
           /                  \
     take 1 → [1]           skip 1 → []
       /        \             /        \
  [1,2]        [1]         [2]         []
```
Leaves in order: `[1,2], [1], [2], []`. That's 2² = 4 subsets.
**Why `path[:]`:** `path` is one list that keeps changing. Appending the list itself would leave `res` full of references to the same list, which is empty by the end.

## 3. Permutations (LC 46): track what's used
```python
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)
    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False              # undo BOTH changes
    dfs()
    return res
```
n! permutations, each copied in O(n), so O(n · n!).

## 4. Combination Sum (LC 39): reuse allowed, use a start index
```python
def combinationSum(candidates, target):
    res, path = [], []
    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                continue                 # prune (with sorted input you could break)
            path.append(candidates[i])
            dfs(i, remain - candidates[i])   # i, not i + 1: the same number can be reused
            path.pop()
    dfs(0, target)
    return res
```
**Why `start`:** without it, `[2,3]` and `[3,2]` would both be produced. Only moving forward means each combination is produced in exactly one order.
- Each number usable **once** (LC 40): recurse with `i + 1` and skip duplicates (section 5).

## 5. Subsets II (LC 90): duplicates in the input
```python
def subsetsWithDup(nums):
    nums.sort()                          # duplicates next to each other
    res, path = [], []
    def dfs(start):
        res.append(path[:])              # every node is a subset
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                 # same value at the same level would repeat a subset
            path.append(nums[i])
            dfs(i + 1)
            path.pop()
    dfs(0)
    return res
```
`[1,2,2]` gives `[], [1], [1,2], [1,2,2], [2], [2,2]`. The second `[2]` and `[1,2]` are skipped.
**Why `i > start` and not `i > 0`:** you may use a second 2 deeper in the same branch (`[2,2]`). You just can't start a sibling branch with the same value.

## 6. Word Search (LC 79): backtracking on a grid
```python
def exist(board, word):
    m, n = len(board), len(board[0])
    def dfs(r, c, k):
        if k == len(word):
            return True
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
            return False
        tmp, board[r][c] = board[r][c], '#'          # mark as visited (choose)
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or
                 dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = tmp                            # restore (un-choose)
        return found
    return any(dfs(r, c, 0) for r in range(m) for c in range(n))
```

## 7. Complexity cheat sheet
| Problem | Number of answers | Time |
|---|---|---|
| Subsets | 2ⁿ | O(n · 2ⁿ) |
| Permutations | n! | O(n · n!) |
| Combinations C(n, k) | C(n, k) | O(k · C(n, k)) |
| Grid word search | — | O(m·n·4ᴸ), where L is the word length |

These are exponential **because the output itself is exponential**. You can't do better than the size of the answer. Say that in the interview.

## 8. Decision table
| Signal | Variant |
|---|---|
| "All subsets", "power set" | include/exclude, or a loop from `start` |
| "All orderings", "arrangements" | `used[]` array |
| "All combinations that sum to…" | `start` index, and `i` or `i+1` depending on reuse |
| Input has duplicates | sort, and skip `i > start and nums[i] == nums[i-1]` |
| Path in a grid | mark the cell, recurse in 4 directions, unmark |
| Only need the **count** or **best**, not every answer | probably DP (see `dp/theory.md`) |

## 9. Common bugs
1. `res.append(path)` instead of `path[:]`.
2. Forgetting to undo the choice (`path.pop()`, `used[i] = False`, restoring the grid cell).
3. `i > 0` instead of `i > start` when skipping duplicates.
4. Recursing with `i + 1` when reuse is allowed, or with `i` when it isn't.
5. No pruning, so the solution times out on large targets.

## 10. Edge cases
- Empty input: subsets should return `[[]]`
- Target 0, and no valid combination
- All elements equal
- A word longer than the grid has cells

## 11. Interview prep
- **Purpose:** list every valid configuration when the problem really needs all of them.
- **Control flow:** a recursive function with `path`. Base case: record a copy. Otherwise, loop over the options: choose, recurse, un-choose.
- **Complexity:** set by the number of answers. Say "O(n · 2ⁿ), which matches the output size".
- **What a strong candidate says:** "It's a decision tree. At each index I take or skip the element. I record a copy of the path at the leaves and undo each choice on the way back up. To avoid duplicate subsets, I sort and skip equal values at the same depth."
- **Likely follow-ups:** N-Queens (LC 51), Palindrome Partitioning (LC 131), Letter Combinations of a Phone Number (LC 17), Generate Parentheses (LC 22). Also "can you just count them?", which usually means DP.
- See also `../recursion/` for your earlier recursion practice.
