# Binary search, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved: 704, 35, 34 (accepted 2026-09-26/27)
- Mistake and correction:

---

**One word:** Halving.
**One sentence:** Binary search keeps a window that is guaranteed to contain the answer and throws away half of it on every step, so it finishes in O(log n).

## Executive summary
- **The window:** `lo` and `hi` bound where the answer can still be. `mid` is the probe.
- **The invariant:** "if the answer exists, it is inside the window." Every move must keep this true.
- **Why O(log n):** the window size goes n, n/2, n/4 … 1. That is about log₂ n steps, so 10⁹ items takes about 30 probes.
- **What you modify:** four knobs. The window style (closed or half-open), the loop condition, how `lo`/`hi` move, and what you return. Each knob follows from the question you ask at `mid`.
- **Two pointers is different:** pointers step by one, so it is O(n). Use it for pairs, palindromes and partitions.

---

## 1. The core template (exact match)
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1        # closed window [lo, hi]
    while lo <= hi:                  # window non-empty
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1             # mid and everything left is too small
        else:
            hi = mid - 1             # mid and everything right is too big
    return -1
```
**Trace** on `[1, 3, 5, 7, 9, 11]`, target 9:
| step | lo | hi | mid | nums[mid] | action |
|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 | 5 | 5 < 9, lo = 3 |
| 2 | 3 | 5 | 4 | 9 | found, return 4 |

Target 4 (missing): (0,5,mid 2 → 5>4, hi=1), (0,1,mid 0 → 1<4, lo=1), (1,1,mid 1 → 3<4, lo=2). Now lo=2 > hi=1, the window is empty, return -1. Notice lo stopped at 2, which is exactly where 4 would be inserted. That fact powers the lower-bound variant.

## 2. Why it is correct
- **Initialization:** the window is the whole array, so the invariant holds.
- **Maintenance:** the array is sorted. If `nums[mid] < target`, every index ≤ mid is also < target, so dropping them loses nothing. Same logic on the right.
- **Progress:** each step removes at least `mid` itself, so the window strictly shrinks. No infinite loop.
- **Termination:** the loop ends when the window is empty. By the invariant, the target is not in the array.

## 3. Why O(log n), precisely
After k steps the window has at most n / 2ᵏ elements. It becomes empty once 2ᵏ > n, so k ≈ ⌊log₂ n⌋ + 1. Space is O(1) iteratively, O(log n) if written recursively. It matches the comparison lower bound: any comparison search needs Ω(log n) probes, because a decision tree with n leaves has depth at least log₂ n.

## 4. The four knobs, and when to change each

### Knob A: closed `[lo, hi]` vs half-open `[lo, hi)`
- **Closed** (`hi = n - 1`): use when you are looking for an exact element and may return from inside the loop.
- **Half-open** (`hi = n`): use when the answer may be "one past the end", like an insertion point. `hi = n` is a legal answer.
- **Rule:** the initial `hi` defines the window, and every other knob must agree with it.

### Knob B: `while lo <= hi` vs `while lo < hi`
- **`lo <= hi`** goes with closed windows. The loop runs while at least one element remains, and you exit with `lo = hi + 1`.
- **`lo < hi`** goes with "shrink until one candidate remains". You exit with `lo == hi`, which is the answer. Use it for lower bound, peak finding and minimum in a rotated array.
- **Bug:** pairing `lo < hi` with `hi = mid - 1` skips checking the last element.

### Knob C: how `lo` and `hi` move
Ask: "can `mid` itself still be the answer?"
- **No, mid is ruled out** → `lo = mid + 1` or `hi = mid - 1`.
- **Yes, mid may be the answer** → keep it: `hi = mid` (answer is at mid or left) or `lo = mid` (answer is at mid or right).
- **Danger with `lo = mid`:** when `hi = lo + 1`, the default mid equals lo and the loop never moves. Fix it by rounding mid up: `mid = lo + (hi - lo + 1) // 2`.
- **Rule of thumb:** `hi = mid` pairs with the lower mid, `lo = mid` pairs with the upper mid.

### Knob D: what you return
- Exact match: return inside the loop, else -1.
- First/last position or insertion point: return `lo` after the loop, then check it is in range and holds the target if the question needs that.

## 5. The variants you will actually meet

