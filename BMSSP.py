import heapq
import math
import sys

sys.setrecursionlimit(10**7)

class DStructure:
    """
    Simulates D data structure from pseudocode with priority queue behavior.
    Supports INSERT, PULL (pop min), and BATCHPREPEND (add many at front).
    """
    def __init__(self, M, B):
        self.heap = []
        self.M = M  #parameter (unused in this simplified version)
        self.B = B

    def insert(self, item):
        #item = (vertex, distance)
        heapq.heappush(self.heap, (item[1], item[0]))

    def pull(self):
        if self.heap:
            dist, vertex = heapq.heappop(self.heap)
            return dist, {vertex}
        else:
            return None, set()

    def batch_prepend(self, items):
        #items: iterable of (vertex, dist)
        for v, d in items:
            heapq.heappush(self.heap, (d, v))

    def empty(self):
        return len(self.heap) == 0


def base_case(B, S, bd, adj, k):
    """
    Algorithm 2 BaseCase(B, S)
    S is singleton set {x}
    """
    U0 = set(S)
    heap = []
    for x in S:
        heapq.heappush(heap, (bd[x], x))

    while heap and len(U0) < k + 1:
        d_u, u = heapq.heappop(heap)
        U0.add(u)
        for v, w in adj.get(u, []):
            nd = bd[u] + w
            if nd < bd.get(v, float('inf')) and nd < B:
                bd[v] = nd
                heapq.heappush(heap, (nd, v))

    if len(U0) <= k:
        return B, U0
    else:
        B_prime = max(bd[v] for v in U0)
        U_prime = {v for v in U0 if bd[v] < B_prime}
        return B_prime, U_prime


def find_pivots(B, S, bd, l, t):
    """
    Splits S into pivots P and remainder W.
    For simplicity, split roughly in half by distance.
    """
    if len(S) <= 1:
        return S, set()
    S_sorted = sorted(S, key=lambda x: bd[x])
    half = len(S_sorted) // 2
    P = set(S_sorted[:half])
    W = set(S_sorted[half:])
    return P, W


def bmssp(l, B, S, bd, adj, k, t):
    """
    Algorithm 3 BMSSP(l, B, S)
    Inputs:
    - l: recursion level
    - B: upper bound distance
    - S: set of complete vertices
    - bd: dict vertex -> tentative distance
    - adj: adjacency list {u: [(v,w), ...]}
    - k, t: algorithm parameters
    Returns:
    - B_prime <= B: updated boundary
    - U: set of complete vertices after expansion
    """
    if l == 0:
        return base_case(B, S, bd, adj, k)

    P, W = find_pivots(B, S, bd, l, t)
    M = 2 ** ((l - 1) * t)
    D = DStructure(M, B)

    #Insert pivots into D
    for x in P:
        D.insert((x, bd[x]))

    i = 0
    B_prime = min((bd[x] for x in P), default=B)
    U = set()

    while len(U) < k * (2 ** (l * t)) and not D.empty():
        i += 1
        Bi, Si = D.pull()
        if Bi is None:
            break
        B_i_prime, U_i = bmssp(l - 1, Bi, Si, bd, adj, k, t)
        U.update(U_i)

        K = set()
        for u in U_i:
            for v, w in adj.get(u, []):
                nd = bd[u] + w
                if nd < bd.get(v, float('inf')):
                    bd[v] = nd
                    if Bi <= nd < B:
                        D.insert((v, nd))
                    elif B_i_prime <= nd < Bi:
                        K.add((v, nd))
        #Batch prepend K and elements of Si with distances in [B_i_prime, Bi)
        batch_items = list(K) + [(x, bd[x]) for x in Si if B_i_prime <= bd[x] < Bi]
        D.batch_prepend(batch_items)

    B_prime = min(B_prime, B)
    U.update({x for x in W if bd[x] < B_prime})
    return B_prime, U


def run_bmssp(adj, source):
    n = len(adj)
    k = int(math.floor(n ** (1 / 3))) or 1
    t = int(math.floor(n ** (2 / 3))) or 1
    bd = {v: float('inf') for v in adj}
    bd[source] = 0.0

    #Initialize S with source and neighbors for better expansion
    S = {source}
    for v, _ in adj.get(source, []):
        S.add(v)

    L = int(math.ceil(math.log(n + 1) / (t + 1)))  # avoid division by zero

    B = float('inf')
    B_prime, U = bmssp(L, B, S, bd, adj, k, t)
    return bd


if __name__ == "__main__":
    GRAPH_FILE_PATH = r"D:\soc-LiveJournal1.txt\soc-LiveJournal1.txt"

    #Simple graph loader for edge list (adjust for your file format)
    def load_graph(file_path):
        adj = {}
        with open(file_path, "r") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                u, v = int(parts[0]), int(parts[1])
                w = 1.0  #assuming unweighted or uniform weight
                adj.setdefault(u, []).append((v, w))
        return adj

    print("Loading graph...")
    adj = load_graph(GRAPH_FILE_PATH)
    print(f"Graph loaded: {len(adj)} nodes.")

    import time
    source_node = 0

    print(f"Running BMSSP from node {source_node} ...")
    start = time.time()
    dist_bmssp = run_bmssp(adj, source_node)
    dt = time.time() - start

    visited = sum(1 for d in dist_bmssp.values() if d < float('inf'))
    print(f"BMSSP took {dt:.2f} sec, visited {visited} nodes.")
