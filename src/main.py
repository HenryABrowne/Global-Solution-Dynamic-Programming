from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import List

try:
    from src.brute_force import forca_bruta_caminhos
    from src.data_loader import (
        carregar_cenario,
        salvar_cenario_processado,
        salvar_json,
    )
    from src.data_structures import (
        Aresta,
        Municipio,
        construir_bst_por_risco,
        criar_mapa_municipios,
    )
    from src.greedy import (
        dijkstra,
        melhor_rota_prioritaria,
        ordenar_municipios_por_prioridade,
        prim_mst,
        selecionar_municipios_alto_risco,
    )
    from src.performance_monitor import (
        executar_benchmark_tamanhos,
        salvar_resultados_csv,
    )
    from src.visualizations import gerar_figuras_obrigatorias
except ImportError:
    from brute_force import forca_bruta_caminhos
    from data_loader import (
        carregar_cenario,
        salvar_cenario_processado,
        salvar_json,
    )
    from data_structures import (
        Aresta,
        Municipio,
        construir_bst_por_risco,
        criar_mapa_municipios,
    )
    from greedy import (
        dijkstra,
        melhor_rota_prioritaria,
        ordenar_municipios_por_prioridade,
        prim_mst,
        selecionar_municipios_alto_risco,
    )
    from performance_monitor import (
        executar_benchmark_tamanhos,
        salvar_resultados_csv,
    )
    from visualizations import gerar_figuras_obrigatorias


TAMANHOS_TESTE = [5, 8, 10, 12, 20, 50, 100]


def arquivo_csv_valido(caminho: str) -> bool:
    path = Path(caminho)

    if not path.exists():
        return False

    try:
        with open(path, mode="r", encoding="utf-8-sig") as arquivo:
            linhas = [
                linha.strip()
                for linha in arquivo.readlines()
                if linha.strip()
            ]

        return len(linhas) > 1

    except OSError:
        return False


def gerar_municipios_sinteticos(
    id_base: int,
    prefixo_nome: str,
    quantidade: int
) -> List[Municipio]:
    municipios: List[Municipio] = []

    for i in range(quantidade):
        id_municipio = id_base + i
        nome = f"{prefixo_nome} {i + 1}"
        indice_risco = round(0.35 + ((i * 17) % 60) / 100, 2)
        custo_atendimento = round(900 + ((i * 137) % 1800), 2)
        populacao = 15000 + ((i * 7919) % 900000)

        municipios.append(
            (
                id_municipio,
                nome,
                indice_risco,
                custo_atendimento,
                populacao,
            )
        )

    return municipios


def gerar_arestas_sinteticas(
    municipios: List[Municipio]
) -> List[Aresta]:
    arestas: List[Aresta] = []

    ids = [municipio[0] for municipio in municipios]

    if len(ids) < 2:
        return arestas

    origem = ids[0]
    destino = ids[-1]

    for i in range(len(ids) - 1):
        peso = round(1.0 + ((i * 11) % 30) / 10, 2)
        arestas.append((ids[i], ids[i + 1], peso))

    for i in range(1, len(ids) - 1):
        peso_origem = round(1.5 + ((i * 7) % 35) / 10, 2)
        peso_destino = round(1.2 + ((i * 5) % 32) / 10, 2)

        arestas.append((origem, ids[i], peso_origem))
        arestas.append((ids[i], destino, peso_destino))

    for i in range(1, len(ids) - 4, 3):
        peso = round(2.0 + ((i * 13) % 25) / 10, 2)
        arestas.append((ids[i], ids[i + 3], peso))

    arestas.append((origem, destino, 8.5))

    return remover_arestas_duplicadas(arestas)


def remover_arestas_duplicadas(arestas: List[Aresta]) -> List[Aresta]:
    vistas = set()
    resultado: List[Aresta] = []

    for origem, destino, peso in arestas:
        chave = tuple(sorted((origem, destino)))

        if chave not in vistas:
            vistas.add(chave)
            resultado.append((origem, destino, peso))

    return resultado


