"""
Grafo nao-direcionado ponderado por listas de adjacencia.

Estrutura baseada em `algs4-py/algs4/edge_weighted_graph.py`, com duas
adaptacoes praticas para o problema F (Codeforces 449B):

1. Vertices sao indexados a partir de 1 (como no enunciado);
2. As listas de adjacencia armazenam tuplas leves
   `(outro_vertice, peso, eh_trem)` em vez de objetos `Edge`. Isso
   reduz overhead de atributos no laco quente do Dijkstra. A classe
   `Edge` ainda e usada na API de `add_edge` por clareza.
"""

from edge import Edge


class EdgeWeightedGraph:
    def __init__(self, v):
        self.V = v
        self.E = 0
        # adj[v] = lista de (outro, peso, eh_trem)
        self.adj = [[] for _ in range(v + 1)]

    def add_edge(self, e):
        v = e.either()
        w = e.other(v)
        is_train = e.is_train()
        self.adj[v].append((w, e.weight, is_train))
        self.adj[w].append((v, e.weight, is_train))
        self.E += 1

    def __str__(self):
        lines = ["%d vertices, %d arestas" % (self.V, self.E)]
        for u in range(1, self.V + 1):
            partes = ["%d(%d,%s)" % (w, peso, "T" if t else "R") for (w, peso, t) in self.adj[u]]
            lines.append("%d: %s" % (u, " ".join(partes)))
        return "\n".join(lines)
