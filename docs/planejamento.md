# Planejamento do Projeto

## Objetivo

Desenvolver um sistema de monitoramento de riscos ambientais em municípios brasileiros utilizando estruturas de dados e algoritmos de busca.

O projeto modela municípios como vértices de um grafo ponderado, rotas como arestas com custo de deslocamento e índices de risco em uma árvore binária de busca.

## Cenários escolhidos

### Cenário A — Enchentes no Rio Grande do Sul

O primeiro cenário representa uma rede de municípios afetados por enchentes. O grafo simula rotas de deslocamento entre municípios, permitindo avaliar caminhos de menor custo para atendimento emergencial.

### Cenário B — Seca no MATOPIBA

O segundo cenário representa municípios da região MATOPIBA, com índices de risco associados à seca. A BST é usada para priorizar municípios com maior criticidade ambiental.

## Estruturas de dados

| Estrutura | Uso |
|---|---|
| Lista | Lista de adjacência, caminhos e resultados |
| Tupla | Representação de municípios e arestas |
| Dicionário | Grafo, distâncias, predecessores e dados dos municípios |
| Conjunto | Controle de visitados e prevenção de ciclos |
| Heap | Fila de prioridade no Dijkstra e no Prim |
| BST | Organização dos municípios por índice de risco |
| Grafo | Modelagem da rede ponderada de municípios |

## Algoritmos

### Força Bruta

A Força Bruta é usada como baseline para grafos pequenos. Ela enumera todos os caminhos simples entre uma origem e um destino usando recursão com backtracking.

A função registra:

- melhor caminho;
- melhor custo;
- número de caminhos avaliados;
- número de chamadas recursivas.

### Dijkstra

O Dijkstra foi escolhido como algoritmo guloso principal para encontrar caminhos mínimos entre municípios.

Ele usa:

- `heapq` como fila de prioridade;
- dicionário de distâncias;
- dicionário de predecessores;
- conjunto de visitados.

### Prim

O Prim foi adicionado para gerar a Árvore Geradora Mínima e atender à figura obrigatória do grafo com MST destacada.

Ele usa:

- `heapq` para selecionar a menor aresta disponível;
- conjunto de visitados;
- lista de arestas da MST.

## Fluxo de execução

1. Carregar ou gerar dados sintéticos.
2. Criar o grafo ponderado.
3. Construir a BST com os municípios ordenados por risco.
4. Consultar municípios de alto risco na BST.
5. Priorizar os municípios por risco, população e custo.
6. Executar Dijkstra para rotas de menor custo.
7. Executar Prim para obter a MST.
8. Executar Força Bruta em instâncias pequenas.
9. Comparar desempenho entre Força Bruta e Dijkstra.
10. Gerar gráficos e arquivos processados.

## Justificativa dos dados sintéticos

Os dados sintéticos foram usados para garantir reprodutibilidade, controle do tamanho das instâncias e execução local sem dependência de bases externas.

Eles simulam:

- identificadores municipais;
- nomes de municípios;
- índice de risco ambiental;
- custo de atendimento;
- população;
- rotas ponderadas por custo de deslocamento.

## Decisões principais

| Decisão | Justificativa |
|---|---|
| Usar lista de adjacência | Menor uso de memória em grafos esparsos |
| Usar Dijkstra | Adequado para caminho mínimo com pesos positivos |
| Usar Prim | Permite gerar MST para análise de cobertura |
| Usar BST | Permite consultar municípios por faixa de risco |
| Limitar Força Bruta até N = 12 | Evita explosão combinatória em instâncias grandes |

## Saídas esperadas

O sistema gera:

- dados processados em JSON;
- resultados de benchmark em CSV;
- priorização por BST;
- rota prioritária;
- MST;
- gráficos obrigatórios;
- notebook de análise;
- relatório técnico.