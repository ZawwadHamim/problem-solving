 # Binary search, in full

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