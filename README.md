# Trabalho Pratico 2 - Unidade 3 - Grupo F

**Disciplina:** Resolucao de Problemas com Grafos

**Orientador:** Prof. Me Ricardo Carubbi

## Problema

- **Nome:** Codeforces 449B - Jzzhu and Cities
- **Link:** <https://codeforces.com/problemset/problem/449/B>
- **Foco da unidade:** Dijkstra com analise de arestas redundantes e
  alternativas especiais.

## Integrantes

| Nome | Matricula |
| --- | --- |
| Anselmo Teixeira | 2410414 |
| Joao Marcelo Juca | 2410392 |
| Thiago Victor Ferreira | 2410413 |

## Linguagem

Python 3 (testado com `python 3.11`). Em caso de TLE em Python puro
no Codeforces, submeter pelo selector **PyPy 3** - o codigo nao usa
bibliotecas exoticas e roda igual em ambos os interpretadores.

## Estrutura do repositorio

```text
projeto/
|-- README.md
|-- src/
|   |-- main.py                 # entrada do programa: le stdin e imprime resposta
|   |-- edge.py                 # classe Edge (estrada ou trem)
|   |-- edge_weighted_graph.py  # grafo nao-direcionado com listas de adjacencia
|   |-- dijkstra_sp.py          # Dijkstra com desempate estrada > trem
|   `-- main_codeforces.py      # versao em arquivo unico para submissao no CF
|-- evidencias/
|   `-- accepted.png            # print do Accepted no Codeforces
|-- apresentacao/
|   `-- apresentacao.pdf        # slides da apresentacao
`-- dados/
    |-- entradas_do_problema.txt
    |-- exemplo1.txt
    `-- exemplo2.txt
```

## Como executa

```bash
# Exemplo 1 do enunciado (resposta esperada: 2)
python3 src/main.py < dados/exemplo1.txt

# Exemplo 2 do enunciado (resposta esperada: 2)
python3 src/main.py < dados/exemplo2.txt
```

O programa le toda a entrada por `stdin` (formato identico ao do
Codeforces) e imprime apenas o numero maximo de rotas de trem que
podem ser fechadas.

### Versao para submissao no Codeforces

O Codeforces aceita apenas **um arquivo por submissao**. O arquivo
[`src/main_codeforces.py`](src/main_codeforces.py) e exatamente o
mesmo algoritmo, ja consolidado em um unico arquivo. Para conferir
que produz a mesma saida:

```bash
python3 src/main_codeforces.py < dados/exemplo1.txt
python3 src/main_codeforces.py < dados/exemplo2.txt
```

## Modelagem do problema como grafo

- **Vertices:** cada cidade `i` em `1..n`. A capital e o vertice `1`.
- **Arestas:** todas as arestas sao nao-direcionadas e ponderadas.
  - Cada estrada `(u, v, x)` vira uma aresta de tipo `road` com peso
    `x` entre `u` e `v`.
  - Cada rota de trem `(s, y)` vira uma aresta de tipo `train` com
    peso `y` entre a capital `1` e a cidade `s`.
- **Pesos:** os pesos sao os comprimentos informados no enunciado.
  Todos sao inteiros positivos (`1 <= x, y <= 1e9`), portanto Dijkstra
  e aplicavel (nao ha pesos negativos). As distancias podem chegar a
  ~1e14, mas Python ja trabalha com inteiros de precisao arbitraria.
- **Representacao:** lista de adjacencia. Para cada vertice `v`,
  `graph.adj[v]` guarda tuplas `(outro, peso, eh_trem)`. Tuplas
  evitam o custo de atributos de `Edge` no laco quente do Dijkstra.
- **Origem:** a capital `1`. Queremos as distancias minimas da capital
  para todas as cidades.

### Reducao do problema

Uma rota de trem `(s, y)` pode ser fechada se, e somente se, a
distancia minima da capital a `s` **continua a mesma** depois de
remove-la. Isso acontece em dois cenarios:

1. **Trem dominado:** existe outra rota de trem para a mesma cidade
   `s` com peso menor ou igual. Para cada cidade, no maximo uma rota
   de trem precisa ser mantida (a de menor peso). As demais sao
   sempre removiveis. Esse pre-processamento ja resolve parte da
   resposta em `O(k)`.
2. **Trem redundante:** depois da deduplicacao, a rota de trem
   restante para `s` so e necessaria se a distancia minima a `s`
   **nao puder** ser atingida usando apenas estradas (e demais
   trens, que vao para outras cidades). Para detectar isso, rodamos
   Dijkstra a partir da capital sobre o grafo completo e, em caso de
   empate, **preferimos terminar o caminho em uma estrada**.

## Algoritmo

### Dijkstra com desempate estrada > trem

A logica principal vive em [`src/dijkstra_sp.py`](src/dijkstra_sp.py).

- **Fila de prioridade:** `heapq` (heap binaria preguicosa). Entradas
  obsoletas sao descartadas pelo teste `if d > dist_to[u]: continue`.
- **Inicializacao:** `dist_to[u] = +inf` para todo `u`,
  `dist_to[source] = 0`. Empilha-se `(0, source)`.
- **Relaxamento de uma aresta `(u, v, peso, eh_trem)`:**
  - Se `dist_to[u] + peso < dist_to[v]`: atualizamos `dist_to[v]`,
    marcamos `used_train[v] = eh_trem` e empurramos `(novo, v)`.
  - Se `dist_to[u] + peso == dist_to[v]` e a aresta atual e estrada
    enquanto `used_train[v]` esta marcado como trem: mudamos
    `used_train[v]` para `False`. **Nao** empurramos de novo na fila,
    porque a distancia minima nao mudou - so o "rotulo" do tipo da
    melhor entrada.
- **Saida:** depois do laco principal, `used_train[s]` vale `True`
  se, e somente se, todo caminho minimo de `1` a `s` precisa terminar
  numa aresta de trem.

### Variacao de Dijkstra usada

E uma **variacao com desempate orientado por tipo de aresta** (em
ingles, costuma aparecer como *tie-breaking Dijkstra*). Para o
problema, o detalhe que muda em relacao ao Dijkstra padrao do
`algs4-py` e exatamente o tratamento da igualdade no relaxamento,
descrito acima. Isso evita ter que executar dois Dijkstras separados
ou rodar uma BFS adicional.

### Calculo da resposta

```text
trens_removidos_na_deduplicacao
    + (numero_de_cidades_com_trem - numero_de_cidades_que_ainda_precisam_de_trem)
