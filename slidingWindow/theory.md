# Sliding window, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved: 121
- Mistake and correction:

---

**One word:** Window.
**One sentence:** Keep a contiguous range `[l, r]` that you grow on the right and shrink on the left, updating its summary as you go, so every subarray question is answered in one pass.

## Executive summary
- **Use it for:** contiguous subarrays or substrings: the longest, shortest or count that satisfies a condition.
- **Two kinds:** fixed size k (slide by one), and variable size (grow `r`, shrink `l` while the window is invalid).
- **State:** a running summary of the window, such as a sum, a character count or the number of distinct characters. Update it in O(1) when a character enters or leaves.
- **Why O(n):** `r` moves n times, and `l` moves at most n times in total. The inner `while` doesn't make it O(n²).
- **When it fails:** the condition must stay monotonic. Shrinking must never turn a valid window invalid in the wrong direction. Sums with negative numbers break this, so use a prefix sum plus a hash map instead.

---

## 1. The variable-window template
```python
def longest_valid(s):
    l = 0
    state = {}                          # whatever describes window s[l..r]
    best = 0
    for r in range(len(s)):
        # 1. add s[r] to state
        # 2. while the window is invalid: remove s[l] from state, l += 1
        # 3. the window is valid now: best = max(best, r - l + 1)
        pass
    return best
```
For **shortest** questions, flip it: while the window **is valid**, record the answer, then shrink.

## 2. Longest Substring Without Repeating Characters (LC 3)
```python
def lengthOfLongestSubstring(s):
    last = {}                           # char -> last index seen
    l = 0
    best = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= l:
            l = last[ch] + 1            # jump past the previous copy
        last[ch] = r
        best = max(best, r - l + 1)
    return best
```
Trace `"abcabcbb"`:
| r | ch | last[ch] before | l after | window | best |
|---|---|---|---|---|---|
| 0 | a | — | 0 | a | 1 |
| 1 | b | — | 0 | ab | 2 |
| 2 | c | — | 0 | abc | 3 |
| 3 | a | 0 | 1 | bca | 3 |
| 4 | b | 1 | 2 | cab | 3 |
| 5 | c | 2 | 3 | abc | 3 |
| 6 | b | 4 | 5 | cb | 3 |
| 7 | b | 6 | 7 | b | 3 |

**Invariant:** `s[l..r]` has no repeated character.
**Why `last[ch] >= l`:** an old copy that's already left of the window doesn't matter. Without this check, `"abba"` moves `l` backwards and returns the wrong answer.

## 3. Shortest window: Minimum Size Subarray Sum (LC 209)
```python
def minSubArrayLen(target, nums):
    l = 0
    s = 0
    best = float('inf')
    for r, x in enumerate(nums):
        s += x
        while s >= target:              # valid, so record it, then try to shrink
            best = min(best, r - l + 1)
            s -= nums[l]
            l += 1
    return 0 if best == float('inf') else best
```
This only works because all numbers are positive: adding makes the sum bigger and removing makes it smaller.

## 4. Longest Repeating Character Replacement (LC 424)
A window is valid if `window length - count of its most frequent char <= k`, meaning at most k characters need replacing.
```python
def characterReplacement(s, k):
    count = {}
    l = 0
    maxf = 0
    best = 0
    for r, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        maxf = max(maxf, count[ch])
        while (r - l + 1) - maxf > k:
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
```
**Why `maxf` never needs to go down:** a stale, too-high `maxf` can only stop the window from growing past its best size so far. `best` only increases when a real, higher frequency appears. This is a classic follow-up question, so be ready to explain it.

## 5. Fixed-size window
Maximum Average Subarray I (LC 643), or any "every window of size k":
```python
def findMaxAverage(nums, k):
    s = sum(nums[:k])
    best = s
    for r in range(k, len(nums)):
        s += nums[r] - nums[r - k]      # one element enters, one leaves
        best = max(best, s)
    return best / k
```
Permutation in String (LC 567) is a fixed window of `len(s1)` that compares 26-letter counts.

## 6. Best Time to Buy and Sell Stock (LC 121) as a window
```python
def maxProfit(prices):
    lowest = float('inf')
    best = 0
    for p in prices:
        lowest = min(lowest, p)         # the best buy day so far is the window's left edge
        best = max(best, p - lowest)
    return best
```

## 7. Decision table
| Question | Window | Loop shape |
|---|---|---|
| Longest with at most / no more than … | variable | shrink while invalid, then record |
| Shortest with at least … | variable | record while valid, then shrink |
| Every window of size k | fixed | add the right element, remove element r−k |
| Count subarrays with exactly K … | variable twice | atMost(K) − atMost(K−1) |
| Subarray sum = k with negative numbers | **not a window** | prefix sum + hash map |

## 8. Common bugs
1. Recording the answer before the window is fixed up (longest) or after it's been shrunk (shortest).
2. Forgetting to remove `s[l]` from the state before moving `l`.
3. Moving `l` backwards (see the `"abba"` case in LC 3).
4. Using a window on sums with negative numbers.
5. Off-by-one in the length: it's `r - l + 1`.

## 9. Edge cases
- Empty string or array
- k = 0, and k ≥ n
- Everything the same character, or all characters different
- No valid window at all (LC 209 should return 0)

## 10. Interview prep
- **Purpose:** answer questions about all contiguous ranges in O(n) instead of O(n²).
- **Control flow:** a `for` loop grows `r`, an inner `while` shrinks `l` until the condition holds again, then you record the answer.
- **Complexity:** O(n) time, because each index enters and leaves once. Space is O(size of the alphabet) or O(k).
- **What a strong candidate says:** "Each index enters the window once and leaves once, so even with the inner while loop, it's O(n). The window is valid when…, and shrinking only ever makes it more valid, which is why the greedy shrink is correct."
- **Likely follow-ups:** Minimum Window Substring (LC 76, hard), Sliding Window Maximum (LC 239, uses a monotonic deque), "at most K distinct characters".