**Lower bound: first index with `nums[i] >= target`** (same as `bisect_left`)
```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)            # half-open, n is a valid answer
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1             # mid too small, rule it out
        else:
            hi = mid                 # mid could be the answer, keep it
    return lo
```
Invariant: everything left of `lo` is < target, everything at or right of `hi` is ≥ target.

**Upper bound: first index with `nums[i] > target`** (same as `bisect_right`). Change only `<` to `<=` in the comparison. The count of `target` is `upper - lower`, and the last occurrence is `upper - 1`.

**Last index satisfying a condition (upper mid):**
```python
lo, hi = 0, n - 1
while lo < hi:
    mid = lo + (hi - lo + 1) // 2    # round up because of lo = mid
    if ok(mid): lo = mid
    else:       hi = mid - 1
```

**Binary search on the answer.** This is the most common Google form. The array is not searched at all. You search a range of possible answers where `feasible(x)` flips from False to True exactly once. Examples: Koko eating bananas, ship within D days, split array largest sum.
```python
def min_feasible(lo, hi, feasible):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid): hi = mid   # mid works, maybe something smaller does too
        else:             lo = mid + 1
    return lo
```
Cost is O(log(range) × cost of feasible).

**Rotated sorted array.** At every mid, one half is sorted. Check whether the target falls in the sorted half. If yes, search there, else go to the other half.

**Peak element / minimum in rotated array.** Compare `nums[mid]` with `nums[mid + 1]` or with `nums[hi]` instead of with a target. Use the `lo < hi` form with `hi = mid`.

## 6. Decision table: which knobs for which question
| Question | Window | Loop | Moves | Return |
|---|---|---|---|---|
| Does x exist? | [0, n-1] | lo <= hi | ±1 both sides | mid or -1 |
| First ≥ x / insert position | [0, n) | lo < hi | lo=mid+1, hi=mid | lo |
| First > x | [0, n) | lo < hi | same, with <= | lo |
| Last satisfying ok | [0, n-1] | lo < hi | lo=mid, hi=mid-1, upper mid | lo |
| Minimum feasible answer | [min, max] | lo < hi | hi=mid, lo=mid+1 | lo |

## 7. Common bugs
1. `(lo + hi) // 2` overflows in Java/C++. Python ints don't overflow, but write `lo + (hi - lo) // 2` in interviews to show you know.
2. Mixing a closed window with `lo < hi`, which skips an element.
3. `lo = mid` with the lower mid, which loops forever.
4. Forgetting that lower bound can return `n`. Check `lo < n and nums[lo] == target`.
5. Using binary search on data that is not monotonic.

## 8. Two pointers, for contrast
```python
def pair_sum(nums, k):               # nums sorted
    i, j = 0, len(nums) - 1
    while i < j:
        s = nums[i] + nums[j]
        if s == k: return i, j
        if s < k: i += 1             # need bigger, drop smallest
        else:     j -= 1             # need smaller, drop largest
    return None
```
Invariant: no valid pair uses an index outside `[i, j]`. Each step drops one element, not half, so it is O(n). Choose binary search when you ask "where does a monotonic condition flip?" Choose two pointers when you look at pairs or a window that moves one step at a time.

## 9. Interview prep
- **Control flow:** initialize the window, loop while it has candidates, probe mid, move one boundary according to the monotonic test, then return from inside the loop or return `lo`.
- **Purpose:** find where a monotonic predicate changes from False to True, in an array or over a range of answers.
- **Output:** an index, an insertion point, or the smallest feasible value.
- **Trade-offs:** O(log n) time and O(1) space, but it needs sorted or monotonic input. Sorting first costs O(n log n), so for one lookup a linear scan is cheaper. For many lookups, sort once and search many times. In production Python, use `bisect`.
- **What a strong candidate says:** "I'll define the predicate first. Here it is `nums[i] >= target`, which is False then True. I'll use a half-open window `[0, n)` because n is a valid answer. The invariant is that left of lo is False and hi onward is True. At mid, if the predicate is False I set `lo = mid + 1`, otherwise `hi = mid` since mid might be the answer. The window shrinks every step, so it ends in O(log n) with lo == hi at the first True."
- **Likely Google follow-ups:** first and last position of a target, search a rotated array, find the minimum of a rotated array, median of two sorted arrays, and "binary search on the answer" problems.

