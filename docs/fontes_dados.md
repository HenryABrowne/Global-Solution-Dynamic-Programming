# Fontes de Dados

## Observação sobre os dados utilizados

Nesta versão do projeto, foram utilizados dados sintéticos controlados para simular os municípios, índices de risco, custos de atendimento, população e rotas ponderadas.

A escolha por dados sintéticos foi feita para garantir:

- reprodutibilidade dos experimentos;
- controle sobre o tamanho das instâncias;
- execução local sem dependência de APIs externas;
- possibilidade de testar Força Bruta em grafos pequenos;
- possibilidade de escalar o Dijkstra para instâncias maiores.

## Estrutura dos dados sintéticos

### Municípios

Cada município é representado por uma tupla:

```text
(id_municipio, nome, indice_risco, custo_atendimento, populacao)