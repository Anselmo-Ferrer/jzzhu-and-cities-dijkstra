"""
Versao em arquivo unico do `main.py` para submissao no Codeforces
(449B - Jzzhu and Cities). Cola, em ordem, o conteudo dos modulos:

  edge.py
  edge_weighted_graph.py
  dijkstra_sp.py
  main.py (corpo da funcao `solve`)

A logica e identica a versao modular em `src/main.py` - este arquivo
existe apenas para permitir copiar/colar em uma unica submissao.
"""

import sys
import heapq

INF = float("inf")


class Edge:
    __slots__ = ("v", "w", "weight", "kind")
    ROAD = "road"
    TRAIN = "train"

    def __init__(self, v, w, weight, kind=ROAD):
        self.v = v
        self.w = w
        self.weight = weight
        self.kind = kind

    def either(self):
        return self.v

    def other(self, vertex):
        if vertex == self.v:
            return self.w
        if vertex == self.w:
            return self.v
        raise ValueError("vertex %d nao pertence a aresta" % vertex)

    def is_train(self):
        return self.kind == Edge.TRAIN


class EdgeWeightedGraph:
    def __init__(self, v):
        self.V = v
        self.E = 0
        self.adj = [[] for _ in range(v + 1)]

    def add_edge(self, e):
        v = e.either()
        w = e.other(v)
        is_train = e.is_train()
        self.adj[v].append((w, e.weight, is_train))
        self.adj[w].append((v, e.weight, is_train))
        self.E += 1


class DijkstraSP:
    def __init__(self, graph, source):
        n = graph.V
        self.dist_to = [INF] * (n + 1)
        self.used_train = [False] * (n + 1)
        self.dist_to[source] = 0
        pq = [(0, source)]
        adj = graph.adj
        dist_to = self.dist_to
        used_train = self.used_train

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist_to[u]:
                continue
            for (v, weight, is_train) in adj[u]:
                nd = d + weight
                if nd < dist_to[v]:
                    dist_to[v] = nd
                    used_train[v] = is_train
                    heapq.heappush(pq, (nd, v))
                elif nd == dist_to[v] and used_train[v] and not is_train:
                    used_train[v] = False


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1

    graph = EdgeWeightedGraph(n)

    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        x = int(data[idx]); idx += 1
        graph.add_edge(Edge(u, v, x, Edge.ROAD))

    min_train = {}
    duplicates_removed = 0
    for _ in range(k):
        s = int(data[idx]); idx += 1
        y = int(data[idx]); idx += 1
        if s in min_train:
            duplicates_removed += 1
            if y < min_train[s]:
                min_train[s] = y
        else:
            min_train[s] = y

    for s, y in min_train.items():
        graph.add_edge(Edge(1, s, y, Edge.TRAIN))

    sp = DijkstraSP(graph, 1)

    needed_trains = 0
    for s in min_train:
        if sp.used_train[s]:
            needed_trains += 1

    print(duplicates_removed + (len(min_train) - needed_trains))


if __name__ == "__main__":
    main()
