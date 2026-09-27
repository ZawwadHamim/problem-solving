# Stack, in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** LIFO.
**One sentence:** A stack remembers unfinished items in the order they must be finished, most recent first, which fits anything nested or anything waiting for its next greater or smaller value.

## Executive summary
- **Operations:** push, pop and peek are all O(1). In Python, a list: `append`, `pop()`, `st[-1]`.
- **Shape 1, matching:** brackets, tags, undo. Push when something opens, pop when it closes.
- **Shape 2, evaluating:** Reverse Polish Notation (RPN), calculators. Push operands, pop two when you see an operator.
- **Shape 3, extra information:** Min Stack stores each value with the minimum at the time it was pushed.
- **Shape 4, monotonic stack:** keep the stack increasing or decreasing to find the "next greater" or "previous smaller" element for every index in O(n) total.
- **Also:** DFS is a stack, and recursion uses the call stack.

---

## 1. Matching: Valid Parentheses (LC 20)
```python
def isValid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in pairs:                          # a closing bracket
            if not st or st[-1] != pairs[ch]:
                return False
            st.pop()
        else:                                    # an opening bracket
            st.append(ch)
    return not st                                # anything left open means invalid
```
Trace `"([)]"`: push `(`, push `[`, then `)` arrives but the top is `[`, which doesn't match, so return False.
Trace `"({})"`: push `(`, push `{`, `}` matches and pops, `)` matches and pops, and the stack is empty, so return True.
**Invariant:** the stack holds exactly the brackets that are open and not yet closed, most recent on top.

## 2. Extra information: Min Stack (LC 155)
```python
class MinStack:
    def __init__(self):
        self.st = []                              # (value, min at or below this item)

    def push(self, val):
        m = min(val, self.st[-1][1]) if self.st else val
        self.st.append((val, m))

    def pop(self):
        self.st.pop()

    def top(self):
        return self.st[-1][0]

    def getMin(self):
        return self.st[-1][1]
```
Every operation is O(1). Each item stores the minimum of everything below it, so popping automatically brings back the previous minimum.

## 3. Evaluating: Evaluate Reverse Polish Notation (LC 150)
```python
def evalRPN(tokens):
    st = []
    for t in tokens:
        if t in {'+', '-', '*', '/'}:
            b = st.pop()                          # the second operand comes off first
            a = st.pop()
            if t == '+': st.append(a + b)
            elif t == '-': st.append(a - b)
            elif t == '*': st.append(a * b)
            else: st.append(int(a / b))           # truncate toward zero, not floor
        else:
            st.append(int(t))
    return st[0]
```
**Bug to avoid:** `a // b` rounds down (−7 // 2 = −4), but the problem wants rounding toward zero (−3). Use `int(a / b)`.

## 4. Monotonic stack: Daily Temperatures (LC 739)
**Question:** for each day, how many days until a warmer one?
**Idea:** keep a stack of indices still waiting for a warmer day. Their temperatures are decreasing from bottom to top. A new temperature pops every waiting day that's colder, and those days have found their answer.
```python
def dailyTemperatures(t):
    res = [0] * len(t)
    st = []                                       # indices, temperatures decreasing
    for i, x in enumerate(t):
        while st and t[st[-1]] < x:
            j = st.pop()
            res[j] = i - j
        st.append(i)
    return res
```
Trace `[73, 74, 75, 71, 69, 72, 76, 73]`:
| i | temp | pops (and their answers) | stack after (temps) |
|---|---|---|---|
| 0 | 73 | — | [73] |
| 1 | 74 | day 0 → 1 | [74] |
| 2 | 75 | day 1 → 1 | [75] |
| 3 | 71 | — | [75, 71] |
| 4 | 69 | — | [75, 71, 69] |
| 5 | 72 | day 4 → 1, day 3 → 2 | [75, 72] |
| 6 | 76 | day 5 → 1, day 2 → 4 | [76] |
| 7 | 73 | — | [76, 73] |

Result: `[1, 1, 4, 2, 1, 1, 0, 0]`. Days left on the stack never find a warmer day and keep 0.
**Why O(n) with a nested loop:** each index is pushed once and popped at most once, so there are 2n operations in total.

## 5. Next Greater Element I (LC 496)
Same idea, with a map from each value to its next greater value:
```python
def nextGreaterElement(nums1, nums2):
    nxt = {}
    st = []
    for x in nums2:
        while st and st[-1] < x:
            nxt[st.pop()] = x
        st.append(x)
    return [nxt.get(x, -1) for x in nums1]
```

## 6. Which monotonic stack to use
| You want, for each element… | Loop direction | Stack keeps | Pop while |
|---|---|---|---|
| Next greater to the right | left → right | decreasing | top < current |
| Next smaller to the right | left → right | increasing | top > current |
| Previous greater to the left | left → right | decreasing | top <= current, then the top is the answer |
| Previous smaller to the left | left → right | increasing | top >= current, then the top is the answer |

Harder problems built on this: Largest Rectangle in Histogram (LC 84, previous and next smaller), Trapping Rain Water (LC 42), Car Fleet (LC 853), Online Stock Span (LC 901).

## 7. Decision table
| Signal | Shape |
|---|---|
| Nested structure, open and close pairs | Matching |
| Postfix expression, "evaluate" | Evaluating |
| O(1) min or max while pushing and popping | Store extra info per item |
| "Next / previous greater / smaller", "days until", "span" | Monotonic stack |
| First in, first out (queue order) needed | `collections.deque`, not a stack |

## 8. Common bugs
1. Popping from an empty stack. Always check `if st` first.
2. Forgetting the final `return not st`, so `"(("` passes.
3. RPN: getting the operand order wrong (`b` is popped first) or using floor division.
4. Monotonic stack: storing values when you need distances. Store indices, since you can always look up the value from an index.
5. Using `list.pop(0)` as a queue, which is O(n). Use `deque.popleft()`.

## 9. Edge cases
- Empty string, and a single character
- Only closing brackets, e.g. `")"`
- Strictly increasing or decreasing temperatures
- Equal values: decide whether "greater" means strictly greater

## 10. Interview prep
- **Purpose:** handle nesting and "what's the nearest bigger or smaller one?" in one pass.
- **Control flow:** scan once. When the current item resolves the top of the stack, pop and record. Then push the current item.
- **Complexity:** O(n) time, because each item is pushed and popped at most once. O(n) space in the worst case.
- **What a strong candidate says:** "I keep a stack of indices still waiting for a greater element, so it stays decreasing. Each new element pops everything smaller, and those indices have their answer. Each index is pushed and popped once, so it's O(n) even with the inner loop."
- **Likely follow-ups:** Largest Rectangle in Histogram (LC 84), Basic Calculator (LC 224), Decode String (LC 394), a queue built from two stacks (LC 232).