```

ou seja, somamos as duplicatas descartadas com as cidades cuja
distancia minima ja era atingida por estradas (ou por trens a outras
cidades), tornando o trem ate ela desnecessario.

## Analise de complexidade

Seja:
- `V = n` (numero de vertices),
- `E = m + |trens deduplicados|`, com `m <= 3*10^5` e
  `|trens deduplicados| <= k <= 10^5`,
- `K = k` (rotas de trem na entrada original).

- **Tempo:**
  - Leitura e deduplicacao dos trens: `O(m + k)`.
  - Construcao do grafo: `O(m + |trens deduplicados|)`.
  - Dijkstra com `heapq`: `O((V + E) log V)`.
  - Contagem final: `O(|trens deduplicados|)`.
  - **Total:** `O((n + m + k) log n)`.
- **Memoria:** `O(n + m + k)` para a lista de adjacencia, os vetores
  `dist_to` e `used_train`, e a fila de prioridade.

Esses limites cabem confortavelmente no orcamento de 2 segundos /
256 MB do problema.

## Casos especiais tratados

- **Multiplas estradas paralelas entre as mesmas cidades:** o
  enunciado permite. Como adicionamos cada estrada como uma aresta
  separada, todas participam do relaxamento; o Dijkstra naturalmente
  pega a de menor peso.
- **Multiplos trens para a mesma cidade:** deduplicacao previa
  mantem apenas o trem de menor peso por cidade e ja contabiliza as
  duplicatas como removiveis.
- **Trem com peso > distancia minima por estradas:** a aresta de
  trem nem chega a relaxar `dist_to[s]`. `used_train[s]` permanece
  `False`, e o trem aparece como removivel.
- **Trem com peso == distancia minima por estradas:** o desempate no
  relaxamento coloca `used_train[s] = False`, marcando o trem como
  removivel (estradas alternativas garantem a mesma distancia).
- **Trem fornecendo o unico caminho minimo:** nenhuma estrada relaxa
  `s` com a mesma distancia, `used_train[s] = True`, e o trem nao
  pode ser fechado.
- **Pesos grandes (`<= 1e9`):** as distancias podem chegar a `~1e14`.
  Python lida com inteiros grandes nativamente; em Java seria `long`.

## Referencia `algs4-py`

O projeto segue a estrutura de:

- `algs4-py/algs4/edge.py` (classe `Edge` com `either()`/`other()`),
- `algs4-py/algs4/edge_weighted_graph.py` (lista de adjacencia),
- `algs4-py/algs4/dijkstra_sp.py` (classe `DijkstraSP` com
  inicializacao de `dist_to`, relaxamento e PQ).

As adaptacoes principais sao:

- `Edge` ganha o campo `kind` (`'road'` ou `'train'`);
- a lista de adjacencia armazena tuplas leves (mais rapido em Python
  com `n = 10^5`);
- a fila de prioridade e `heapq` em vez de `IndexMinPQ` (a
  `IndexMinPQ` da base tem operacoes `contains` / `del_min` em `O(n)`
  e nao escala para o tamanho da entrada deste problema);
- o relaxamento mantem `used_train[v]` e implementa o desempate
  estrada > trem explicitamente.

Nao foram usadas bibliotecas externas de grafos ou de caminho
minimo: somente estruturas nativas do Python (`list`, `dict`,
`heapq`).

## Evidencia de Accepted

A imagem do veredito **Accepted** na submissao do Codeforces esta
em [`evidencias/accepted.png`](evidencias/accepted.png).

Dados da submissao aceita:

- Submission ID: **376095016**
- Usuario: **frreneto**
- Problema: **449B - Jzzhu and Cities**
- Linguagem: **Python 3**
- Veredito: **Accepted**
- Tempo: **1625 ms**
- Memoria: **171300 KB**
- Data: **25/05/2026 21:47 UTC-3**
- Link: <https://codeforces.com/contest/449/submission/376095016>

## Apresentacao

Os slides em PDF estao em
[`apresentacao/apresentacao.pdf`](apresentacao/apresentacao.pdf).
