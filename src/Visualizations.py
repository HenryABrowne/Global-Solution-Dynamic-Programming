from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx

try:
    from src.data_structures import BinarySearchTree, Grafo, Municipio, Node
except ImportError:
    from data_structures import BinarySearchTree, Grafo, Municipio, Node


def criar_pasta_saida(caminho: str) -> None:
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)


def salvar_figura(caminho: Optional[str]) -> None:
    if caminho:
        criar_pasta_saida(caminho)
        plt.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close()


def grafo_para_networkx(grafo: Grafo) -> nx.Graph:
    g = nx.Graph()

    for origem, vizinhos in grafo.items():
        g.add_node(origem)

        for destino, peso in vizinhos:
            g.add_edge(origem, destino, weight=peso)

    return g


def labels_municipios(
    nodes: List[int],
    municipios: Optional[Dict[int, Municipio]] = None
) -> Dict[int, str]:
    labels: Dict[int, str] = {}

    for node in nodes:
        if municipios and node in municipios:
            labels[node] = municipios[node][1]
        else:
            labels[node] = str(node)

    return labels


def plotar_grafo(
    grafo: Grafo,
    municipios: Optional[Dict[int, Municipio]] = None,
    caminho_destaque: Optional[List[int]] = None,
    titulo: str = "Grafo de municípios",
    caminho_saida: Optional[str] = None
) -> None:
    g = grafo_para_networkx(grafo)
    pos = nx.spring_layout(g, seed=42)
    labels = labels_municipios(list(g.nodes), municipios)

    arestas_destaque = set()

    if caminho_destaque:
        for i in range(len(caminho_destaque) - 1):
            u = caminho_destaque[i]
            v = caminho_destaque[i + 1]
            arestas_destaque.add(tuple(sorted((u, v))))

    cores_arestas = [
        "red" if tuple(sorted((u, v))) in arestas_destaque else "gray"
        for u, v in g.edges
    ]

    larguras = [
        3 if tuple(sorted((u, v))) in arestas_destaque else 1
        for u, v in g.edges
    ]

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(g, pos, node_size=650, node_color="#d9eaf7")
    nx.draw_networkx_edges(g, pos, edge_color=cores_arestas, width=larguras)
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=7)

    pesos = nx.get_edge_attributes(g, "weight")
    pesos_formatados = {aresta: round(valor, 2) for aresta, valor in pesos.items()}

    nx.draw_networkx_edge_labels(
        g,
        pos,
        edge_labels=pesos_formatados,
        font_size=6
    )

    plt.title(titulo)
    plt.axis("off")
    salvar_figura(caminho_saida)


def plotar_grafo_com_mst(
    grafo: Grafo,
    arestas_mst: List[Tuple[int, int, float]],
    municipios: Optional[Dict[int, Municipio]] = None,
    titulo: str = "Grafo de municípios com MST destacada",
    caminho_saida: Optional[str] = None
) -> None:
    g = grafo_para_networkx(grafo)
    pos = nx.spring_layout(g, seed=42)
    labels = labels_municipios(list(g.nodes), municipios)

    mst_set = {tuple(sorted((u, v))) for u, v, _ in arestas_mst}

    cores_arestas = [
        "red" if tuple(sorted((u, v))) in mst_set else "lightgray"
        for u, v in g.edges
    ]

    larguras = [
        3 if tuple(sorted((u, v))) in mst_set else 0.7
        for u, v in g.edges
    ]

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(g, pos, node_size=650, node_color="#d9eaf7")
    nx.draw_networkx_edges(g, pos, edge_color=cores_arestas, width=larguras)
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=7)

    pesos = nx.get_edge_attributes(g, "weight")
    pesos_mst = {
        aresta: round(valor, 2)
        for aresta, valor in pesos.items()
        if tuple(sorted(aresta)) in mst_set
    }

    nx.draw_networkx_edge_labels(
        g,
        pos,
        edge_labels=pesos_mst,
        font_size=6
    )

    plt.title(titulo)
    plt.axis("off")
    salvar_figura(caminho_saida)


