# Hash map, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved: 1, 242
- Mistake and correction:

---

**One word:** Lookup.
**One sentence:** A hash map spends O(n) extra memory so that "have I seen this before, and where?" costs O(1) instead of a full scan.

## Executive summary
- **What it is:** a table from key to value. `dict` in Python, `set` when you only need the keys.
- **Why it's fast:** the key is hashed to a bucket index, so lookup, insert and delete are O(1) on average.
- **The trade:** O(n) memory for O(1) lookups. Most "O(n²) → O(n)" improvements in interviews are this trade.
- **Five shapes you'll meet:** complement lookup, frequency count, grouping by a key, seen-set, and prefix sum plus a map.

---

## 1. How it works (just enough)
- `hash(key)` gives a number, and `number % capacity` picks a bucket.
- Two keys can land in the same bucket (a collision). Python probes other slots until it finds a free one.
- When the table gets about 2/3 full, Python grows it and re-inserts everything. That's O(n) once in a while, so the cost averages out to O(1) per insert.
- **Worst case is O(n)** per operation if many keys collide. It almost never happens with built-in types. Say "O(1) average" in interviews.
- **Keys must be hashable,** meaning they can't change: `int`, `str` and `tuple` work, but `list`, `dict` and `set` don't. To use a list as a key, convert it: `tuple(lst)`.

## 2. Shape A: complement lookup (Two Sum, LC 1)
**Question:** find `i, j` with `nums[i] + nums[j] == target`.
**Idea:** for each `x`, the partner you need is `target - x`. Remember every value you've passed and its index.
```python
def twoSum(nums, target):
    seen = {}                      # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:           # check BEFORE storing x
            return [seen[need], i]
        seen[x] = i
    return []
```
Trace `[2, 7, 11, 15]`, target 9:
| i | x | need | seen before | action |
|---|---|---|---|---|
| 0 | 2 | 7 | {} | store 2→0 |
| 1 | 7 | 2 | {2:0} | found, return [0, 1] |

**Invariant:** at step `i`, `seen` holds every value from `nums[0..i-1]`, so any pair ending at `i` is found at step `i`.
**Why check before storing:** with `[3]` and target 6, storing first would pair 3 with itself. With `[3, 3]`, checking first still finds `[0, 1]`.

## 3. Shape B: frequency count (Valid Anagram, LC 242)
```python
from collections import Counter

def isAnagram(s, t):
    return Counter(s) == Counter(t)

# by hand, which interviewers sometimes ask for:
def isAnagram_manual(s, t):
    if len(s) != len(t):
        return False
    count = {}
    for a, b in zip(s, t):
        count[a] = count.get(a, 0) + 1
        count[b] = count.get(b, 0) - 1
    return all(v == 0 for v in count.values())
```
- `count.get(k, 0) + 1` is the standard counting idiom. `collections.defaultdict(int)` avoids the `.get`.
- If the input is only lowercase a–z, an array of 26 counts works too and is still O(1) space.

## 4. Shape C: grouping by a key (Group Anagrams, LC 49)
**Idea:** give every word a key that's identical for all its anagrams, then group words by that key.
```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for w in strs:
        key = [0] * 26
        for ch in w:
            key[ord(ch) - ord('a')] += 1
        groups[tuple(key)].append(w)    # a list can't be a key, a tuple can
    return list(groups.values())
```
- The key could also be `''.join(sorted(w))`, which costs O(k log k) per word instead of O(k) for the count tuple.
- **Total cost:** O(n·k), where k is the word length.

## 5. Shape D: seen-set (Contains Duplicate, LC 217; Longest Consecutive Sequence, LC 128)
```python
def containsDuplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
# one-liner: return len(set(nums)) < len(nums)
```
LC 128 finds the longest run of consecutive integers in O(n) without sorting:
```python
def longestConsecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:          # x starts a run; only count from starts
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best
```
**Why it's O(n) with a nested loop:** the inner `while` only runs from the start of a run, so each number is walked over at most once in total.

## 6. Shape E: top-k by frequency (LC 347), using bucket sort
```python
from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]   # index = frequency
    for x, c in count.items():
        buckets[c].append(x)
    res = []
    for c in range(len(buckets) - 1, 0, -1):
        for x in buckets[c]:
            res.append(x)
            if len(res) == k:
                return res
    return res
```
O(n), because a frequency can't be bigger than n. The heap version is O(n log k) (see `heap/theory.md`), and `Counter(nums).most_common(k)` does it in one line.

## 7. Shape F: prefix sum plus a map
"Count subarrays with sum k" uses a map from prefix sum to how many times it's been seen. Covered in full in `prefixSum/theory.md` (LC 560).

## 8. Decision table
| Question | Structure | Key → value |
|---|---|---|
| Does a partner exist? | dict | value → index |
| Same letters / same counts? | Counter | item → count |
| Group things that are "the same" | defaultdict(list) | canonical key → items |
| Have I seen it before? | set | — |
| Count subarrays with a sum | dict | prefix sum → count |
| Most or least frequent | Counter + buckets or heap | item → count |

## 9. Common bugs
1. Storing before checking in Two Sum, which pairs an element with itself.
2. Using a list as a key (`TypeError: unhashable type`). Use a tuple.
3. `d[k] += 1` on a missing key raises `KeyError`. Use `.get(k, 0)` or `defaultdict(int)`.
4. Changing a dict while looping over it. Loop over `list(d)` instead.
5. Assuming a dict is sorted. It keeps insertion order, not key order.

## 10. Edge cases
- Empty input, and a single element
- Duplicates, e.g. `[3, 3]` with target 6
- Negative numbers and zero
- Unicode or uppercase when the problem says "lowercase". Ask first.

## 11. Complexity
| Operation | Average | Worst |
|---|---|---|
| `x in d`, `d[x]`, `d[x] = v`, `del d[x]` | O(1) | O(n) |
| Build from n items | O(n) | O(n²) |
| Space | O(n) | O(n) |

## 12. Interview prep
- **Purpose:** turn repeated searching into one lookup, in exchange for memory.
- **Control flow:** one pass. At each element, query the map for what you need, then update the map with the current element.
- **Trade-offs:** O(n) memory. If memory is tight and the input can be sorted, sorting plus two pointers gives O(n log n) time and O(1) extra space (see `twoPointers/theory.md`).
- **What a strong candidate says:** "The brute force checks all pairs, O(n²). The inner loop only answers 'does target minus x exist?', which a hash map answers in O(1). So one pass with a value-to-index map gives O(n) time and O(n) space. I check before inserting so an element can't pair with itself."
- **Likely follow-ups:** "What if the input is sorted?" (two pointers, O(1) space). "What if it doesn't fit in memory?" (split the data into hash buckets on disk, or sort externally). "Return all pairs, not just one?" (count occurrences and handle duplicates).
