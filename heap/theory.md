# Heap / priority queue, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** Priority.
**One sentence:** A heap always hands you the smallest (or largest) item in O(log n), which is exactly what "top k", "k-th largest", "merge sorted streams" and "the next event to happen" need.

## Executive summary
- **Python's `heapq` is a min-heap** stored in a plain list. `h[0]` is always the smallest.
- **Costs:** `heappush` and `heappop` are O(log n), peeking at `h[0]` is O(1), and `heapify` is O(n).
- **Max-heap:** push `-x` and negate again when you pop.
- **Top k largest:** keep a **min**-heap of size k. Its root is the k-th largest. O(n log k) time, O(k) space.
- **Ties and objects that can't be compared:** push tuples like `(priority, counter, item)`.

---

## 1. How it works (just enough)
- It's a complete binary tree stored in an array. The children of index `i` are at `2i+1` and `2i+2`, and its parent is at `(i-1)//2`.
- **Heap property:** every parent is ≤ its children. So the minimum is at the root. The rest isn't sorted.
- **Push:** add at the end, then swap upward while it's smaller than its parent. O(log n).
- **Pop:** move the last element to the root, then swap downward with its smaller child. O(log n).
- **heapify is O(n), not O(n log n):** most nodes are near the bottom and only move a short distance.

```python
import heapq
h = [5, 1, 8, 3]
heapq.heapify(h)          # h[0] == 1
heapq.heappush(h, 0)      # h[0] == 0
heapq.heappop(h)          # returns 0
heapq.nlargest(2, [5, 1, 8, 3])    # [8, 5]
heapq.nsmallest(2, [5, 1, 8, 3])   # [1, 3]
```

## 2. Kth Largest Element in a Stream (LC 703)
```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.h = nums[:]
        heapq.heapify(self.h)
        while len(self.h) > k:
            heapq.heappop(self.h)

    def add(self, val):
        heapq.heappush(self.h, val)
        if len(self.h) > self.k:
            heapq.heappop(self.h)       # throw away the smallest, which can't be in the top k
        return self.h[0]
```
**Invariant:** the heap holds the k largest values seen so far, so its minimum is the k-th largest.
Trace with k = 3, nums `[4,5,8,2]`: after heapify and trimming, the heap is `{4,5,8}`. add(3): push 3, pop 3, return 4. add(5): push 5, pop 4, the heap is `{5,5,8}`, return 5. add(10): the heap becomes `{5,8,10}`, return 5.

## 3. Last Stone Weight (LC 1046): max-heap by negating
```python
def lastStoneWeight(stones):
    h = [-s for s in stones]
    heapq.heapify(h)
    while len(h) > 1:
        a = -heapq.heappop(h)           # heaviest
        b = -heapq.heappop(h)           # second heaviest
        if a != b:
            heapq.heappush(h, -(a - b))
    return -h[0] if h else 0
```
Trace `[2,7,4,1,8,1]`: 8 and 7 leave 1 → `[4,2,1,1,1]`. 4 and 2 leave 2 → `[2,1,1,1]`. 2 and 1 leave 1 → `[1,1,1]`. 1 and 1 cancel → `[1]`. **Answer: 1.**

## 4. Kth Largest Element in an Array (LC 215)
```python
def findKthLargest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]
```
O(n log k). Alternatives: `heapq.nlargest(k, nums)[-1]`, sorting in O(n log n), or Quickselect, which averages O(n) but is O(n²) in the worst case. Mentioning Quickselect scores points.

## 5. K Closest Points to Origin (LC 973)
Keep the k **smallest** distances, using a max-heap of size k (distances negated):
```python
def kClosest(points, k):
    h = []
    for x, y in points:
        d = x * x + y * y               # compare squared distances, no sqrt needed
        heapq.heappush(h, (-d, x, y))
        if len(h) > k:
            heapq.heappop(h)            # removes the farthest
    return [[x, y] for _, x, y in h]
```
Or simply `heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)`.

## 6. Top K Frequent Elements (LC 347)
```python
from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```
O(n log k). The O(n) bucket version is in `hashmap/theory.md`.

## 7. Merge k sorted lists (LC 23): the tie-breaker trick
```python
def mergeKLists(lists):
    h = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(h, (node.val, i, node))   # i breaks ties, because ListNode can't be compared
    dummy = tail = ListNode()
    while h:
        _, i, node = heapq.heappop(h)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next
```
Without `i`, two equal values make Python compare the `ListNode` objects, which raises a `TypeError`. O(N log k), where N is the total number of nodes.

## 8. Two heaps (Find Median from Data Stream, LC 295)
Keep a max-heap for the smaller half and a min-heap for the larger half, with sizes differing by at most 1. The median comes from the tops. This is the standard hard follow-up. Know the idea even if you don't code it yet.

## 9. Decision table
| Question | Heap setup |
|---|---|
| k-th largest, or top k largest | min-heap of size k |
| k-th smallest, or k closest | max-heap of size k (negate) |
| Repeatedly take the biggest or smallest and put back a result | max-heap or min-heap of everything |
| Merge k sorted sources | min-heap of the current head of each (value, index, item) |
| Schedule the next event by time (meeting rooms, CPU tasks) | min-heap of end times |
| Running median | two heaps |
| Only ever need the minimum once | just `min()`, O(n) |

## 10. Common bugs
1. Forgetting that `heapq` is a min-heap, and getting the order backwards.
2. Negating on push but not on pop (or the reverse).
3. Pushing objects that can't be compared, without a tie-breaker.
4. Thinking `h` is sorted. Only `h[0]` is guaranteed. Use `sorted(h)` if you need the order.
5. Using a heap for top-k when the heap holds everything. That's O(n log n). Cap it at k.

## 11. Edge cases
- k equal to n, or k = 1
- Duplicate values
- An empty heap at the end (LC 1046 should return 0)
- Negative numbers when you negate for a max-heap (still works, but check your trace)

## 12. Interview prep
- **Purpose:** get the current extreme value fast while the data keeps changing.
- **Control flow:** push candidates. Whenever the size goes over k, pop the one that can no longer be in the answer. Read the root.
- **Complexity:** O(n log k) time and O(k) space for top-k. O(n) to heapify.
- **What a strong candidate says:** "I keep a min-heap of the k largest values seen. Anything smaller than the root can't be in the top k, so I pop it. That's O(n log k) time and O(k) space, and it works on a stream. For a one-off query on an array, Quickselect gives O(n) on average."
- **Likely follow-ups:** Task Scheduler (LC 621), Reorganize String (LC 767), Find Median from Data Stream (LC 295), Dijkstra's shortest path (a heap of `(distance, node)`).