def calcular_posicoes_bst(
    node: Optional[Node],
    x: float = 0.0,
    y: float = 0.0,
    dx: float = 1.0,
    posicoes: Optional[Dict[int, Tuple[float, float]]] = None,
    arestas: Optional[List[Tuple[int, int]]] = None
) -> tuple[Dict[int, Tuple[float, float]], List[Tuple[int, int]]]:
    if posicoes is None:
        posicoes = {}

    if arestas is None:
        arestas = []

    if node is None:
        return posicoes, arestas

    node_id = node.id_municipio
    posicoes[node_id] = (x, y)

    if node.left is not None:
        arestas.append((node_id, node.left.id_municipio))
        calcular_posicoes_bst(node.left, x - dx, y - 1, dx / 1.8, posicoes, arestas)

    if node.right is not None:
        arestas.append((node_id, node.right.id_municipio))
        calcular_posicoes_bst(node.right, x + dx, y - 1, dx / 1.8, posicoes, arestas)

    return posicoes, arestas


def coletar_labels_bst(
    node: Optional[Node],
    labels: Optional[Dict[int, str]] = None
) -> Dict[int, str]:
    if labels is None:
        labels = {}

    if node is None:
        return labels

    labels[node.id_municipio] = f"{node.nome}\nRisco: {node.indice_risco:.2f}"

    coletar_labels_bst(node.left, labels)
    coletar_labels_bst(node.right, labels)

    return labels


def plotar_bst(
    bst: BinarySearchTree,
    titulo: str = "BST por índice de risco",
    caminho_saida: Optional[str] = None
) -> None:
    if bst.root is None:
        plt.figure(figsize=(8, 4))
        plt.title(titulo)
        plt.text(0.5, 0.5, "Árvore vazia", ha="center", va="center")
        plt.axis("off")
        salvar_figura(caminho_saida)
        return

    g = nx.DiGraph()
    posicoes, arestas = calcular_posicoes_bst(bst.root, dx=4.0)
    labels = coletar_labels_bst(bst.root)

    for node_id in posicoes:
        g.add_node(node_id)

    for origem, destino in arestas:
        g.add_edge(origem, destino)

    plt.figure(figsize=(14, 8))
    nx.draw_networkx_nodes(g, posicoes, node_size=1800, node_color="#e8f5e9")
    nx.draw_networkx_edges(g, posicoes, arrows=False)
    nx.draw_networkx_labels(g, posicoes, labels=labels, font_size=8)

    plt.title(titulo)
    plt.axis("off")
    salvar_figura(caminho_saida)


def plotar_desempenho(
    resultados: List[Dict[str, Any]],
    titulo: str = "Tempo de execução x N",
    caminho_saida: Optional[str] = None
) -> None:
    algoritmos = sorted(set(item["algoritmo"] for item in resultados))

    plt.figure(figsize=(10, 6))

    for algoritmo in algoritmos:
        dados = [item for item in resultados if item["algoritmo"] == algoritmo]
        dados.sort(key=lambda item: item["n_vertices"])

        x = [item["n_vertices"] for item in dados]
        y = [item["tempo_ms"] for item in dados]

        plt.plot(x, y, marker="o", label=algoritmo)

    plt.title(titulo)
    plt.xlabel("Número de vértices")
    plt.ylabel("Tempo de execução (ms)")
    plt.legend()
    plt.grid(True)
    salvar_figura(caminho_saida)


def plotar_memoria(
    resultados: List[Dict[str, Any]],
    titulo: str = "Memória alocada x N",
    caminho_saida: Optional[str] = None
) -> None:
    algoritmos = sorted(set(item["algoritmo"] for item in resultados))

    plt.figure(figsize=(10, 6))

    for algoritmo in algoritmos:
        dados = [item for item in resultados if item["algoritmo"] == algoritmo]
        dados.sort(key=lambda item: item["n_vertices"])

        x = [item["n_vertices"] for item in dados]
        y = [item["memoria_mb"] for item in dados]

        plt.plot(x, y, marker="o", label=algoritmo)

    plt.title(titulo)
    plt.xlabel("Número de vértices")
    plt.ylabel("Memória alocada (MB)")
    plt.legend()
    plt.grid(True)
    salvar_figura(caminho_saida)


