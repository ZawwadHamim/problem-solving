# Two pointers, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** Squeeze.
**One sentence:** Two indices move through the array under a rule that lets you discard one element per step for sure, turning an O(n²) pair search into O(n).

## Executive summary
- **Opposite ends:** `i` starts left and `j` starts right, and they move toward each other. Used for sorted pair sums, palindromes and Container With Most Water.
- **Same direction (read/write):** a fast reader and a slow writer. Used for removing duplicates, moving zeroes and in-place filtering.
- **Fast/slow on linked lists:** cycle detection and finding the middle. See `linkedList/theory.md`.
- **Why it works:** every move must be provably safe. You only drop an element when no answer can use it. That argument is what the interviewer wants to hear.
- **Cost:** O(n) time and O(1) space, plus O(n log n) if you have to sort first.

---

## 1. Opposite ends: Two Sum II, sorted input (LC 167)
```python
def twoSumSorted(numbers, target):
    i, j = 0, len(numbers) - 1
    while i < j:
        s = numbers[i] + numbers[j]
        if s == target:
            return [i + 1, j + 1]      # LC 167 is 1-indexed
        if s < target:
            i += 1                     # need a bigger sum, and numbers[i] is too small with every j
        else:
            j -= 1                     # need a smaller sum, and numbers[j] is too big with every i
    return []
```
Trace `[2, 7, 11, 15]`, target 9: (0,3: 17 > 9, j = 2), (0,2: 13 > 9, j = 1), (0,1: 9, return [1, 2]).

**Invariant:** if an answer exists, it uses indices inside `[i, j]`.
**Why moving `i` is safe:** if `numbers[i] + numbers[j] < target`, then `numbers[i]` plus any element left of `j` is even smaller, because the array is sorted. So `numbers[i]` can't be in any answer and can be dropped.

## 2. Opposite ends: Valid Palindrome (LC 125)
```python
def isPalindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1
        elif not s[j].isalnum():
            j -= 1
        elif s[i].lower() != s[j].lower():
            return False
        else:
            i += 1
            j -= 1
    return True
```
- O(n) time and O(1) space. The one-liner `t = [c.lower() for c in s if c.isalnum()]; return t == t[::-1]` is O(n) space.
- **Follow-up, LC 680 "delete at most one character":** at the first mismatch, try skipping `i` or skipping `j` and check whether the rest is a palindrome.

## 3. Opposite ends: Container With Most Water (LC 11)
```python
def maxArea(height):
    i, j = 0, len(height) - 1
    best = 0
    while i < j:
        best = max(best, (j - i) * min(height[i], height[j]))
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
    return best
```
**Why moving the shorter line is safe:** say `height[i]` is the shorter one. Any other container using line `i` has a smaller width, and its height is still at most `height[i]`. So none of them can beat the area just measured, and line `i` can be dropped.

## 4. Fix one element, two-pointer the rest: 3Sum (LC 15)
```python
def threeSum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue                    # skip a repeated first value
        if nums[i] > 0:
            break                       # everything after is positive too
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1              # skip a repeated second value
    return res
```
- O(n²) time, and O(1) extra space apart from the output.
- **Skipping duplicates is the whole difficulty.** Skip at the outer level (`nums[i] == nums[i-1]`) and at the inner level after a match.

## 5. Same direction: read and write pointers
Remove Duplicates from Sorted Array (LC 26):
```python
def removeDuplicates(nums):
    w = 1                               # nums[0:w] holds the unique values so far
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:
            nums[w] = nums[r]
            w += 1
    return w
```
Move Zeroes (LC 283):
```python
def moveZeroes(nums):
    w = 0                               # nums[0:w] holds the non-zeros in their original order
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[w], nums[r] = nums[r], nums[w]
            w += 1
```
**Invariant:** everything before `w` is final. `r` only looks ahead.

## 6. Decision table
| Signal | Variant |
|---|---|
| Sorted array, find a pair or triple with a sum | Opposite ends (fix one element for 3Sum) |
| Symmetry: palindrome, reversing in place | Opposite ends |
| Maximize something set by the two ends (area, width) | Opposite ends, move the weaker side |
| In-place filter, dedupe or compact | Same direction, read and write |
| Cycle, middle, k-th from the end in a list | Fast and slow (see `linkedList/`) |
| Unsorted, and you need the original indices | Hash map instead (see `hashmap/`) |

## 7. Common bugs
1. `while i <= j` when a pair must use two different elements. Use `i < j`.
2. Forgetting to move a pointer after a match, which loops forever.
3. 3Sum duplicates: skipping before the first use (`nums[i] == nums[i+1]`) loses valid triples. Compare with the previous element instead.
4. Two pointers on unsorted data for a sum problem. The discard argument needs sorted input.
5. Returning 0-based indices when the problem is 1-based (LC 167).

## 8. Edge cases
- Length 0, 1 and 2
- All duplicates, e.g. `[0,0,0,0]` for 3Sum should return one triple
- Negative numbers
- Strings with only punctuation for LC 125 should return True

## 9. Interview prep
- **Purpose:** examine pairs without checking all of them, by using order to discard candidates.
- **Control flow:** start the pointers, compare, move exactly the pointer that the discard rule allows, and stop when they meet.
- **Trade-offs:** needs sorted input or a monotonic structure. Sorting loses the original indices, so keep `(value, index)` pairs if you need them. Compared with a hash map, it uses less memory (O(1)) but takes more time if you have to sort.
- **What a strong candidate says:** "The array is sorted, so if the sum is too small, the left element can't work with anything, and I can drop it. Every step drops one element, so it's O(n) with O(1) space."
- **Likely follow-ups:** 3Sum Closest (LC 16), 4Sum (LC 18, fix two elements), Trapping Rain Water (LC 42, move the side with the lower max), "what if there are duplicates?"
