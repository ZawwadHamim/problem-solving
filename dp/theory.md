# Dynamic programming (1-D), in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved: 53 (Kadane, in ../array)
- Mistake and correction:

---

**One word:** Reuse.
**One sentence:** When the answer for a big input is built from answers to smaller inputs, and those smaller answers repeat, compute each one once and store it.

## Executive summary
- **Two conditions for DP:**
  1. **Optimal substructure:** the best answer is built from the best answers to smaller pieces.
  2. **Overlapping subproblems:** the same smaller piece is needed again and again.
- **The four questions** (answer them in writing before coding):
  1. **State:** what does `dp[i]` mean, in one sentence?
  2. **Transition:** how is `dp[i]` computed from smaller states?
  3. **Base cases:** the smallest states, known directly.
  4. **Order and answer:** which direction to fill in, and which entry is the final answer.
- **Top-down:** recursion plus `@cache` (memoization). Easiest to write from the recursive idea.
- **Bottom-up:** a loop filling a table. No recursion limit, and often reducible to O(1) space by keeping only the last few values.
- **Backtracking vs DP:** backtracking lists every answer. DP counts them or finds the best one, without listing them.

---

## 1. Climbing Stairs (LC 70): the first DP
**State:** `ways(i)` = the number of ways to reach step i.
**Transition:** the last move was 1 step or 2 steps, so `ways(i) = ways(i-1) + ways(i-2)`.
**Base cases:** `ways(0) = 1` (standing still), `ways(1) = 1`.

Top-down:
```python
from functools import cache

def climbStairs_memo(n):
    @cache
    def ways(i):
        if i <= 1:
            return 1
        return ways(i - 1) + ways(i - 2)
    return ways(n)
```
Bottom-up, O(1) space:
```python
def climbStairs(n):
    a, b = 1, 1                    # ways(i-2), ways(i-1)
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```
Check by hand: n = 1 gives 1. n = 2 gives 2 (1+1, or 2). n = 3 gives 3. n = 4 gives 5.
**Why memoization matters:** plain recursion calls `ways(n-2)` from two places, `ways(n-3)` from three, and so on. That's O(2ⁿ). Caching makes it O(n).

## 2. Min Cost Climbing Stairs (LC 746)
**State:** `dp[i]` = the minimum cost to stand on step i, where the top is step n.
**Transition:** `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`.
**Base cases:** `dp[0] = dp[1] = 0`, because you may start on either step.
```python
def minCostClimbingStairs(cost):
    a = b = 0                      # dp[i-2], dp[i-1]
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b
```
Trace `[10, 15, 20]`: dp[2] = min(0+15, 0+10) = 10. dp[3] = min(10+20, 0+15) = **15**.

## 3. House Robber (LC 198): take or skip
**State:** `dp[i]` = the most money from houses `0..i`.
**Transition:** skip house i (`dp[i-1]`) or rob it (`dp[i-2] + nums[i]`). Take the larger.
```python
def rob(nums):
    prev, cur = 0, 0               # best up to i-2, best up to i-1
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur
```
Trace `[2, 7, 9, 3, 1]`:
| x | prev (i−2) | cur (i−1) | new cur = max(cur, prev + x) |
|---|---|---|---|
| 2 | 0 | 0 | 2 |
| 7 | 0 | 2 | 7 |
| 9 | 2 | 7 | 11 |
| 3 | 7 | 11 | 11 |
| 1 | 11 | 11 | **12** |

Houses in a circle (LC 213): run it on `nums[1:]` and on `nums[:-1]`, and take the larger.

## 4. Coin Change (LC 322): the state is an amount, not an index
**State:** `dp[a]` = the fewest coins that make amount a.
**Transition:** `dp[a] = min(dp[a - c] + 1)` over every coin c ≤ a.
**Base case:** `dp[0] = 0`. Everything else starts as "impossible" (use `amount + 1` for that).
```python
def coinChange(coins, amount):
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
```
Coins `[1, 2, 5]`, amount 11: dp[5] = 1, dp[10] = 2, dp[11] = dp[10] + 1 = **3** (5 + 5 + 1). O(amount × number of coins).
**Why greedy fails:** with coins `[1, 3, 4]` and amount 6, greedy picks 4 + 1 + 1 (3 coins), but 3 + 3 uses 2.

