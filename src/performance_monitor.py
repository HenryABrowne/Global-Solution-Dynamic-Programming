from _future_ import annotations

import csv
import time
import tracemalloc
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

try:
    from src.data_structures import Grafo, filtrar_subgrafo
except ImportError:
    from data_structures import Grafo, filtrar_subgrafo


@dataclass
class ResultadoPerformance:
    algoritmo: str
    cenario: str
    n_vertices: int
    tempo_ms: float
    memoria_mb: float
    operacoes: int
    custo_solucao: float
    caminho: str
    extra: Dict[str, Any]


def medir_tempo_memoria(
    funcao: Callable[..., Any],
    *args: Any,
    **kwargs: Any
) -> tuple[Any, float, float]:
    tracemalloc.start()
    inicio = time.perf_counter()

    resultado = funcao(*args, **kwargs)

    fim = time.perf_counter()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tempo_ms = (fim - inicio) * 1000
    memoria_mb = memoria_pico / (1024 * 1024)

    return resultado, tempo_ms, memoria_mb


def extrair_valor(objeto: Any, atributo: str, padrao: Any = None) -> Any:
    if hasattr(objeto, atributo):
        return getattr(objeto, atributo)

    if isinstance(objeto, dict):
        return objeto.get(atributo, padrao)

    return padrao


def resultado_para_dict(resultado: Any) -> Dict[str, Any]:
    if is_dataclass(resultado):
        return asdict(resultado)

    if isinstance(resultado, dict):
        return resultado

    return {"resultado": str(resultado)}


def contar_operacoes(algoritmo: str, resultado: Any) -> int:
    nome = algoritmo.lower()

    if "forca" in nome or "bruta" in nome:
        return int(extrair_valor(resultado, "chamadas_recursivas", 0))

    if "dijkstra" in nome:
        return int(extrair_valor(resultado, "arestas_relaxadas", 0))

    if "prim" in nome or "kruskal" in nome:
        return int(extrair_valor(resultado, "insercoes_heap", 0))

    return 0


def extrair_custo(resultado: Any) -> float:
    custo = extrair_valor(resultado, "custo_total", None)

    if custo is not None:
        return float(custo)

    custo = extrair_valor(resultado, "melhor_custo", None)

    if custo is not None:
        return float(custo)

    return 0.0


def extrair_caminho(resultado: Any) -> str:
    caminho = extrair_valor(resultado, "caminho", None)

    if caminho is None:
        caminho = extrair_valor(resultado, "melhor_caminho", [])

    return " -> ".join(str(item) for item in caminho)


def executar_monitoramento(
    algoritmo: str,
    cenario: str,
    n_vertices: int,
    funcao: Callable[..., Any],
    *args: Any,
    **kwargs: Any
) -> ResultadoPerformance:
    resultado, tempo_ms, memoria_mb = medir_tempo_memoria(
        funcao,
        *args,
        **kwargs
    )

    return ResultadoPerformance(
        algoritmo=algoritmo,
        cenario=cenario,
        n_vertices=n_vertices,
        tempo_ms=tempo_ms,
        memoria_mb=memoria_mb,
        operacoes=contar_operacoes(algoritmo, resultado),
        custo_solucao=extrair_custo(resultado),
        caminho=extrair_caminho(resultado),
        extra=resultado_para_dict(resultado)
    )


def executar_benchmark_tamanhos(
    grafo: Grafo,
    tamanhos: List[int],
    origem: int,
    destino: int,
    cenario: str,
    funcao_forca_bruta: Optional[Callable[..., Any]] = None,
    funcao_gulosa: Optional[Callable[..., Any]] = None,
    limite_forca_bruta: int = 12
) -> List[ResultadoPerformance]:
    resultados: List[ResultadoPerformance] = []
    vertices = list(grafo.keys())

    for n in tamanhos:
        if n > len(vertices):
            continue

        vertices_selecionados = vertices[:n]

        if origem not in vertices_selecionados:
            vertices_selecionados[0] = origem

        if destino not in vertices_selecionados:
            vertices_selecionados[-1] = destino

        subgrafo = filtrar_subgrafo(grafo, vertices_selecionados)

        if funcao_forca_bruta is not None and n <= limite_forca_bruta:
            resultado_fb = executar_monitoramento(
                "Força Bruta",
                cenario,
                n,
                funcao_forca_bruta,
                subgrafo,
                origem,
                destino
            )
            resultados.append(resultado_fb)

        if funcao_gulosa is not None:
            resultado_guloso = executar_monitoramento(
                "Dijkstra",
                cenario,
                n,
                funcao_gulosa,
                subgrafo,
                origem,
                destino
            )
            resultados.append(resultado_guloso)

    return resultados


def salvar_resultados_csv(
    resultados: List[ResultadoPerformance],
    caminho: str
) -> None:
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)

    campos = [
        "algoritmo",
        "cenario",
        "n_vertices",
        "tempo_ms",
        "memoria_mb",
        "operacoes",
        "custo_solucao",
        "caminho"
    ]

    with open(path, mode="w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()

        for resultado in resultados:
            escritor.writerow(
                {
                    "algoritmo": resultado.algoritmo,
                    "cenario": resultado.cenario,
                    "n_vertices": resultado.n_vertices,
                    "tempo_ms": round(resultado.tempo_ms, 6),
                    "memoria_mb": round(resultado.memoria_mb, 6),
                    "operacoes": resultado.operacoes,
                    "custo_solucao": resultado.custo_solucao,
                    "caminho": resultado.caminho
                }
            )


def carregar_resultados_csv(caminho: str) -> List[Dict[str, Any]]:
    resultados: List[Dict[str, Any]] = []

    with open(caminho, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            resultados.append(
                {
                    "algoritmo": linha["algoritmo"],
                    "cenario": linha["cenario"],
                    "n_vertices": int(linha["n_vertices"]),
                    "tempo_ms": float(linha["tempo_ms"]),
                    "memoria_mb": float(linha["memoria_mb"]),
                    "operacoes": int(linha["operacoes"]),
                    "custo_solucao": float(linha["custo_solucao"]),
                    "caminho": linha["caminho"]
                }
            )

    return resultados
