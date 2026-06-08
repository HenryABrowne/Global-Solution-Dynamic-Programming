import csv
import json
from pathlib import Path
from typing import Dict, List, Any

try:
    from src.data_structures import Municipio, Aresta, Grafo, construir_grafo
except ImportError:
    from data_structures import Municipio, Aresta, Grafo, construir_grafo


def ler_municipios_csv(caminho: str) -> List[Municipio]:
    municipios: List[Municipio] = []

    with open(caminho, mode="r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            municipio: Municipio = (
                int(linha["id_municipio"]),
                str(linha["nome"]),
                float(linha["indice_risco"]),
                float(linha["custo_atendimento"]),
                int(linha["populacao"]),
            )
            municipios.append(municipio)

    return municipios


def ler_arestas_csv(caminho: str) -> List[Aresta]:
    arestas: List[Aresta] = []

    with open(caminho, mode="r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            aresta: Aresta = (
                int(linha["origem"]),
                int(linha["destino"]),
                float(linha["peso"]),
            )
            arestas.append(aresta)

    return arestas


def carregar_cenario(
    caminho_municipios: str,
    caminho_arestas: str,
    direcionado: bool = False
) -> tuple[List[Municipio], List[Aresta], Grafo]:
    municipios = ler_municipios_csv(caminho_municipios)
    arestas = ler_arestas_csv(caminho_arestas)
    grafo = construir_grafo(municipios, arestas, direcionado=direcionado)

    return municipios, arestas, grafo


def salvar_json(dados: Any, caminho: str) -> None:
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode="w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_json(caminho: str) -> Any:
    with open(caminho, mode="r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def grafo_para_json(grafo: Grafo) -> Dict[str, List[Dict[str, float]]]:
    grafo_json: Dict[str, List[Dict[str, float]]] = {}

    for origem, vizinhos in grafo.items():
        grafo_json[str(origem)] = [
            {
                "destino": destino,
                "peso": peso
            }
            for destino, peso in vizinhos
        ]

    return grafo_json


def json_para_grafo(dados: Dict[str, List[Dict[str, float]]]) -> Grafo:
    grafo: Grafo = {}

    for origem, vizinhos in dados.items():
        grafo[int(origem)] = [
            (int(vizinho["destino"]), float(vizinho["peso"]))
            for vizinho in vizinhos
        ]

    return grafo


def municipios_para_json(municipios: List[Municipio]) -> List[Dict[str, Any]]:
    return [
        {
            "id_municipio": municipio[0],
            "nome": municipio[1],
            "indice_risco": municipio[2],
            "custo_atendimento": municipio[3],
            "populacao": municipio[4],
        }
        for municipio in municipios
    ]


def json_para_municipios(dados: List[Dict[str, Any]]) -> List[Municipio]:
    return [
        (
            int(item["id_municipio"]),
            str(item["nome"]),
            float(item["indice_risco"]),
            float(item["custo_atendimento"]),
            int(item["populacao"]),
        )
        for item in dados
    ]


def salvar_cenario_processado(
    municipios: List[Municipio],
    grafo: Grafo,
    caminho_municipios: str,
    caminho_grafo: str
) -> None:
    salvar_json(municipios_para_json(municipios), caminho_municipios)
    salvar_json(grafo_para_json(grafo), caminho_grafo)


def carregar_cenario_processado(
    caminho_municipios: str,
    caminho_grafo: str
) -> tuple[List[Municipio], Grafo]:
    municipios = json_para_municipios(carregar_json(caminho_municipios))
    grafo = json_para_grafo(carregar_json(caminho_grafo))

    return municipios, grafo
