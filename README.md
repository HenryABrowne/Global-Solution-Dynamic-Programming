# Global Solution 2026 — Dynamic Programming

## Monitoramento de Riscos Ambientais com Árvores, Grafos e Algoritmos

Projeto desenvolvido para a disciplina **Dynamic Programming / Estruturas de Dados e Algoritmos**, da FIAP, no contexto da **Global Solution 2026 — Economia Espacial**.

O objetivo do projeto é simular um sistema de monitoramento e triagem de riscos ambientais em municípios brasileiros, utilizando **grafos ponderados**, **árvore binária de busca (BST)**, **Força Bruta**, **algoritmos gulosos** e análise de desempenho computacional.

## Integrantes

| Nome                    | RM       |
| ----------------------- | -------- |
| Eduardo Santiago Bassan | RM561474 |
| Henry Andrade Browne    | RM562622 |
| João Victor Abe         | RM561446 |

## Tema

O projeto simula um sistema de apoio à tomada de decisão para monitoramento ambiental. Municípios são representados como vértices de um grafo ponderado, enquanto as rotas entre eles são representadas por arestas com peso associado ao custo ou tempo de deslocamento.

Além disso, os municípios possuem um índice de risco ambiental, organizado em uma **Binary Search Tree (BST)**, permitindo consultas por faixa de risco e priorização de atendimento.

## Cenários brasileiros escolhidos

### Cenário 1 — Enchentes no Rio Grande do Sul

Rede de municípios afetados por enchentes, representada por um grafo ponderado. Os vértices representam municípios e as arestas representam rotas de deslocamento entre eles.

O objetivo é simular rotas de atendimento emergencial, priorizando municípios de maior risco e avaliando caminhos de menor custo.

### Cenário 2 — Seca no MATOPIBA

Rede de municípios da região MATOPIBA, com índice de risco associado à criticidade ambiental. A BST organiza os municípios por grau de risco, permitindo identificar os pontos mais críticos para atendimento.

O objetivo é simular uma triagem de risco de seca e avaliar a eficiência computacional das estruturas e algoritmos utilizados.

## Observação sobre os dados

Nesta versão, foram utilizados **dados sintéticos controlados** para simular municípios, índices de risco, custos de atendimento, população e rotas ponderadas.

A escolha por dados sintéticos foi feita para garantir:

* reprodutibilidade dos experimentos;
* controle do tamanho das instâncias;
* execução local sem dependência de APIs externas;
* comparação entre Força Bruta e algoritmo guloso;
* geração de gráficos e testes automatizados.

## Estruturas de dados utilizadas

| Estrutura | Uso no projeto                                             |
| --------- | ---------------------------------------------------------- |
| `list`    | Lista de adjacência, caminhos, resultados e arestas da MST |
| `tuple`   | Representação de municípios e arestas                      |
| `dict`    | Grafo, distâncias, predecessores e metadados               |
| `set`     | Controle de visitados e prevenção de ciclos                |
| `heapq`   | Fila de prioridade no Dijkstra e no Prim                   |
| BST       | Organização dos municípios por índice de risco             |
| Grafo     | Modelagem da rede ponderada de municípios                  |

## Algoritmos implementados

### Força Bruta

O algoritmo de Força Bruta enumera todos os caminhos possíveis entre origem e destino em instâncias pequenas, usando recursão com backtracking.

Ele registra:

* melhor caminho encontrado;
* melhor custo;
* número de caminhos avaliados;
* número de chamadas recursivas;
* custos encontrados.

A Força Bruta é usada como baseline para validar a solução ótima em grafos pequenos.

### Guloso — Dijkstra

O algoritmo guloso escolhido para o problema de caminho mínimo foi o **Dijkstra**, utilizado para encontrar a rota de menor custo entre um município de origem e um município de destino.

Ele registra:

* caminho mínimo;
* custo total;
* distâncias acumuladas;
* predecessores;
* vértices visitados;
* arestas relaxadas;
* inserções no heap.

### Prim — Árvore Geradora Mínima