---

# Part 2: going deeper

## 10. How to recognize a binary search problem
Reach for binary search when you see any of these:
- **Sorted input** (or "non-decreasing", "rotated sorted") and a question about position, existence or count.
- **"Minimum X such that…" / "maximum X such that…"**: the smallest speed, capacity, day or size that works. That is binary search on the answer.
- **A yes/no check that flips once.** If `feasible(x)` is True, then `feasible(x + 1)` is also True (or the reverse). That is called monotonic.
- **Constraints:** n up to 10⁵–10⁶ with values up to 10⁹, and a hint that O(n²) is too slow. O(n log n) or O(n log V) is the target.
- **"Find a peak", "find the rotation point"**: no target at all, but you can still tell which half to keep.

Ask yourself one question: **"If I probe the middle, can I throw away one half for sure?"** If yes, it's binary search.

## 11. More traces

### Leftmost position (lower bound) with duplicates
`nums = [5, 7, 7, 8, 8, 10]`, target 8, half-open window `[0, 6)`:
| step | lo | hi | mid | nums[mid] | nums[mid] < 8? | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 8 | no | hi = 3 (mid might be the first 8) |
| 2 | 0 | 3 | 1 | 7 | yes | lo = 2 |
| 3 | 2 | 3 | 2 | 7 | yes | lo = 3 |
| end | 3 | 3 | | | | return 3 |

### Rightmost position (upper bound − 1)
Same array, "first index with `nums[i] > 8`":
| step | lo | hi | mid | nums[mid] | nums[mid] <= 8? | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 6 | 3 | 8 | yes | lo = 4 |
| 2 | 4 | 6 | 5 | 10 | no | hi = 5 |
| 3 | 4 | 5 | 4 | 8 | yes | lo = 5 |
| end | 5 | 5 | | | | upper = 5, last 8 is at 4 |

### LC 34 in terms of those two
```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

def searchRange(nums, target):
    first = lower_bound(nums, target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    last = lower_bound(nums, target + 1) - 1   # first index of anything bigger, minus one
    return [first, last]
```
`target + 1` works because the values are integers. For floats, write a separate upper bound with `<=`.

## 12. Worked problems

### LC 33: Search in Rotated Sorted Array
**Idea:** a rotated array like `[4,5,6,7,0,1,2]` is two sorted runs. At any `mid`, at least one of the two halves is fully sorted. Check whether the target lies in the sorted half. If yes, go there, otherwise go to the other half.
```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                 # left half [lo, mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                     # right half [mid, hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```
Trace `[4,5,6,7,0,1,2]`, target 0:
| lo | hi | mid | nums[mid] | sorted half | target inside? | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | left (4 ≤ 7) | 4 ≤ 0 < 7? no | lo = 4 |
| 4 | 6 | 5 | 1 | left (0 ≤ 1) | 0 ≤ 0 < 1? yes | hi = 4 |
| 4 | 4 | 4 | 0 | | found | return 4 |

**Why `<=` in `nums[lo] <= nums[mid]`:** when `lo == mid` (two elements left), the "left half" is one element, and one element is sorted. With `<` you would wrongly treat it as the unsorted side.

### LC 153: Minimum in Rotated Sorted Array
```python
def findMin(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1      # the drop is to the right of mid, mid is not the minimum
        else:
            hi = mid          # mid..hi is sorted, so the minimum is mid or to its left
    return nums[lo]
```
Trace `[3,4,5,1,2]`: (0,4, mid 2: 5 > 2 → lo = 3), (3,4, mid 3: 1 > 2? no → hi = 3), return `nums[3] = 1`.
**Why compare with `nums[hi]` and not `nums[lo]`:** on an unrotated array `[1,2,3]`, `nums[mid] > nums[lo]` is True but the minimum is on the left. Comparing with `hi` works for both the rotated and the unrotated case.

### LC 162: Find Peak Element
```python
def findPeakElement(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1      # going uphill to the right, so a peak exists on the right
        else:
            hi = mid          # downhill or flat to the right, so mid or something left is a peak
    return lo
```
`mid + 1` never goes out of range, because `lo < hi` means `mid < hi`. The array isn't sorted, but the question "which side has a peak?" still has a sure answer. That's all binary search needs.

