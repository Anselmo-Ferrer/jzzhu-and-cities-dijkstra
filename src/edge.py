"""
Aresta ponderada nao-direcionada com um campo extra `kind` que indica
se a aresta representa uma estrada (`'road'`) ou uma rota de trem
(`'train'`).

Estrutura baseada em `algs4-py/algs4/edge.py`, com os metodos
`either()` e `other(v)` da convencao de Sedgewick.
"""


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
        raise ValueError("vertex %d is not in edge (%d, %d)" % (vertex, self.v, self.w))

    def is_train(self):
        return self.kind == Edge.TRAIN

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return "%d-%d (%d, %s)" % (self.v, self.w, self.weight, self.kind)
