# Intervals, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** Overlap.
**One sentence:** Sort intervals by start (or by end), then sweep once, comparing each interval only with the last one you kept.

## Executive summary
- **Overlap test:** `[a, b]` and `[c, d]` overlap when `a <= d and c <= b`. Whether touching ends (`b == c`) count as overlapping depends on the problem, so read it carefully.
- **Merging:** sort by start. Each interval either extends the last merged interval or starts a new one.
- **Keeping as many as possible without overlap:** sort by **end**, and greedily keep whichever interval finishes earliest.
- **Counting how many overlap at once (meeting rooms):** sort the starts and ends separately, or use a min-heap of end times.
- **Cost:** O(n log n) for the sort, then an O(n) sweep.

---

## 1. Merge Intervals (LC 56)
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for s, e in intervals:
        if res and s <= res[-1][1]:            # overlaps (or touches) the last merged one
            res[-1][1] = max(res[-1][1], e)    # max, because the new one may be fully inside
        else:
            res.append([s, e])
    return res
```
Trace `[[1,3],[2,6],[8,10],[15,18]]` (already sorted):
| interval | last merged | overlaps? | res |
|---|---|---|---|
| [1,3] | — | — | [[1,3]] |
| [2,6] | [1,3] | 2 ≤ 3, yes | [[1,6]] |
| [8,10] | [1,6] | 8 ≤ 6? no | [[1,6],[8,10]] |
| [15,18] | [8,10] | no | [[1,6],[8,10],[15,18]] |

**Invariant:** after sorting, an interval can only overlap the **last** merged interval. Earlier ones end before the last one starts.
**Why `max`:** `[1,10]` followed by `[2,3]` must stay `[1,10]`, not shrink to `[1,3]`.

## 2. Insert Interval (LC 57): already sorted, O(n)
Three phases: intervals entirely before the new one, intervals overlapping it (merge them in), and intervals entirely after.
```python
def insert(intervals, new):
    res = []
    i, n = 0, len(intervals)
    while i < n and intervals[i][1] < new[0]:       # ends before new starts
        res.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new[1]:      # overlaps new
        new = [min(new[0], intervals[i][0]), max(new[1], intervals[i][1])]
        i += 1
    res.append(new)
    res.extend(intervals[i:])                       # starts after new ends
    return res
```
Trace `[[1,2],[3,5],[6,7],[8,10],[12,16]]` with new `[4,8]`: `[1,2]` goes before. `[3,5]`, `[6,7]` and `[8,10]` merge into `[3,10]`. `[12,16]` goes after. Result: `[[1,2],[3,10],[12,16]]`.

## 3. Non-overlapping Intervals (LC 435): sort by end
Remove as few intervals as possible so that none overlap. That's the same as keeping as many as possible.
```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])
    end = float('-inf')
    keep = 0
    for s, e in intervals:
        if s >= end:                    # touching is allowed in this problem
            keep += 1
            end = e
    return len(intervals) - keep
```
**Why sort by end (the exchange argument):** take any best solution. Its first interval can be swapped for the interval that ends earliest without causing any overlap, because ending earlier only leaves more room. Repeat that for each step, and the greedy choice is optimal.
**Why not sort by start:** one long interval that starts early would block many short ones.

## 4. Minimum Number of Arrows to Burst Balloons (LC 452)
The same greedy idea: sort by end, and shoot at the end of the first balloon still standing.
```python
def findMinArrowShots(points):
    points.sort(key=lambda x: x[1])
    arrows = 0
    end = float('-inf')
    for s, e in points:
        if s > end:                     # touching balloons ARE burst by one arrow, hence >
            arrows += 1
            end = e
    return arrows
```
Compare with LC 435: the only difference is `>` versus `>=`, depending on whether touching counts. Read every problem's definition of overlap.

## 5. Meeting Rooms II (LC 253): the most rooms needed at once
```python
def minMeetingRooms(intervals):
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = 0
    j = 0
    for s in starts:
        if s < ends[j]:                 # nothing has finished yet, so open a new room
            rooms += 1
        else:                           # a meeting ended, so reuse its room
            j += 1
    return rooms
```
Trace `[[0,30],[5,10],[15,20]]`: starts `[0,5,15]`, ends `[10,20,30]`. 0 < 10 → 1 room. 5 < 10 → 2 rooms. 15 ≥ 10 → reuse (j = 1). **Answer: 2.**
**Heap version:** sort by start, and keep a min-heap of end times. Pop the earliest end if it's ≤ the current start, then push the current end. The heap's size at the end is the answer. See `heap/theory.md`.
Meeting Rooms I (LC 252, "can one person attend all?"): sort by start and check `intervals[i][0] >= intervals[i-1][1]` for every i.

## 6. Decision table
| Question | Sort by | Sweep rule |
|---|---|---|
| Merge overlapping | start | extend the last one or start a new one |
| Insert into an already sorted list | (already sorted) | before / overlap / after phases |
| Keep the most, or remove the fewest | end | keep if start ≥ the last kept end |
| Fewest points that hit every interval | end | new point if start > the last point |
| Most intervals overlapping at once | starts and ends separately, or a heap | two pointers or a heap of ends |
| Can one person attend everything? | start | any overlap means no |

## 7. Common bugs
1. Forgetting to sort, or sorting by the wrong end.
2. Replacing the end instead of taking `max(old_end, new_end)`.
3. Mixing up `<` and `<=` for touching intervals. Check an example like `[1,2],[2,3]` against the problem statement.
4. Changing the input list when the caller still needs it. Say so, or copy it first.
5. Changing a tuple in place. Store lists, or build new tuples.

## 8. Edge cases
- Empty list, or one interval
- One interval fully inside another
- Touching endpoints
- All intervals identical
- Intervals given out of order

## 9. Interview prep
- **Purpose:** make overlap questions local. After sorting, you only ever compare with the previous interval.
- **Control flow:** sort, then one pass keeping a single "current" interval or end value.
- **Complexity:** O(n log n) time for the sort. O(n) space for the output, or O(1) extra.
- **What a strong candidate says:** "Once sorted by start, an interval can only overlap the last merged one, so a single pass works. For keeping the most intervals, I sort by end, and the exchange argument proves it's optimal: the earliest-ending interval leaves the most room."
- **Likely follow-ups:** Employee Free Time (LC 759), Interval List Intersections (LC 986, two pointers), Minimum Interval to Include Each Query (LC 1851, sort plus a heap).