Além do Dijkstra, o projeto também implementa o **algoritmo de Prim** para gerar a **Árvore Geradora Mínima (MST)**.

Essa implementação foi adicionada para visualizar a rede de cobertura mínima entre os municípios e gerar a figura obrigatória com a MST destacada.

## Arquitetura do projeto

O projeto está organizado para que o código-fonte, os dados, os testes, o notebook de análise, a documentação auxiliar, as figuras e o relatório final estejam no mesmo repositório.

O arquivo **`report/relatorio_final.pdf`** faz parte da entrega oficial e está incluído junto às pastas com os arquivos de código. Dessa forma, a entrega não depende de um documento externo separado: o relatório final está versionado e organizado dentro da própria estrutura do projeto.

```text
DynamicProgramming/
│
├── README.md
├── requirements.txt
├── .gitignore
├── conftest.py
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
│       ├── resultados_matopiba.csv
│       ├── priorizacao_bst_rs.json
│       ├── priorizacao_bst_matopiba.json
│       ├── rota_prioritaria_rs.json
│       ├── rota_prioritaria_matopiba.json
│       ├── mst_rs.json
│       └── mst_matopiba.json
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
├── docs/
│   ├── planejamento.md
│   ├── fontes_dados.md
│   └── escala_decisao.md
│
└── report/
    ├── gerar_relatorio_pdf.py
    ├── relatorio_final.pdf
    └── figuras/
        ├── rs/
        │   ├── grafo_mst.png
        │   ├── grafo_rota_destacada.png
        │   ├── bst_riscos.png
        │   ├── desempenho_tempo_n.png
        │   ├── gap_otimalidade.png
        │   ├── operacoes_n.png
        │   └── tabela_estruturas.png
        │
        └── matopiba/
            ├── grafo_mst.png
            ├── grafo_rota_destacada.png
            ├── bst_riscos.png
            ├── desempenho_tempo_n.png
            ├── gap_otimalidade.png
            ├── operacoes_n.png
            └── tabela_estruturas.png
```

## Relatório final

O relatório técnico final está incluído no próprio repositório, no caminho:

```text
report/relatorio_final.pdf
```

Esse PDF consolida:

* identificação dos integrantes;
* contextualização dos cenários brasileiros;
* modelagem do grafo e da BST;
* justificativa das estruturas de dados;
* análise de complexidade;
* resultados e figuras obrigatórias;
* gráfico de desempenho;
* gap de otimalidade;
* escala de decisão;
* conclusão;
* referências.

O PDF deve ser entregue junto com o código-fonte, os dados, os testes e o notebook, pois representa a documentação técnica final do projeto.

## Instalação

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/Mac:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar o projeto

Na raiz do projeto, execute:

```bash
python -m src.main
```

O sistema irá:

1. Gerar dados sintéticos caso os arquivos CSV ainda não existam;
2. Carregar os dados dos dois cenários;
3. Construir os grafos ponderados;
4. Construir as BSTs;
5. Consultar municípios de alto risco;
6. Executar Força Bruta em instâncias pequenas;
7. Executar Dijkstra para caminhos mínimos;
8. Executar Prim para gerar a MST;
9. Medir tempo, memória e operações;
10. Salvar os resultados em CSV e JSON;
11. Gerar as figuras obrigatórias.

## Como gerar o relatório PDF

Antes de gerar o PDF, execute o projeto principal para garantir que as figuras e resultados estejam atualizados:

```bash
python -m src.main
```

Depois, execute:

```bash
python report/gerar_relatorio_pdf.py
```

O relatório será gerado em:

```text
report/relatorio_final.pdf
```

## Como rodar os testes

Execute:

```bash
python -m pytest -q
```

Os testes verificam:

* construção do grafo;
* inserção de arestas;
* contagem de vértices e arestas;
* validação do grafo;
* funcionamento da BST;
* busca por intervalo de risco;
* remoção de nós;
* Força Bruta;
* Dijkstra;
* Prim/MST;
* priorização de municípios de alto risco.

## Saídas geradas

### Dados processados