def salvar_csv_municipios(
    municipios: List[Municipio],
    caminho: str
) -> None:
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode="w", encoding="utf-8", newline="") as arquivo:
        arquivo.write(
            "id_municipio,nome,indice_risco,custo_atendimento,populacao\n"
        )

        for municipio in municipios:
            arquivo.write(
                f"{municipio[0]},{municipio[1]},{municipio[2]},"
                f"{municipio[3]},{municipio[4]}\n"
            )


def salvar_csv_arestas(
    arestas: List[Aresta],
    caminho: str
) -> None:
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode="w", encoding="utf-8", newline="") as arquivo:
        arquivo.write("origem,destino,peso\n")

        for origem, destino, peso in arestas:
            arquivo.write(f"{origem},{destino},{peso}\n")


def preparar_dados_sinteticos() -> None:
    cenarios = [
        (
            "rs",
            4310000,
            "Municipio RS",
            "data/raw/municipios_rs.csv",
            "data/raw/rotas_rs.csv",
        ),
        (
            "matopiba",
            1700000,
            "Municipio MATOPIBA",
            "data/raw/municipios_matopiba.csv",
            "data/raw/rotas_matopiba.csv",
        ),
    ]

    for _, id_base, prefixo, caminho_municipios, caminho_rotas in cenarios:
        if arquivo_csv_valido(caminho_municipios) and arquivo_csv_valido(caminho_rotas):
            continue

        municipios = gerar_municipios_sinteticos(id_base, prefixo, 100)
        arestas = gerar_arestas_sinteticas(municipios)

        salvar_csv_municipios(municipios, caminho_municipios)
        salvar_csv_arestas(arestas, caminho_rotas)


def salvar_priorizacao_bst(
    municipios_prioritarios: List[Municipio],
    caminho: str
) -> None:
    dados = [
        {
            "id_municipio": municipio[0],
            "nome": municipio[1],
            "indice_risco": municipio[2],
            "custo_atendimento": municipio[3],
            "populacao": municipio[4],
        }
        for municipio in municipios_prioritarios
    ]

    salvar_json(dados, caminho)


def salvar_resultado_rota_prioritaria(
    resultado,
    caminho: str
) -> None:
    if resultado is None:
        salvar_json({}, caminho)
        return

    salvar_json(
        {
            "origem": resultado.origem,
            "destino": resultado.destino,
            "caminho": resultado.caminho,
            "custo_total": resultado.custo_total,
            "vertices_visitados": resultado.vertices_visitados,
            "arestas_relaxadas": resultado.arestas_relaxadas,
            "insercoes_heap": resultado.insercoes_heap,
        },
        caminho
    )


def salvar_resultado_mst(
    resultado,
    caminho: str
) -> None:
    salvar_json(
        {
            "origem": resultado.origem,
            "arestas_mst": [
                {
                    "origem": origem,
                    "destino": destino,
                    "peso": peso,
                }
                for origem, destino, peso in resultado.arestas_mst
            ],
            "custo_total": resultado.custo_total,
            "vertices_visitados": resultado.vertices_visitados,
            "insercoes_heap": resultado.insercoes_heap,
            "arestas_avaliadas": resultado.arestas_avaliadas,
        },
        caminho
    )


