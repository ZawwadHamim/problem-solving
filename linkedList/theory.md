# Linked list, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** Rewiring.
**One sentence:** Linked-list problems come down to moving a few pointers in the right order, and a dummy head, the fast/slow technique and "save `next` before you overwrite it" handle almost all of them.

## Executive summary
- **The structure:** each node has a `val` and a `next`. Access is O(n), but inserting or deleting at a known node is O(1).
- **Four tools:**
  1. **Save next first:** `nxt = cur.next` before changing `cur.next`.
  2. **Dummy head:** a fake node before the real head, so deleting or inserting at the head needs no special case.
  3. **Fast and slow pointers:** fast moves 2 steps, slow moves 1. Used for the middle, cycle detection, and the start of a cycle.
  4. **Gap pointers:** move one pointer n steps ahead, then move both together. Used for "n-th from the end".
- **Draw it.** Most bugs are a pointer changed in the wrong order. Sketch the boxes and arrows for 3 nodes before writing code.

---

## 0. Helpers for local testing (LeetCode provides `ListNode`)
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out
```

## 1. Reverse Linked List (LC 206)
```python
def reverseList(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next      # 1. save
        cur.next = prev     # 2. reverse this node's arrow
        prev = cur          # 3. move prev forward
        cur = nxt           # 4. move cur forward
    return prev
```
Trace `1 → 2 → 3`:
| step | prev | cur | reversed part so far |
|---|---|---|---|
| start | None | 1 | — |
| 1 | 1 | 2 | 1 → None |
| 2 | 2 | 3 | 2 → 1 → None |
| 3 | 3 | None | 3 → 2 → 1 → None |

**Invariant:** `prev` is the head of the reversed part, and `cur` is the head of the part not yet reversed.
Recursive version: `rest = reverseList(head.next); head.next.next = head; head.next = None; return rest`, with a base case of an empty list or one node. That's O(n) stack space.

## 2. Merge Two Sorted Lists (LC 21), with a dummy head
```python
def mergeTwoLists(a, b):
    dummy = ListNode()
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a or b          # attach whatever is left
    return dummy.next
```
The dummy means you never have to ask "is this the first node?".

## 3. Linked List Cycle (LC 141): Floyd's algorithm
```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```
**Why they must meet:** once both are inside the cycle, fast gains 1 node on slow each step. The gap shrinks by 1 every step, so it reaches 0. O(n) time, O(1) space. A `set` of visited nodes also works, but needs O(n) space.
**Where the cycle starts (LC 142):** after they meet, move one pointer back to `head`, then move both one step at a time. They meet at the cycle's start. The distance from the head to the start equals the distance from the meeting point onward to the start, going around the cycle.

## 4. Middle of the Linked List (LC 876)
```python
def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow                 # with an even length, this is the second of the two middles
```

## 5. Remove Nth Node From End (LC 19): gap pointers
```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):      # put a gap of n nodes between them
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next  # slow is just before the node to remove
    return dummy.next
```
**Why a dummy:** when n equals the list length, the head itself is removed, and `slow` stays on the dummy.

## 6. Reorder List (LC 143): combining the tools
Find the middle (fast and slow), reverse the second half (LC 206), then weave the two halves together (similar to LC 21). A common interview question because it tests all three tools at once.

## 7. Decision table
| Question | Tool |
|---|---|
| Reverse all or part of the list | prev / cur / nxt |
| Build a new list, or delete that might remove the head | Dummy head |
| Cycle? Middle? | Fast and slow |
| k-th from the end | Gap of k |
| Palindrome list | Middle, reverse second half, compare |
| Intersection of two lists (LC 160) | Two pointers that switch lists when they reach the end |

## 8. Common bugs
1. Losing the rest of the list by overwriting `cur.next` before saving it.
2. `fast.next.next` when `fast.next` is None. The loop condition must be `fast and fast.next`.
3. Returning `head` instead of `dummy.next` after the head was removed.
4. Comparing nodes with `==` when you mean the same object. Use `is`.
5. An infinite loop after rewiring (a cycle you created by accident). Set the last node's `next` to None.

## 9. Edge cases
- Empty list (`head = None`)
- One node, and two nodes
- Removing the head, and removing the tail
- Even and odd lengths for the middle

## 10. Interview prep
- **Purpose:** restructure data in place in O(1) extra space by changing references instead of copying.
- **Control flow:** walk with one or two pointers, save the next node, rewire, and advance.
- **Complexity:** almost always O(n) time and O(1) space. Recursive solutions add O(n) stack space.
- **What a strong candidate says:** "I'll use a dummy head so removing the first node isn't a special case. I save `next` before changing any pointer. For the cycle, fast gains one step per iteration inside the loop, so they must meet, with O(1) space."
- **Likely follow-ups:** Reverse Nodes in k-Group (LC 25), Copy List with Random Pointer (LC 138), LRU Cache (LC 146, a hash map plus a doubly linked list), Add Two Numbers (LC 2).