```text
data/processed/municipios_rs.json
data/processed/municipios_matopiba.json
data/processed/grafo_rs.json
data/processed/grafo_matopiba.json
data/processed/bst_rs.json
data/processed/bst_matopiba.json
data/processed/resultados_rs.csv
data/processed/resultados_matopiba.csv
data/processed/priorizacao_bst_rs.json
data/processed/priorizacao_bst_matopiba.json
data/processed/rota_prioritaria_rs.json
data/processed/rota_prioritaria_matopiba.json
data/processed/mst_rs.json
data/processed/mst_matopiba.json
```

### Figuras

```text
report/figuras/rs/grafo_mst.png
report/figuras/rs/grafo_rota_destacada.png
report/figuras/rs/bst_riscos.png
report/figuras/rs/desempenho_tempo_n.png
report/figuras/rs/gap_otimalidade.png
report/figuras/rs/operacoes_n.png
report/figuras/rs/tabela_estruturas.png

report/figuras/matopiba/grafo_mst.png
report/figuras/matopiba/grafo_rota_destacada.png
report/figuras/matopiba/bst_riscos.png
report/figuras/matopiba/desempenho_tempo_n.png
report/figuras/matopiba/gap_otimalidade.png
report/figuras/matopiba/operacoes_n.png
report/figuras/matopiba/tabela_estruturas.png
```

### Relatório

```text
report/relatorio_final.pdf
```

## Análise de complexidade

### Força Bruta

A Força Bruta enumera todos os caminhos simples possíveis entre origem e destino. No pior caso, o número de possibilidades cresce de forma combinatória, tornando o algoritmo inviável para instâncias maiores.

### Dijkstra

Com lista de adjacência e heap, o Dijkstra possui complexidade aproximada:

```text
O((V + E) log V)
```

Onde:

* `V` é o número de vértices;
* `E` é o número de arestas.

### Prim

Com heap e lista de adjacência, o Prim possui complexidade aproximada:

```text
O(E log V)
```

Ele é utilizado para gerar a Árvore Geradora Mínima e visualizar uma rede de cobertura mínima.

### BST

As operações da BST dependem da altura `h` da árvore:

```text
Inserção: O(h)
Busca por intervalo: O(h + k)
Percurso in-order: O(n)
Remoção: O(h)
```

Onde:

* `h` é a altura da árvore;
* `k` é a quantidade de elementos retornados;
* `n` é o número de municípios armazenados.

## Escala de decisão

| Nível     | Interpretação                                                       |
| --------- | ------------------------------------------------------------------- |
| Excelente | Baixo custo computacional e solução igual ou muito próxima da ótima |
| Bom       | Tempo aceitável e pequeno gap de otimalidade                        |
| Regular   | Solução utilizável, mas com custo ou gap perceptível                |
| Inviável  | Alto custo computacional ou tempo impraticável                      |

## Conclusão

O projeto demonstra como estruturas de dados e algoritmos podem apoiar decisões em cenários ambientais. A BST permite organizar municípios por índice de risco, o grafo modela a rede de deslocamento, a Força Bruta valida instâncias pequenas, o Dijkstra encontra rotas de menor custo e o Prim gera a cobertura mínima da rede.

A solução equilibra qualidade da resposta, custo computacional e aplicabilidade prática aos cenários brasileiros escolhidos.

## Conexão com ODS

O projeto se conecta aos seguintes Objetivos de Desenvolvimento Sustentável:

* ODS 2 — Fome Zero e Agricultura Sustentável;
* ODS 9 — Indústria, Inovação e Infraestrutura;
* ODS 11 — Cidades e Comunidades Sustentáveis;
* ODS 13 — Ação Contra a Mudança Global do Clima.

## Referências

* NASA Earthdata — MODIS NDVI e SRTM;
* INPE PRODES/DETER;
* ANA HidroWeb;
* INMET;
* IBGE;
* ANATEL;
* DNIT;
* Cormen, T. et al. Introduction to Algorithms;
* Sedgewick, R. & Wayne, K. Algorithms;
* Skiena, S. The Algorithm Design Manual.
