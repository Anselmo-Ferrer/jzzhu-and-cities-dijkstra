"""
Dijkstra a partir de um vertice fonte com uma variacao de desempate:
quando dois caminhos minimos para um mesmo vertice tem o mesmo custo,
preferimos o que termina em uma aresta de estrada em vez de uma rota
de trem. Isso e exatamente o que o problema F (CF 449B) precisa para
decidir quais rotas de trem sao redundantes.

A estrutura segue `algs4-py/algs4/dijkstra_sp.py` (classe `DijkstraSP`,
atributos `dist_to`, relaxamento de arestas, fila de prioridade), mas:

- usa `heapq` em vez de `IndexMinPQ` (heap binaria preguicosa), porque
  `IndexMinPQ` daquela base tem operacoes O(n) em `contains` e
  `del_min` que nao escalam para n = 10^5;
- mantem um vetor `used_train[v]` indicando se a melhor rota conhecida
  ate `v` termina em aresta de trem. O vetor e atualizado tanto em
  relaxamentos estritamente menores quanto em empates (estrada vence
  trem).

A logica principal (inicializacao de distancias, relaxamento, condicao
de parada e desempate) e implementada aqui pelo grupo, conforme exige
o enunciado do trabalho.
"""

import heapq

INF = float("inf")


class DijkstraSP:
    def __init__(self, graph, source):
        n = graph.V
        self.dist_to = [INF] * (n + 1)
        self.used_train = [False] * (n + 1)

        self.dist_to[source] = 0
        # Heap binaria preguicosa: pode haver entradas obsoletas (com
        # distancia maior que `dist_to[u]` atual). Elas sao descartadas
        # com o teste `d > self.dist_to[u]` ao serem extraidas.
        pq = [(0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > self.dist_to[u]:
                continue
            self._relax(graph, u, d, pq)

    def _relax(self, graph, u, d, pq):
        # Relaxa todas as arestas incidentes a `u`.
        for (v, weight, is_train) in graph.adj[u]:
            nd = d + weight
            if nd < self.dist_to[v]:
                # Caminho estritamente melhor encontrado.
                self.dist_to[v] = nd
                self.used_train[v] = is_train
                heapq.heappush(pq, (nd, v))
            elif nd == self.dist_to[v] and self.used_train[v] and not is_train:
                # Caminho de mesma distancia, mas via estrada. Preferimos
                # estrada porque qualquer trem com peso == dist[v] passa
                # a ser redundante. Nao precisamos reempilhar `v`: o
                # custo final nao mudou; apenas o "rotulo" da entrada.
                self.used_train[v] = False

    def has_path_to(self, v):
        return self.dist_to[v] < INF
