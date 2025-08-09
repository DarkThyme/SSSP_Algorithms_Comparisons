# SSSP_Algorithms_Comparisons
Comparison of Dijkstra and BMSSP shortest path algorithms on large sparse graphs with Python implementations and performance analysis.

This repository contains Python implementations of two Single-Source Shortest Path (SSSP) algorithms:

- **Dijkstra’s Algorithm**: Classical, widely-used algorithm with \(O(m + n \log n)\) complexity.
- **Bounded Multi-Source Shortest Path (BMSSP)**: A newer, theoretically faster algorithm that breaks Dijkstra’s bound on sparse graphs.

---

## Dataset

We use the [soc-LiveJournal1](https://snap.stanford.edu/data/soc-LiveJournal1.html) graph dataset, a large sparse directed graph with over 4 million nodes and edges. The graph is unweighted (or treated as having uniform weights) for simplicity.

The dataset file used: soc-LiveJournal1.txt

The file should be downloaded and placed locally, then its path configured in the code.

---

## Algorithms

### Dijkstra

- Classic priority-queue-based shortest path algorithm.
- Efficient and widely applicable.
- Our implementation uses Python's `heapq`.

### BMSSP (Bounded Multi-Source Shortest Path)

- Based on the paper: *“A deterministic \(O(m \log^{2/3} n)\)-time algorithm for SSSP on sparse graphs”*.
- Uses recursive divide-and-conquer, pivoting, and batch relaxation.
- Python implementation follows the pseudocode with parameters tuned for the dataset.
####PseudoCode
function BMSSP(l, B, S)
// l: recursion level
// B: upper bound distance
// S: set of complete vertices
if l == 0 then
return BASECASE(B, S)
(P, W) ← FINDPIVOTS(B, S)
Initialize data structure D with parameter M = 2^{(l−1) * t} and bound B
for each x in P do
    D.INSERT((x, d[x]))

i ← 0
B' ← min_{x in P} d[x]
U ← empty set

while |U| < k * 2^{l * t} and D is not empty do
    i ← i + 1
    (B_i, S_i) ← D.PULL()
    (B'_i, U_i) ← BMSSP(l − 1, B_i, S_i)
    U ← U ∪ U_i

    K ← empty set
    for each edge (u, v) where u ∈ U_i do
        if d[u] + w(u, v) ≤ d[v] then
            d[v] ← d[u] + w(u, v)
            if d[u] + w(u, v) ∈ [B_i, B) then
                D.INSERT((v, d[v]))
            else if d[u] + w(u, v) ∈ [B'_i, B_i) then
                K ← K ∪ {(v, d[v])}
    D.BATCHPREPEND(K ∪ {(x, d[x]) : x ∈ S_i and d[x] ∈ [B'_i, B_i)})

return min(B', B), U ∪ {x ∈ W : d[x] < min(B', B)}

---

## Findings

- Dijkstra completes in ~30-35 seconds on the dataset, visiting over 4.4 million nodes.
- BMSSP is slower in our current Python implementation (~225 seconds) due to recursion overhead and Python inefficiencies.
- BMSSP visits all reachable nodes correctly, confirming correctness.
- Theoretically, BMSSP beats Dijkstra asymptotically on sparse graphs, but practical speedups require low-level optimizations and advanced data structures.
- Future work could include optimized C++ implementations or parameter tuning.

---

## Usage

1. Download and place the dataset locally.
2. Update the file path in each script to point to the dataset.
3. Run the scripts individually to test and compare runtimes.

---

## Files

- `Djikstra`: Python implementation of Dijkstra's algorithm.
- `BMSSP.py`: Python implementation of BMSSP algorithm following the pseudocode.

---


## References

- [Network Repository](https://networkrepository.com/)
- [Stanford SNAP: soc-LiveJournal1](https://snap.stanford.edu/data/soc-LiveJournal1.html)
- [Breaking the Sorting Barrier for Directed Single-Source Shortest Paths](https://www.alphaxiv.org/abs/2504.17033?s=08)