def processar_cenario(
    nome_cenario: str,
    caminho_municipios_raw: str,
    caminho_rotas_raw: str,
    caminho_municipios_processed: str,
    caminho_grafo_processed: str,
    caminho_bst_processed: str,
    caminho_resultados: str,
    caminho_priorizacao: str,
    caminho_rota_prioritaria: str,
    caminho_mst: str,
    pasta_figuras: str
) -> None:
    municipios, _, grafo = carregar_cenario(
        caminho_municipios_raw,
        caminho_rotas_raw,
        direcionado=False
    )

    if not municipios:
        raise ValueError(
            f"Nenhum município foi carregado em {caminho_municipios_raw}. "
            "Verifique se o CSV possui dados além do cabeçalho."
        )

    if not grafo:
        raise ValueError(
            f"Nenhum grafo foi carregado a partir de {caminho_rotas_raw}. "
            "Verifique se o CSV possui arestas válidas."
        )

    bst = construir_bst_por_risco(municipios)
    mapa_municipios = criar_mapa_municipios(municipios)

    salvar_cenario_processado(
        municipios,
        grafo,
        caminho_municipios_processed,
        caminho_grafo_processed
    )

    salvar_json(
        bst.to_list(),
        caminho_bst_processed
    )

    origem = municipios[0][0]
    destino = municipios[-1][0]

    municipios_alto_risco = selecionar_municipios_alto_risco(
        bst,
        risco_minimo=0.70,
        risco_maximo=1.00
    )

    municipios_prioritarios = ordenar_municipios_por_prioridade(
        municipios_alto_risco
    )

    salvar_priorizacao_bst(
        municipios_prioritarios,
        caminho_priorizacao
    )

    rota_prioritaria = melhor_rota_prioritaria(
        grafo=grafo,
        origem=origem,
        bst=bst,
        risco_minimo=0.70,
        risco_maximo=1.00
    )

    salvar_resultado_rota_prioritaria(
        rota_prioritaria,
        caminho_rota_prioritaria
    )

    resultado_mst = prim_mst(grafo, origem=origem)

    salvar_resultado_mst(
        resultado_mst,
        caminho_mst
    )

    resultados = executar_benchmark_tamanhos(
        grafo=grafo,
        tamanhos=TAMANHOS_TESTE,
        origem=origem,
        destino=destino,
        cenario=nome_cenario,
        funcao_forca_bruta=forca_bruta_caminhos,
        funcao_gulosa=dijkstra,
        limite_forca_bruta=12
    )

    salvar_resultados_csv(
        resultados,
        caminho_resultados
    )

    resultados_dict = [
        asdict(resultado)
        for resultado in resultados
    ]

    melhor_rota = dijkstra(grafo, origem, destino)

    gerar_figuras_obrigatorias(
        grafo=grafo,
        bst=bst,
        resultados=resultados_dict,
        municipios=mapa_municipios,
        caminho_destaque=melhor_rota.caminho,
        arestas_mst=resultado_mst.arestas_mst,
        pasta_saida=pasta_figuras
    )


def main() -> None:
    preparar_dados_sinteticos()

    processar_cenario(
        nome_cenario="Enchentes no Rio Grande do Sul",
        caminho_municipios_raw="data/raw/municipios_rs.csv",
        caminho_rotas_raw="data/raw/rotas_rs.csv",
        caminho_municipios_processed="data/processed/municipios_rs.json",
        caminho_grafo_processed="data/processed/grafo_rs.json",
        caminho_bst_processed="data/processed/bst_rs.json",
        caminho_resultados="data/processed/resultados_rs.csv",
        caminho_priorizacao="data/processed/priorizacao_bst_rs.json",
        caminho_rota_prioritaria="data/processed/rota_prioritaria_rs.json",
        caminho_mst="data/processed/mst_rs.json",
        pasta_figuras="report/figuras/rs"
    )

    processar_cenario(
        nome_cenario="Seca no MATOPIBA",
        caminho_municipios_raw="data/raw/municipios_matopiba.csv",
        caminho_rotas_raw="data/raw/rotas_matopiba.csv",
        caminho_municipios_processed="data/processed/municipios_matopiba.json",
        caminho_grafo_processed="data/processed/grafo_matopiba.json",
        caminho_bst_processed="data/processed/bst_matopiba.json",
        caminho_resultados="data/processed/resultados_matopiba.csv",
        caminho_priorizacao="data/processed/priorizacao_bst_matopiba.json",
        caminho_rota_prioritaria="data/processed/rota_prioritaria_matopiba.json",
        caminho_mst="data/processed/mst_matopiba.json",
        pasta_figuras="report/figuras/matopiba"
    )


if __name__ == "__main__":
    main()