### LC 74: Search a 2-D Matrix
Each row is sorted, and each row starts after the previous row ends, so the matrix is one sorted list of `m * n` values. Index `i` of that list is `matrix[i // n][i % n]`.
```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        v = matrix[mid // n][mid % n]
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

### LC 875: Koko Eating Bananas (binary search on the answer)
- **Answer range:** speed `k` from 1 to `max(piles)`. At `max(piles)`, every pile takes 1 hour, which always fits because `h >= len(piles)`.
- **Check:** `hours(k) = sum(ceil(p / k))`. A faster speed never takes more hours, so `hours(k) <= h` flips from False to True exactly once.
- **Goal:** the smallest `k` with `hours(k) <= h`, which is the "minimum feasible" template.
```python
def minEatingSpeed(piles, h):
    def hours(k):
        return sum((p + k - 1) // k for p in piles)   # integer ceil(p / k)
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if hours(mid) <= h:
            hi = mid          # mid works, try slower
        else:
            lo = mid + 1      # too slow
    return lo
```
Trace `piles = [3,6,7,11]`, `h = 8`:
| lo | hi | mid | hours(mid) | fits? | action |
|---|---|---|---|---|---|
| 1 | 11 | 6 | 1+1+2+2 = 6 | yes | hi = 6 |
| 1 | 6 | 3 | 1+2+3+4 = 10 | no | lo = 4 |
| 4 | 6 | 5 | 1+2+2+3 = 8 | yes | hi = 5 |
| 4 | 5 | 4 | 1+2+2+3 = 8 | yes | hi = 4 |
| end | | | | | return 4 |

Cost: O(n · log(max(piles))). `(p + k - 1) // k` is ceiling division without floats. `math.ceil(p / k)` also works but can hit float rounding on huge numbers.

## 13. Python's `bisect` module
```python
import bisect
a = [1, 3, 3, 3, 7]
bisect.bisect_left(a, 3)    # 1: first index with a[i] >= 3 (lower bound)
bisect.bisect_right(a, 3)   # 4: first index with a[i] > 3 (upper bound)
bisect.bisect_right(a, 3) - bisect.bisect_left(a, 3)   # 3: count of 3s
bisect.insort(a, 5)         # inserts, keeping a sorted (the insert itself is O(n))
```
- Python 3.10+ accepts `key=` for searching by a derived value.
- **In an interview:** write the loop by hand unless they allow libraries. Then mention "in production I'd use `bisect_left`". That shows you know both.

## 14. Edge-case checklist
Run every binary search against these before submitting:
1. Empty array `[]`
2. One element, where the target equals it, is below it, and is above it
3. Two elements. Most off-by-one bugs show up here.
4. Target smaller than everything, and target larger than everything
5. All elements equal, e.g. `[2,2,2,2]` with target 2, for first and last position
6. Target at index 0 and at index n−1

## 15. Debugging an off-by-one: the two-element trace
If you're unsure about a loop, trace it by hand on `[1, 3]` with targets 0, 1, 2, 3 and 4. That's five tiny traces. They catch:
- **Infinite loops:** `lo = mid` with the lower mid. On `lo = 0, hi = 1`, mid is 0 forever.
- **Skipped elements:** a closed window with `lo < hi` never checks the last candidate.
- **Out-of-range reads:** a half-open `hi = n` with `lo <= hi` reads `nums[n]`.

## 16. Recursive version, and why to prefer the loop
```python
def search_rec(nums, target, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo > hi:
        return -1
    mid = lo + (hi - lo) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        return search_rec(nums, target, mid + 1, hi)
    return search_rec(nums, target, lo, mid - 1)
```
Same O(log n) time, but O(log n) stack space instead of O(1). The loop is the standard answer. Recursion is useful mainly for explaining the idea.

## 17. Practice ladder
1. 704 Binary Search: exact match (done)
2. 35 Search Insert Position: lower bound (done)
3. 34 First and Last Position: lower and upper bound (done)
4. 74 Search a 2-D Matrix: index mapping
5. 153 Find Minimum in Rotated Sorted Array: compare with `hi`
6. 33 Search in Rotated Sorted Array: find the sorted half
7. 162 Find Peak Element: no target
8. 875 Koko Eating Bananas: binary search on the answer
9. 1011 Capacity to Ship Packages Within D Days: same as 875, with different bounds
