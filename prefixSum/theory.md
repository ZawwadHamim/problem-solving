# Prefix sum, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved: 238
- Mistake and correction:

---

**One word:** Accumulate.
**One sentence:** Precompute running totals once, so the sum of any range becomes one subtraction instead of a loop.

## Executive summary
- **Definition:** `P[0] = 0` and `P[i+1] = P[i] + nums[i]`. So `P[i]` is the sum of the first i elements.
- **Range sum:** `sum(nums[l..r]) = P[r+1] - P[l]`, in O(1) after an O(n) build.
- **The big trick:** "subarray sum equals k" becomes "find an earlier prefix equal to `current - k`", which a hash map answers. It works with negative numbers, where a sliding window fails.
- **Related ideas:** prefix products (LC 238), 2-D prefix sums, difference arrays (for range updates), and prefix XOR.

---

## 1. Build and query
```python
def build_prefix(nums):
    P = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        P[i + 1] = P[i] + x
    return P

def range_sum(P, l, r):                  # inclusive l..r
    return P[r + 1] - P[l]
```
Example: `nums = [3, 1, 4, 1, 5]` gives `P = [0, 3, 4, 8, 9, 14]`. Then `sum(nums[1..3]) = P[4] - P[1] = 9 - 3 = 6`, which checks out: 1 + 4 + 1.
**Why the extra leading 0:** it makes ranges that start at index 0 work with no special case. `sum(nums[0..r]) = P[r+1] - P[0]`.
`itertools.accumulate(nums, initial=0)` builds the same list.

## 2. Find Pivot Index (LC 724)
The pivot is where the left sum equals the right sum. The right sum is `total - left - nums[i]`.
```python
def pivotIndex(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1
```
Trace `[1, 7, 3, 6, 5, 6]`, total 28:
| i | x | left | right = 28 − left − x | equal? |
|---|---|---|---|---|
| 0 | 1 | 0 | 27 | no |
| 1 | 7 | 1 | 20 | no |
| 2 | 3 | 8 | 17 | no |
| 3 | 6 | 11 | 11 | **yes, return 3** |

## 3. Subarray Sum Equals K (LC 560): prefix sum plus a hash map
A subarray `nums[j..i]` sums to k exactly when `P[i+1] - P[j] = k`, which means `P[j] = P[i+1] - k`. So for each position, count how many earlier prefixes equal `current - k`.
```python
def subarraySum(nums, k):
    count = {0: 1}                      # the empty prefix, for subarrays starting at index 0
    s = 0
    res = 0
    for x in nums:
        s += x
        res += count.get(s - k, 0)
        count[s] = count.get(s, 0) + 1
    return res
```
Trace `[1, 1, 1]`, k = 2:
| x | s | need s−k | count before | res |
|---|---|---|---|---|
| 1 | 1 | −1 | {0:1} | 0 |
| 1 | 2 | 0 | {0:1, 1:1} | 1 |
| 1 | 3 | 1 | {0:1, 1:1, 2:1} | 2 |

- **Why `{0: 1}`:** without it, a subarray that starts at index 0 is never counted.
- **Why look up before storing:** otherwise, with k = 0, a prefix would match itself and count an empty subarray.
- **Why not a sliding window:** with negative numbers, growing the window doesn't always make the sum bigger, so the shrink rule breaks.

## 4. Contiguous Array (LC 525): turning a count into a sum
Longest subarray with equally many 0s and 1s. Treat 0 as −1, so the question becomes "longest subarray with sum 0". Store the **first** index each prefix sum was seen.
```python
def findMaxLength(nums):
    first = {0: -1}
    s = 0
    best = 0
    for i, x in enumerate(nums):
        s += 1 if x == 1 else -1
        if s in first:
            best = max(best, i - first[s])
        else:
            first[s] = i                # keep the earliest index, which gives the longest span
    return best
```

## 5. Prefix and suffix products: Product of Array Except Self (LC 238)
```python
def productExceptSelf(nums):
    n = len(nums)
    res = [1] * n
    pre = 1
    for i in range(n):                  # res[i] = product of everything left of i
        res[i] = pre
        pre *= nums[i]
    suf = 1
    for i in range(n - 1, -1, -1):      # multiply in the product of everything right of i
        res[i] *= suf
        suf *= nums[i]
    return res
```
O(n) time, O(1) extra space apart from the output, and no division, so zeros are handled.

## 6. 2-D prefix sum (Range Sum Query 2D, LC 304)
`P[r+1][c+1]` is the sum of the rectangle from `(0,0)` to `(r,c)`.
- Build: `P[r+1][c+1] = grid[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]`
- Query the rectangle `(r1,c1)` to `(r2,c2)`: `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`

This is inclusion and exclusion: subtract the two strips, then add back the corner that was subtracted twice.

## 7. Difference array (range updates)
To add `v` to every element of `nums[l..r]` many times, record the updates, then build once:
```python
diff = [0] * (n + 1)
diff[l] += v
diff[r + 1] -= v
# afterwards: running sum of diff gives the total added at each index
```
Each update is O(1), and one O(n) pass applies them all. Used in Car Pooling (LC 1094) and Corporate Flight Bookings (LC 1109).

## 8. Decision table
| Question | Tool |
|---|---|
| Many range-sum queries on fixed data | Prefix array |
| Count or length of subarrays with sum = k (negatives allowed) | Prefix sum + hash map |
| Longest subarray with a balanced count | Map each value to ±1, then prefix sum + first-seen map |
| Product of everything except self | Prefix and suffix products |
| Many range updates, then read | Difference array |
| Sum of a rectangle | 2-D prefix sum |
| Data changes between queries | Fenwick tree or segment tree (outside this roadmap) |

## 9. Common bugs
1. Forgetting the leading 0, then special-casing `l = 0` and getting it wrong.
2. Off-by-one: the range `[l, r]` is `P[r+1] - P[l]`, not `P[r] - P[l]`.
3. LC 560: storing the current prefix before looking it up.
4. LC 525: overwriting the first-seen index, which shrinks the answer.
5. Using a sliding window when the input has negative numbers.

## 10. Edge cases
- Empty array, and a single element
- k = 0, and all zeros (LC 560 with `[0,0,0]` and k = 0 should give 6)
- Negative numbers
- A pivot at index 0 or n−1

## 11. Interview prep
- **Purpose:** replace repeated range loops with O(1) subtraction after an O(n) setup.
- **Control flow:** one pass to build or keep a running sum. For counting questions, look up `current - k` in a map, then record `current`.
- **Complexity:** O(n) time. O(n) space for the array or map, or O(1) for a single running total.
- **What a strong candidate says:** "A subarray sum is the difference of two prefix sums, so 'sum equals k' means 'an earlier prefix equals the current one minus k'. A hash map of prefix counts makes it O(n), and it works with negative numbers, where a sliding window wouldn't."
- **Likely follow-ups:** Continuous Subarray Sum (LC 523, prefix mod k), Subarray Sums Divisible by K (LC 974), "what if the array changes?" (Fenwick tree).