def calcular_gaps_por_n(resultados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    gaps: List[Dict[str, Any]] = []
    tamanhos = sorted(set(item["n_vertices"] for item in resultados))

    for n in tamanhos:
        dados_n = [item for item in resultados if item["n_vertices"] == n]

        fb = next(
            (
                item
                for item in dados_n
                if "força" in item["algoritmo"].lower()
                or "bruta" in item["algoritmo"].lower()
            ),
            None
        )

        guloso = next(
            (
                item
                for item in dados_n
                if "dijkstra" in item["algoritmo"].lower()
                or "guloso" in item["algoritmo"].lower()
            ),
            None
        )

        if fb is None or guloso is None:
            continue

        custo_otimo = float(fb["custo_solucao"])
        custo_guloso = float(guloso["custo_solucao"])

        if custo_otimo <= 0:
            gap = 0.0
        else:
            gap = ((custo_guloso - custo_otimo) / custo_otimo) * 100

        gaps.append(
            {
                "n_vertices": n,
                "gap_percentual": gap,
                "custo_otimo": custo_otimo,
                "custo_guloso": custo_guloso
            }
        )

    return gaps


def plotar_gap_otimalidade(
    resultados: List[Dict[str, Any]],
    titulo: str = "Gap de otimalidade x N",
    caminho_saida: Optional[str] = None
) -> None:
    gaps = calcular_gaps_por_n(resultados)

    x = [item["n_vertices"] for item in gaps]
    y = [item["gap_percentual"] for item in gaps]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker="o")
    plt.title(titulo)
    plt.xlabel("Número de vértices")
    plt.ylabel("Gap de otimalidade (%)")
    plt.grid(True)
    salvar_figura(caminho_saida)


def plotar_operacoes(
    resultados: List[Dict[str, Any]],
    titulo: str = "Operações elementares x N",
    caminho_saida: Optional[str] = None
) -> None:
    algoritmos = sorted(set(item["algoritmo"] for item in resultados))

    plt.figure(figsize=(10, 6))

    for algoritmo in algoritmos:
        dados = [item for item in resultados if item["algoritmo"] == algoritmo]
        dados.sort(key=lambda item: item["n_vertices"])

        x = [item["n_vertices"] for item in dados]
        y = [item["operacoes"] for item in dados]

        plt.plot(x, y, marker="o", label=algoritmo)

    plt.title(titulo)
    plt.xlabel("Número de vértices")
    plt.ylabel("Operações elementares")
    plt.legend()
    plt.grid(True)
    salvar_figura(caminho_saida)


def plotar_tabela_estruturas(caminho_saida: Optional[str] = None) -> None:
    dados = [
        ["list", "Adjacência, caminhos e resultados"],
        ["tuple", "Municípios e arestas"],
        ["dict", "Grafo, custos e predecessores"],
        ["set", "Visitados e controle de ciclos"],
        ["heapq", "Fila de prioridade do Dijkstra/Prim"],
        ["BST", "Consulta por intervalo de risco"],
        ["grafo", "Rede ponderada de municípios"]
    ]

    plt.figure(figsize=(12, 4))
    plt.axis("off")

    tabela = plt.table(
        cellText=dados,
        colLabels=["Estrutura", "Uso no sistema"],
        loc="center",
        cellLoc="left"
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1, 1.6)

    plt.title("Estruturas de dados utilizadas")
    salvar_figura(caminho_saida)


def gerar_figuras_obrigatorias(
    grafo: Grafo,
    bst: BinarySearchTree,
    resultados: List[Dict[str, Any]],
    municipios: Optional[Dict[int, Municipio]] = None,
    caminho_destaque: Optional[List[int]] = None,
    arestas_mst: Optional[List[Tuple[int, int, float]]] = None,
    pasta_saida: str = "report/figuras"
) -> None:
    Path(pasta_saida).mkdir(parents=True, exist_ok=True)

    if arestas_mst is not None:
        plotar_grafo_com_mst(
            grafo=grafo,
            arestas_mst=arestas_mst,
            municipios=municipios,
            caminho_saida=f"{pasta_saida}/grafo_mst.png"
        )

    plotar_grafo(
        grafo=grafo,
        municipios=municipios,
        caminho_destaque=caminho_destaque,
        caminho_saida=f"{pasta_saida}/grafo_rota_destacada.png"
    )

    plotar_bst(
        bst=bst,
        caminho_saida=f"{pasta_saida}/bst_riscos.png"
    )

    plotar_desempenho(
        resultados=resultados,
        caminho_saida=f"{pasta_saida}/desempenho_tempo_n.png"
    )

    plotar_gap_otimalidade(
        resultados=resultados,
        caminho_saida=f"{pasta_saida}/gap_otimalidade.png"
    )

    plotar_operacoes(
        resultados=resultados,
        caminho_saida=f"{pasta_saida}/operacoes_n.png"
    )

    plotar_tabela_estruturas(
        caminho_saida=f"{pasta_saida}/tabela_estruturas.png"
    )
