# Escala de Decisão

## Objetivo

A escala de decisão classifica as alternativas de solução considerando simultaneamente:

- qualidade da solução;
- custo computacional;
- uso adequado das estruturas de dados;
- aplicabilidade prática nos cenários brasileiros escolhidos.

## Critérios utilizados

| Critério | Descrição |
|---|---|
| Qualidade da solução | Proximidade da solução gulosa em relação ao ótimo obtido por Força Bruta |
| Custo computacional | Tempo de execução, memória e número de operações |
| Estruturas de dados | Adequação do uso de grafo, BST, heap, dicionários, listas e conjuntos |
| Aplicabilidade prática | Viabilidade de uso em cenários ambientais reais |

## Níveis da escala

| Nível | Classificação | Interpretação |
|---|---|---|
| 1 | Excelente | Baixo tempo de execução, baixo uso de memória e gap próximo de 0% |
| 2 | Bom | Solução eficiente, com pequeno aumento de custo computacional |
| 3 | Regular | Solução utilizável, mas com custo computacional ou gap perceptível |
| 4 | Inviável | Tempo, memória ou número de operações tornam o uso impraticável |

## Aplicação à Força Bruta

A Força Bruta tem papel importante como baseline, pois encontra a solução ótima para instâncias pequenas. Porém, seu custo cresce rapidamente conforme o número de vértices aumenta.

### Classificação

| Tamanho da instância | Classificação | Justificativa |
|---|---|---|
| N até 5 | Excelente | Executa rapidamente e permite validar o ótimo global |
| N até 8 | Bom | Ainda viável, mas já apresenta crescimento no número de chamadas |
| N até 12 | Regular | Útil para comparação, mas começa a se aproximar do limite prático |
| N acima de 12 | Inviável | A enumeração de caminhos se torna combinatória |

## Aplicação ao Dijkstra

O Dijkstra foi escolhido como algoritmo guloso principal por resolver o problema de caminho mínimo com pesos positivos.

### Classificação

| Tamanho da instância | Classificação | Justificativa |
|---|---|---|
| N até 12 | Excelente | Produz o mesmo resultado da Força Bruta nos testes pequenos |
| N até 20 | Excelente | Mantém tempo e memória baixos |
| N até 50 | Bom | Continua eficiente para grafos médios |
| N até 100 | Bom | Escala melhor que a Força Bruta e permanece aplicável |

## Aplicação ao Prim

O Prim foi usado para gerar a Árvore Geradora Mínima, permitindo avaliar uma rede de cobertura de menor custo.

### Classificação

| Aspecto | Classificação | Justificativa |
|---|---|---|
| Cobertura de municípios | Excelente | Conecta os vértices com custo total mínimo |
| Visualização da rede | Excelente | Permite destacar as arestas da MST |
| Aplicação prática | Bom | Útil para planejamento de infraestrutura e cobertura de atendimento |
| Comparação direta com Força Bruta | Regular | O foco do benchmark principal continua sendo caminho mínimo |

## Gap de otimalidade

O gap de otimalidade é calculado por:

```text
gap = ((custo_guloso - custo_otimo) / custo_otimo) * 100