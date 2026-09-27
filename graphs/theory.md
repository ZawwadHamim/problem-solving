# Graphs (BFS, DFS, topological sort), in full

## Pattern card (fill from memory, don't copy from below)
- Trigger:
- Invariant:
- Template/pseudocode from memory:
- Complexity:
- Solved/re-solved:
- Mistake and correction:

---

**One word:** Traversal.
**One sentence:** Visit every reachable node exactly once by keeping a `visited` set, using DFS to explore regions and BFS to find the fewest steps.

## Executive summary
- **What a graph is:** nodes plus edges. Interviews give it as an edge list, an adjacency list, or **a grid, where each cell connects to its 4 neighbours**.
- **The key rule:** mark a node visited **when you add it** to the stack or queue, not when you pop it. Otherwise it gets added twice.
- **DFS:** recursion or a stack. Use it for connected components, flood fill and cycle detection.
- **BFS:** a queue. Gives the **shortest path in an unweighted graph** and processes things level by level ("minutes", "steps").
- **Multi-source BFS:** start with every source in the queue at once (e.g. all the rotten oranges).
- **Topological sort (Kahn's algorithm):** repeatedly take a node with in-degree 0. If you can't take all n nodes, there's a cycle. Used for course schedules and build orders.
- **Cost:** O(V + E), where V is the number of nodes and E the number of edges. For an m×n grid, that's O(m·n).

---

## 1. Representations
```python
from collections import defaultdict, deque

edges = [[0, 1], [1, 2], [2, 0]]
adj = defaultdict(list)
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)             # leave this out for a directed graph

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))   # grid neighbours
```

## 2. Flood Fill (LC 733): DFS on a grid
```python
def floodFill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image             # otherwise it recurses forever: filled cells still look "old"
    m, n = len(image), len(image[0])
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or image[r][c] != old:
            return
        image[r][c] = color      # recolouring IS the visited mark
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    dfs(sr, sc)
    return image
```

## 3. Number of Islands (LC 200): counting connected components
```python
def numIslands(grid):
    m, n = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return
        grid[r][c] = '0'         # sink it = mark visited
        for dr, dc in DIRS:
            dfs(r + dr, c + dc)
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                count += 1       # a new island, then sink all of it
                dfs(r, c)
    return count
```
Trace:
```
1 1 0      the first '1' at (0,0) sinks (0,0),(0,1),(1,0)  → count 1
1 0 0      the next unvisited '1' is (2,2)                   → count 2
0 0 1
```
**Invariant:** every land cell already seen is `'0'`, so each island is counted once.
Max Area of Island (LC 695) is the same, except `dfs` returns `1 + sum of neighbours`.

## 4. BFS for the fewest steps: Rotting Oranges (LC 994), multi-source
```python
def orangesRotting(grid):
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2:
                q.append((r, c))                 # every rotten orange starts at minute 0
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):                  # one level = one minute
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2             # mark when enqueuing
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes
```
Trace `[[2,1,1],[1,1,0],[0,1,1]]`: minute 1 rots (0,1) and (1,0). Minute 2 rots (0,2) and (1,1). Minute 3 rots (2,1). Minute 4 rots (2,2). **Answer: 4.**
**Why BFS gives the shortest path:** it finishes every node at distance d before touching distance d+1, so the first time you reach a node is by the shortest route.

## 5. Plain BFS shortest path on a graph
```python
def shortest_path(adj, src, dst):
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            return dist[u]
        for v in adj[u]:
            if v not in dist:            # dist doubles as the visited set
                dist[v] = dist[u] + 1
                q.append(v)
    return -1
```

## 6. Course Schedule (LC 207): topological sort with Kahn's algorithm
`[a, b]` means "to take a, you must first take b", so the edge goes b → a.
```python
def canFinish(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:            # all of v's prerequisites are done
                q.append(v)
    return done == numCourses            # anything left over is stuck in a cycle
```
- Course Schedule II (LC 210): return the order in which nodes were popped.
- **DFS alternative:** give each node 3 states (unvisited, visiting, done). Reaching a "visiting" node means there's a cycle.

## 7. Clone Graph (LC 133): a map from each original node to its copy
```python
def cloneGraph(node):
    if not node:
        return None
    copies = {node: Node(node.val)}
    q = deque([node])
    while q:
        u = q.popleft()
        for v in u.neighbors:
            if v not in copies:
                copies[v] = Node(v.val)
                q.append(v)
            copies[u].neighbors.append(copies[v])
    return copies[node]
```

## 8. Decision table
| Question | Tool |
|---|---|
| How many regions or islands? | DFS or BFS from each unvisited cell |
| Fewest steps or minutes (unweighted) | BFS, level by level |
| Spreading from many sources at once | Multi-source BFS |
| Order with dependencies, "is it possible?" | Topological sort (Kahn) |
| Cycle in a directed graph | Kahn (done < n) or DFS with 3 states |
| Shortest path with weights | Dijkstra (heap), outside this roadmap |
| Dynamic connectivity, "are these connected?" | Union-find, outside this roadmap |

## 9. Common bugs
1. Marking visited when popping instead of when pushing, so nodes get enqueued many times.
2. Flood fill when `old == color`, which recurses forever.
3. Forgetting bounds checks, or checking them after indexing into the grid.
4. Getting the edge direction backwards in Course Schedule.
5. Recursion depth on a 300×300 grid (90,000 cells). Use BFS or an explicit stack.
6. Counting minutes one too many (check `while q and fresh`).

## 10. Edge cases
- An empty grid, or a 1×1 grid
- No land, or all land
- A disconnected graph (loop over every node, not just node 0)
- No fresh oranges at the start (answer 0)
- Self-loops and duplicate edges

## 11. Interview prep
- **Purpose:** explore connectivity and shortest distances in networks, grids and dependency lists.
- **Control flow:** build the adjacency list. For each unvisited node, start a traversal. Mark visited when adding, and add the unvisited neighbours.
- **Complexity:** O(V + E) time, O(V) space for the visited set and the queue or stack.
- **What a strong candidate says:** "I treat the grid as a graph where each cell has 4 edges. I scan every cell, and each unvisited land cell starts a new island, which I sink with DFS so it isn't counted again. Every cell is processed a constant number of times, so it's O(m·n)."
- **Likely follow-ups:** Pacific Atlantic Water Flow (LC 417), Surrounded Regions (LC 130), Word Ladder (LC 127, BFS), Network Delay Time (LC 743, Dijkstra), Redundant Connection (LC 684, union-find).
