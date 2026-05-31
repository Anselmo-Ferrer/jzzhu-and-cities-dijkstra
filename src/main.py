"""
Codeforces 449B - Jzzhu and Cities
Grupo F - Trabalho Pratico 2, Unidade 3

Modelagem:
- Cada cidade e um vertice (1..n). A capital e o vertice 1.
- Cada estrada vira uma aresta nao-direcionada do tipo `road` com o
  peso informado.
- Cada rota de trem vira uma aresta nao-direcionada do tipo `train`
  entre a capital (vertice 1) e a cidade de destino.

Antes de rodar Dijkstra, deduplicamos rotas de trem que chegam na
mesma cidade: para cada cidade `s`, mantemos apenas a rota de trem
com menor peso. As demais ja podem ser fechadas (pois sao dominadas
por uma rota igual ou mais curta). Esse numero de descartes vai para
`duplicates_removed`.

Rodamos uma variante de Dijkstra a partir do vertice 1 que, em caso
de empate na distancia minima, prefere terminar o caminho em uma
aresta de estrada (`used_train[v] = False`). Apos o algoritmo,
`used_train[s]` indica se a melhor distancia a `s` exige de fato
uma aresta de trem.

A resposta e o numero de trens descartados na deduplicacao mais o
numero de cidades cuja melhor distancia ja e atingida por estradas
(ou seja, cidades onde a rota de trem restante e desnecessaria).
"""

import sys

from edge import Edge
from edge_weighted_graph import EdgeWeightedGraph
from dijkstra_sp import DijkstraSP


def solve(input_bytes):
    data = input_bytes.split()
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

    # Deduplicacao: para cada cidade destino do trem, manter apenas
    # a rota de menor peso. As outras sao removiveis "de graca".
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

    answer = duplicates_removed + (len(min_train) - needed_trains)
    return answer


def main():
    data = sys.stdin.buffer.read()
    print(solve(data))


if __name__ == "__main__":
    main()
