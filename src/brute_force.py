from _future_ import annotations

from dataclasses import dataclass
from math import inf
from typing import List, Set

try:
    from src.data_structures import Grafo
except ImportError:
    from data_structures import Grafo


@dataclass
class ResultadoForcaBruta:
    melhor_caminho: List[int]
    melhor_custo: float
    caminhos_avaliados: int
    chamadas_recursivas: int
    custos_encontrados: List[float]


def calcular_custo_caminho(grafo: Grafo, caminho: List[int]) -> float:
    if len(caminho) <= 1:
        return 0.0

    custo_total = 0.0

    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]
        encontrou_aresta = False

        for vizinho, peso in grafo.get(origem, []):
            if vizinho == destino:
                custo_total += peso
                encontrou_aresta = True
                break

        if not encontrou_aresta:
            return inf

    return custo_total


def forca_bruta_caminhos(
    grafo: Grafo,
    origem: int,
    destino: int
) -> ResultadoForcaBruta:
    melhor_caminho: List[int] = []
    melhor_custo = inf
    caminhos_avaliados = 0
    chamadas_recursivas = 0
    custos_encontrados: List[float] = []

    def backtracking(
        atual: int,
        caminho: List[int],
        visitados: Set[int],
        custo_atual: float
    ) -> None:
        nonlocal melhor_caminho
        nonlocal melhor_custo
        nonlocal caminhos_avaliados
        nonlocal chamadas_recursivas

        chamadas_recursivas += 1

        if atual == destino:
            caminhos_avaliados += 1
            custos_encontrados.append(custo_atual)

            if custo_atual < melhor_custo:
                melhor_custo = custo_atual
                melhor_caminho = caminho.copy()

            return

        for vizinho, peso in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                caminho.append(vizinho)

                backtracking(
                    vizinho,
                    caminho,
                    visitados,
                    custo_atual + peso
                )

                caminho.pop()
                visitados.remove(vizinho)

    if origem not in grafo or destino not in grafo:
        return ResultadoForcaBruta(
            melhor_caminho=[],
            melhor_custo=inf,
            caminhos_avaliados=0,
            chamadas_recursivas=0,
            custos_encontrados=[]
        )

    backtracking(
        atual=origem,
        caminho=[origem],
        visitados={origem},
        custo_atual=0.0
    )

    return ResultadoForcaBruta(
        melhor_caminho=melhor_caminho,
        melhor_custo=melhor_custo,
        caminhos_avaliados=caminhos_avaliados,
        chamadas_recursivas=chamadas_recursivas,
        custos_encontrados=custos_encontrados
    )


def listar_todos_caminhos(
    grafo: Grafo,
    origem: int,
    destino: int
) -> List[List[int]]:
    caminhos: List[List[int]] = []

    def backtracking(
        atual: int,
        caminho: List[int],
        visitados: Set[int]
    ) -> None:
        if atual == destino:
            caminhos.append(caminho.copy())
            return

        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                caminho.append(vizinho)

                backtracking(vizinho, caminho, visitados)

                caminho.pop()
                visitados.remove(vizinho)

    if origem not in grafo or destino not in grafo:
        return caminhos

    backtracking(origem, [origem], {origem})

    return caminhos


def comparar_todos_caminhos(
    grafo: Grafo,
    origem: int,
    destino: int
) -> List[dict]:
    caminhos = listar_todos_caminhos(grafo, origem, destino)
    resultados = []

    for caminho in caminhos:
        resultados.append(
            {
                "caminho": caminho,
                "custo": calcular_custo_caminho(grafo, caminho)
            }
        )

    resultados.sort(key=lambda item: item["custo"])

    return resultados


def calcular_gap_otimalidade(
    custo_otimo: float,
    custo_guloso: float
) -> float:
    if custo_otimo == inf or custo_otimo == 0:
        return 0.0

    return ((custo_guloso - custo_otimo) / custo_otimo) * 100