## 5. Longest Increasing Subsequence (LC 300)
**State:** `dp[i]` = the length of the longest increasing subsequence that **ends at** index i.
**Transition:** `dp[i] = 1 + max(dp[j])` over every j < i with `nums[j] < nums[i]`.
**Answer:** `max(dp)`, not `dp[-1]`.
```python
def lengthOfLIS(nums):
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```
O(n²). The O(n log n) version keeps `tails[k]` = the smallest possible last value of an increasing subsequence of length k+1, and places each number with `bisect_left`. That's where DP and binary search meet (see `../binarySearch/theory.md`).

## 6. Maximum Subarray (LC 53): Kadane's algorithm is DP
**State:** `best_ending_here` = the best sum of a subarray that ends at i.
**Transition:** `max(x, best_ending_here + x)`, meaning start fresh here or extend the previous one.
```python
def maxSubArray(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```
You already solved it in `../array/53_maximum_subarray.py`. Now you know it's DP.

## 7. How to find the state (when you're stuck)
1. Write the brute-force recursion first: "the answer for i uses the answers for…".
2. List what changes between recursive calls. Those values are the state. One changing value means 1-D DP.
3. Check whether any call repeats. If yes, cache it.
4. Turn it into a loop in the order the dependencies point (small i to large i).
5. If `dp[i]` only uses `dp[i-1]` and `dp[i-2]`, keep two variables instead of the whole array.

## 8. Decision table
| Signal | State |
|---|---|
| "Number of ways to reach…" | `dp[i]` = ways to reach i, **summed** over the last moves |
| "Min or max cost to reach…" | `dp[i]` = best cost to reach i, **min/max** over the last moves |
| "Can't pick adjacent items" | take or skip: `max(dp[i-1], dp[i-2] + x)` |
| "Fewest items to make a total" | `dp[amount]` over each item |
| "Longest subsequence with a property" | `dp[i]` = best that **ends at** i, answer = `max(dp)` |
| "Best contiguous subarray" | Kadane: best ending here |
| "List all the solutions" | not DP: backtracking |

## 9. Common bugs
1. A vague state. If you can't say what `dp[i]` means in one sentence, stop and define it.
2. Wrong base cases (`ways(0) = 1`, not 0).
3. Returning `dp[-1]` when the answer is `max(dp)` (LIS).
4. Using 0 as "impossible" in a min DP. Use infinity or `amount + 1`.
5. Recursion without a cache, which is exponential time.
6. Recursion depth errors with `@cache` for large n. Switch to bottom-up.

## 10. Edge cases
- n = 0, and n = 1
- Amount 0 (answer 0), and an amount that can't be made (answer −1)
- All negative numbers (Kadane must return the largest single element)
- A single house

## 11. Interview prep
- **Purpose:** turn exponential recursion into polynomial time by solving each subproblem once.
- **Control flow:** define the state, write the transition, set the base cases, fill in the table in dependency order, return the answer entry.
- **Complexity:** number of states × work per state. For example, Coin Change is O(amount × coins), and LIS is O(n²).
- **What a strong candidate says:** "Let dp[i] be the most money from the first i houses. For house i, I either skip it and take dp[i-1], or rob it and take dp[i-2] plus its value. That's O(n), and since only two previous values are used, I can keep two variables for O(1) space."
- **Likely follow-ups:** Decode Ways (LC 91), Word Break (LC 139), Partition Equal Subset Sum (LC 416), Longest Palindromic Substring (LC 5), then 2-D DP (Unique Paths LC 62, Longest Common Subsequence LC 1143).
