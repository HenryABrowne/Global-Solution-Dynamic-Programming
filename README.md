# Global Solution 2026 — Dynamic Programming

## Monitoramento de Riscos Ambientais com Árvores, Grafos e Algoritmos

Projeto desenvolvido para a disciplina **Dynamic Programming / Estruturas de Dados e Algoritmos**, da FIAP, no contexto da **Global Solution 2026 — Economia Espacial**.

## Integrantes

| Eduardo Santiago Bassan | RM561474 |
| Henry Andrade Browne | RM562622 |
| João Victor Abe | RM561446 |

## Tema

O projeto simula um sistema de monitoramento e triagem de riscos ambientais em municípios brasileiros, utilizando estruturas de dados e algoritmos para analisar rotas, risco municipal e desempenho computacional.

## Cenários brasileiros escolhidos

### Cenário 1 — Enchentes no Rio Grande do Sul

Rede de municípios afetados por enchentes, representada por um grafo ponderado. Os vértices representam municípios e as arestas representam rotas de deslocamento entre eles.

### Cenário 2 — Seca no MATOPIBA

Rede de municípios da região MATOPIBA, com índice de risco associado à criticidade ambiental. A BST organiza os municípios por grau de risco.

## Estruturas de dados utilizadas

| Estrutura | Uso no projeto |
|---|---|
| `list` | Lista de adjacência, caminhos e resultados |
| `tuple` | Representação de municípios e arestas |
| `dict` | Grafo, distâncias, predecessores e metadados |
| `set` | Controle de visitados e prevenção de ciclos |
| `heapq` | Fila de prioridade do algoritmo de Dijkstra |
| BST | Organização dos municípios por índice de risco |
| Grafo | Modelagem da rede ponderada de municípios |

## Algoritmos implementados

### Força Bruta

O algoritmo de força bruta enumera todos os caminhos possíveis entre origem e destino em instâncias pequenas, usando recursão com backtracking.

Ele registra:

- melhor caminho encontrado;
- melhor custo;
- número de caminhos avaliados;
- número de chamadas recursivas;
- custos encontrados.

### Guloso — Dijkstra

O algoritmo guloso escolhido foi o **Dijkstra**, utilizado para encontrar o caminho mínimo entre um município de origem e um município de destino.

Ele registra:

- caminho mínimo;
- custo total;
- distâncias acumuladas;
- predecessores;
- vértices visitados;
- arestas relaxadas;
- inserções no heap.

## Arquitetura do projeto

```text
global-solution-2026-fund/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── municipios_rs.csv
│   │   ├── municipios_matopiba.csv
│   │   ├── rotas_rs.csv
│   │   └── rotas_matopiba.csv
│   │
│   └── processed/
│       ├── municipios_rs.json
│       ├── municipios_matopiba.json
│       ├── grafo_rs.json
│       ├── grafo_matopiba.json
│       ├── bst_rs.json
│       ├── bst_matopiba.json
│       ├── resultados_rs.csv
│       └── resultados_matopiba.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_structures.py
│   ├── brute_force.py
│   ├── greedy.py
│   ├── performance_monitor.py
│   ├── visualizations.py
│   └── main.py
│
├── notebooks/
│   └── analise_resultados.ipynb
│
├── tests/
│   └── test_algorithms.py
│
├── report/
│   ├── relatorio_final.pdf
│   └── figuras/
│
└── docs/
    ├── planejamento.md
    ├── fontes_dados.md
    └── escala_decisao.md