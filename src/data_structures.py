from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


Municipio = Tuple[int, str, float, float, int]
Aresta = Tuple[int, int, float]
Grafo = Dict[int, List[Tuple[int, float]]]


@dataclass
class Node:
    municipio: Municipio
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    @property
    def id_municipio(self) -> int:
        return self.municipio[0]

    @property
    def nome(self) -> str:
        return self.municipio[1]

    @property
    def indice_risco(self) -> float:
        return self.municipio[2]

    @property
    def custo_atendimento(self) -> float:
        return self.municipio[3]

    @property
    def populacao(self) -> int:
        return self.municipio[4]


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.root is None

    @staticmethod
    def _key(municipio: Municipio) -> Tuple[float, int]:
        return municipio[2], municipio[0]

    @staticmethod
    def _node_key(node: Node) -> Tuple[float, int]:
        return node.indice_risco, node.id_municipio

    def inserir(self, municipio: Municipio) -> None:
        if self.root is None:
            self.root = Node(municipio)
            self._size += 1
            return

        if self._inserir_recursivo(self.root, municipio):
            self._size += 1

    def _inserir_recursivo(self, atual: Node, municipio: Municipio) -> bool:
        chave_nova = self._key(municipio)
        chave_atual = self._node_key(atual)

        if chave_nova < chave_atual:
            if atual.left is None:
                atual.left = Node(municipio)
                return True
            return self._inserir_recursivo(atual.left, municipio)

        if chave_nova > chave_atual:
            if atual.right is None:
                atual.right = Node(municipio)
                return True
            return self._inserir_recursivo(atual.right, municipio)

        return False

    def buscar_intervalo(self, r_min: float, r_max: float) -> List[Municipio]:
        resultado: List[Municipio] = []
        self._buscar_intervalo_recursivo(self.root, r_min, r_max, resultado)
        return resultado

    def _buscar_intervalo_recursivo(
        self,
        atual: Optional[Node],
        r_min: float,
        r_max: float,
        resultado: List[Municipio]
    ) -> None:
        if atual is None:
            return

        if atual.indice_risco >= r_min:
            self._buscar_intervalo_recursivo(atual.left, r_min, r_max, resultado)

        if r_min <= atual.indice_risco <= r_max:
            resultado.append(atual.municipio)

        if atual.indice_risco <= r_max:
            self._buscar_intervalo_recursivo(atual.right, r_min, r_max, resultado)

    def percurso_in_order(self) -> List[Municipio]:
        resultado: List[Municipio] = []
        self._in_order_recursivo(self.root, resultado)
        return resultado

    def _in_order_recursivo(
        self,
        atual: Optional[Node],
        resultado: List[Municipio]
    ) -> None:
        if atual is None:
            return

        self._in_order_recursivo(atual.left, resultado)
        resultado.append(atual.municipio)
        self._in_order_recursivo(atual.right, resultado)

    def altura(self) -> int:
        return self._altura_recursiva(self.root)

    def _altura_recursiva(self, atual: Optional[Node]) -> int:
        if atual is None:
            return 0

        return 1 + max(
            self._altura_recursiva(atual.left),
            self._altura_recursiva(atual.right)
        )

    def buscar_por_id(self, id_municipio: int) -> Optional[Municipio]:
        return self._buscar_por_id_recursivo(self.root, id_municipio)

    def _buscar_por_id_recursivo(
        self,
        atual: Optional[Node],
        id_municipio: int
    ) -> Optional[Municipio]:
        if atual is None:
            return None

        if atual.id_municipio == id_municipio:
            return atual.municipio

        encontrado = self._buscar_por_id_recursivo(atual.left, id_municipio)

        if encontrado is not None:
            return encontrado

        return self._buscar_por_id_recursivo(atual.right, id_municipio)

    def remover(self, id_municipio: int) -> bool:
        municipio = self.buscar_por_id(id_municipio)

        if municipio is None:
            return False

        self.root = self._remover_recursivo(self.root, self._key(municipio))
        self._size -= 1
        return True

    def _remover_recursivo(
        self,
        atual: Optional[Node],
        chave: Tuple[float, int]
    ) -> Optional[Node]:
        if atual is None:
            return None

        chave_atual = self._node_key(atual)

        if chave < chave_atual:
            atual.left = self._remover_recursivo(atual.left, chave)
            return atual

        if chave > chave_atual:
            atual.right = self._remover_recursivo(atual.right, chave)
            return atual

        if atual.left is None:
            return atual.right

        if atual.right is None:
            return atual.left

        sucessor = self._menor_no(atual.right)
        atual.municipio = sucessor.municipio
        atual.right = self._remover_recursivo(
            atual.right,
            self._node_key(sucessor)
        )

        return atual

    def _menor_no(self, atual: Node) -> Node:
        while atual.left is not None:
            atual = atual.left

        return atual

    def to_list(self) -> List[Dict[str, Any]]:
        return [
            {
                "id_municipio": municipio[0],
                "nome": municipio[1],
                "indice_risco": municipio[2],
                "custo_atendimento": municipio[3],
                "populacao": municipio[4],
            }
            for municipio in self.percurso_in_order()
        ]


