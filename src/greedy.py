from __future__ import annotations

import heapq
from dataclasses import dataclass
from math import inf
from typing import Dict, List, Optional, Set, Tuple

try:
    from src.data_structures import BinarySearchTree, Grafo, Municipio
except ImportError:
    from data_structures import BinarySearchTree, Grafo, Municipio


@dataclass
class ResultadoDijkstra:
    origem: int
    destino: int
    caminho: List[int]
    custo_total: float
    distancias: Dict[int, float]
    predecessores: Dict[int, Optional[int]]
    vertices_visitados: int
    arestas_relaxadas: int
    insercoes_heap: int


@dataclass
class ResultadoPrim:
    origem: int
    arestas_mst: List[Tuple[int, int, float]]
    custo_total: float
    vertices_visitados: int
    insercoes_heap: int
    arestas_avaliadas: int


def dijkstra(
    grafo: Grafo,
    origem: int,
    destino: Optional[int] = None
) -> ResultadoDijkstra:
    distancias: Dict[int, float] = {vertice: inf for vertice in grafo}
    predecessores: Dict[int, Optional[int]] = {vertice: None for vertice in grafo}
    visitados: Set[int] = set()

    distancias[origem] = 0.0
    heap: List[Tuple[float, int]] = [(0.0, origem)]

    arestas_relaxadas = 0
    insercoes_heap = 1

    while heap:
        distancia_atual, vertice_atual = heapq.heappop(heap)

        if vertice_atual in visitados:
            continue

        visitados.add(vertice_atual)

        if destino is not None and vertice_atual == destino:
            break

        for vizinho, peso in grafo.get(vertice_atual, []):
            if vizinho in visitados:
                continue

            arestas_relaxadas += 1
            nova_distancia = distancia_atual + peso

            if nova_distancia < distancias.get(vizinho, inf):
                distancias[vizinho] = nova_distancia
                predecessores[vizinho] = vertice_atual
                heapq.heappush(heap, (nova_distancia, vizinho))
                insercoes_heap += 1

    if destino is None:
        destino_resultado = origem
        caminho = []
        custo_total = 0.0
    else:
        destino_resultado = destino
        caminho = reconstruir_caminho(predecessores, origem, destino)
        custo_total = distancias.get(destino, inf)

    return ResultadoDijkstra(
        origem=origem,
        destino=destino_resultado,
        caminho=caminho,
        custo_total=custo_total,
        distancias=distancias,
        predecessores=predecessores,
        vertices_visitados=len(visitados),
        arestas_relaxadas=arestas_relaxadas,
        insercoes_heap=insercoes_heap
    )


def reconstruir_caminho(
    predecessores: Dict[int, Optional[int]],
    origem: int,
    destino: int
) -> List[int]:
    caminho: List[int] = []
    atual: Optional[int] = destino

    while atual is not None:
        caminho.append(atual)

        if atual == origem:
            break

        atual = predecessores.get(atual)

    caminho.reverse()

    if not caminho or caminho[0] != origem:
        return []

    return caminho


def prim_mst(
    grafo: Grafo,
    origem: Optional[int] = None
) -> ResultadoPrim:
    if not grafo:
        return ResultadoPrim(
            origem=-1,
            arestas_mst=[],
            custo_total=0.0,
            vertices_visitados=0,
            insercoes_heap=0,
            arestas_avaliadas=0
        )

    if origem is None:
        origem = next(iter(grafo))

    visitados: Set[int] = set()
    arestas_mst: List[Tuple[int, int, float]] = []
    heap: List[Tuple[float, int, int]] = []

    visitados.add(origem)

    insercoes_heap = 0
    arestas_avaliadas = 0

    for vizinho, peso in grafo.get(origem, []):
        heapq.heappush(heap, (peso, origem, vizinho))
        insercoes_heap += 1

    while heap and len(visitados) < len(grafo):
        peso, origem_aresta, destino_aresta = heapq.heappop(heap)
        arestas_avaliadas += 1

        if destino_aresta in visitados:
            continue

        visitados.add(destino_aresta)
        arestas_mst.append((origem_aresta, destino_aresta, peso))

        for proximo, peso_proximo in grafo.get(destino_aresta, []):
            if proximo not in visitados:
                heapq.heappush(
                    heap,
                    (peso_proximo, destino_aresta, proximo)
                )
                insercoes_heap += 1

    custo_total = sum(peso for _, _, peso in arestas_mst)

    return ResultadoPrim(
        origem=origem,
        arestas_mst=arestas_mst,
        custo_total=custo_total,
        vertices_visitados=len(visitados),
        insercoes_heap=insercoes_heap,
        arestas_avaliadas=arestas_avaliadas
    )


def selecionar_municipios_alto_risco(
    bst: BinarySearchTree,
    risco_minimo: float = 0.7,
    risco_maximo: float = 1.0
) -> List[Municipio]:
    return bst.buscar_intervalo(risco_minimo, risco_maximo)


def ordenar_municipios_por_prioridade(
    municipios: List[Municipio]
) -> List[Municipio]:
    return sorted(
        municipios,
        key=lambda municipio: (
            municipio[2],
            municipio[4],
            -municipio[3]
        ),
        reverse=True
    )


def rotas_para_municipios_prioritarios(
    grafo: Grafo,
    origem: int,
    municipios_prioritarios: List[Municipio]
) -> List[ResultadoDijkstra]:
    resultados: List[ResultadoDijkstra] = []

    for municipio in municipios_prioritarios:
        destino = municipio[0]
        resultado = dijkstra(grafo, origem, destino)
        resultados.append(resultado)

    resultados.sort(key=lambda item: item.custo_total)

    return resultados


def melhor_rota_prioritaria(
    grafo: Grafo,
    origem: int,
    bst: BinarySearchTree,
    risco_minimo: float = 0.7,
    risco_maximo: float = 1.0
) -> Optional[ResultadoDijkstra]:
    municipios_alto_risco = selecionar_municipios_alto_risco(
        bst,
        risco_minimo,
        risco_maximo
    )

    municipios_ordenados = ordenar_municipios_por_prioridade(municipios_alto_risco)

    if not municipios_ordenados:
        return None

    resultados = rotas_para_municipios_prioritarios(
        grafo,
        origem,
        municipios_ordenados
    )

    resultados_validos = [
        resultado
        for resultado in resultados
        if resultado.caminho and resultado.custo_total < inf
    ]

    if not resultados_validos:
        return None

    return min(resultados_validos, key=lambda item: item.custo_total)


def calcular_custo_caminho_guloso(
    grafo: Grafo,
    caminho: List[int]
) -> float:
    if len(caminho) <= 1:
        return 0.0

    custo_total = 0.0

    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]

        encontrou = False

        for vizinho, peso in grafo.get(origem, []):
            if vizinho == destino:
                custo_total += peso
                encontrou = True
                break

        if not encontrou:
            return inf

    return custo_total