def criar_grafo_vazio() -> Grafo:
    return {}


def adicionar_vertice(grafo: Grafo, id_municipio: int) -> None:
    if id_municipio not in grafo:
        grafo[id_municipio] = []


def adicionar_aresta(
    grafo: Grafo,
    origem: int,
    destino: int,
    peso: float,
    direcionado: bool = False
) -> None:
    adicionar_vertice(grafo, origem)
    adicionar_vertice(grafo, destino)

    grafo[origem].append((destino, peso))

    if not direcionado:
        grafo[destino].append((origem, peso))


def construir_grafo(
    municipios: List[Municipio],
    arestas: List[Aresta],
    direcionado: bool = False
) -> Grafo:
    grafo = criar_grafo_vazio()

    for municipio in municipios:
        adicionar_vertice(grafo, municipio[0])

    for origem, destino, peso in arestas:
        adicionar_aresta(grafo, origem, destino, peso, direcionado)

    return grafo


def obter_vizinhos(grafo: Grafo, id_municipio: int) -> List[Tuple[int, float]]:
    return grafo.get(id_municipio, [])


def numero_vertices(grafo: Grafo) -> int:
    return len(grafo)


def numero_arestas(grafo: Grafo, direcionado: bool = False) -> int:
    total = sum(len(vizinhos) for vizinhos in grafo.values())

    if direcionado:
        return total

    return total // 2


def listar_arestas(grafo: Grafo, direcionado: bool = False) -> List[Aresta]:
    arestas: List[Aresta] = []
    visitadas = set()

    for origem, vizinhos in grafo.items():
        for destino, peso in vizinhos:
            if direcionado:
                arestas.append((origem, destino, peso))
            else:
                chave = tuple(sorted((origem, destino)))

                if chave not in visitadas:
                    visitadas.add(chave)
                    arestas.append((origem, destino, peso))

    return arestas


def criar_mapa_municipios(municipios: List[Municipio]) -> Dict[int, Municipio]:
    return {municipio[0]: municipio for municipio in municipios}


def construir_bst_por_risco(municipios: List[Municipio]) -> BinarySearchTree:
    bst = BinarySearchTree()

    for municipio in municipios:
        bst.inserir(municipio)

    return bst


def filtrar_subgrafo(
    grafo: Grafo,
    vertices_selecionados: List[int]
) -> Grafo:
    selecionados = set(vertices_selecionados)
    subgrafo: Grafo = {}

    for origem in vertices_selecionados:
        subgrafo[origem] = []

        for destino, peso in grafo.get(origem, []):
            if destino in selecionados:
                subgrafo[origem].append((destino, peso))

    return subgrafo


def validar_grafo(grafo: Grafo) -> bool:
    for origem, vizinhos in grafo.items():
        if not isinstance(origem, int):
            return False

        if not isinstance(vizinhos, list):
            return False

        for destino, peso in vizinhos:
            if not isinstance(destino, int):
                return False

            if not isinstance(peso, (int, float)):
                return False

            if peso < 0:
                return False

    return True