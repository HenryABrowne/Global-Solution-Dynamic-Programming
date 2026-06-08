from math import inf

from src.brute_force import (
    calcular_custo_caminho,
    calcular_gap_otimalidade,
    forca_bruta_caminhos,
)
from src.data_structures import (
    adicionar_aresta,
    construir_bst_por_risco,
    construir_grafo,
    filtrar_subgrafo,
    listar_arestas,
    numero_arestas,
    numero_vertices,
    validar_grafo,
)
from src.greedy import (
    dijkstra,
    melhor_rota_prioritaria,
    prim_mst,
    reconstruir_caminho,
    selecionar_municipios_alto_risco,
)


def grafo_teste():
    return {
        1: [(2, 2.0), (3, 5.0)],
        2: [(1, 2.0), (3, 1.0), (4, 4.0)],
        3: [(1, 5.0), (2, 1.0), (4, 1.0)],
        4: [(2, 4.0), (3, 1.0)],
    }


def municipios_teste():
    return [
        (1, "A", 0.50, 1000.0, 10000),
        (2, "B", 0.80, 1500.0, 20000),
        (3, "C", 0.65, 1200.0, 15000),
        (4, "D", 0.90, 1800.0, 30000),
        (5, "E", 0.70, 1100.0, 12000),
    ]


def test_construir_grafo():
    municipios = municipios_teste()

    arestas = [
        (1, 2, 2.0),
        (2, 3, 1.0),
        (3, 4, 1.0),
    ]

    grafo = construir_grafo(municipios, arestas)

    assert numero_vertices(grafo) == 5
    assert numero_arestas(grafo) == 3
    assert validar_grafo(grafo) is True


def test_adicionar_aresta():
    grafo = {}

    adicionar_aresta(grafo, 1, 2, 3.5)

    assert 1 in grafo
    assert 2 in grafo
    assert (2, 3.5) in grafo[1]
    assert (1, 3.5) in grafo[2]


def test_listar_arestas_sem_duplicidade():
    grafo = grafo_teste()
    arestas = listar_arestas(grafo)

    assert len(arestas) == 5


def test_filtrar_subgrafo():
    grafo = grafo_teste()
    subgrafo = filtrar_subgrafo(grafo, [1, 2, 3])

    assert 4 not in subgrafo
    assert (4, 4.0) not in subgrafo[2]
    assert (4, 1.0) not in subgrafo[3]


def test_bst_inserir_e_tamanho():
    bst = construir_bst_por_risco(municipios_teste())

    assert len(bst) == 5
    assert bst.is_empty() is False


def test_bst_percurso_in_order():
    bst = construir_bst_por_risco(municipios_teste())

    municipios_ordenados = bst.percurso_in_order()
    riscos = [municipio[2] for municipio in municipios_ordenados]

    assert riscos == sorted(riscos)


def test_bst_buscar_intervalo():
    bst = construir_bst_por_risco(municipios_teste())

    resultado = bst.buscar_intervalo(0.70, 0.90)
    ids = [municipio[0] for municipio in resultado]

    assert 2 in ids
    assert 4 in ids
    assert 5 in ids
    assert 1 not in ids


def test_bst_altura():
    bst = construir_bst_por_risco(municipios_teste())

    assert bst.altura() >= 1


def test_bst_buscar_por_id():
    bst = construir_bst_por_risco(municipios_teste())

    municipio = bst.buscar_por_id(3)

    assert municipio is not None
    assert municipio[1] == "C"


def test_bst_remover():
    bst = construir_bst_por_risco(municipios_teste())

    removido = bst.remover(3)

    assert removido is True
    assert len(bst) == 4
    assert bst.buscar_por_id(3) is None


def test_bst_remover_inexistente():
    bst = construir_bst_por_risco(municipios_teste())

    removido = bst.remover(999)

    assert removido is False
    assert len(bst) == 5


def test_calcular_custo_caminho():
    grafo = grafo_teste()

    custo = calcular_custo_caminho(grafo, [1, 2, 3, 4])

    assert custo == 4.0


def test_calcular_custo_caminho_invalido():
    grafo = grafo_teste()

    custo = calcular_custo_caminho(grafo, [1, 4])

    assert custo == inf


def test_forca_bruta_caminhos():
    grafo = grafo_teste()

    resultado = forca_bruta_caminhos(grafo, 1, 4)

    assert resultado.melhor_caminho == [1, 2, 3, 4]
    assert resultado.melhor_custo == 4.0
    assert resultado.caminhos_avaliados > 0
    assert resultado.chamadas_recursivas > 0


def test_forca_bruta_origem_inexistente():
    grafo = grafo_teste()

    resultado = forca_bruta_caminhos(grafo, 99, 4)

    assert resultado.melhor_caminho == []
    assert resultado.melhor_custo == inf


def test_dijkstra_caminho_minimo():
    grafo = grafo_teste()

    resultado = dijkstra(grafo, 1, 4)

    assert resultado.caminho == [1, 2, 3, 4]
    assert resultado.custo_total == 4.0
    assert resultado.arestas_relaxadas > 0
    assert resultado.insercoes_heap > 0


def test_reconstruir_caminho():
    predecessores = {
        1: None,
        2: 1,
        3: 2,
        4: 3,
    }

    caminho = reconstruir_caminho(predecessores, 1, 4)

    assert caminho == [1, 2, 3, 4]


def test_reconstruir_caminho_inexistente():
    predecessores = {
        1: None,
        2: None,
        3: None,
        4: None,
    }

    caminho = reconstruir_caminho(predecessores, 1, 4)

    assert caminho == []


def test_forca_bruta_e_dijkstra_mesmo_resultado():
    grafo = grafo_teste()

    resultado_fb = forca_bruta_caminhos(grafo, 1, 4)
    resultado_dijkstra = dijkstra(grafo, 1, 4)

    assert resultado_fb.melhor_custo == resultado_dijkstra.custo_total
    assert resultado_fb.melhor_caminho == resultado_dijkstra.caminho


def test_gap_otimalidade_zero():
    gap = calcular_gap_otimalidade(100.0, 100.0)

    assert gap == 0.0


def test_gap_otimalidade_positivo():
    gap = calcular_gap_otimalidade(100.0, 125.0)

    assert gap == 25.0


def test_prim_mst():
    grafo = grafo_teste()

    resultado = prim_mst(grafo, origem=1)

    assert resultado.origem == 1
    assert len(resultado.arestas_mst) == 3
    assert resultado.custo_total == 4.0
    assert resultado.vertices_visitados == 4
    assert resultado.insercoes_heap > 0
    assert resultado.arestas_avaliadas > 0


def test_prim_mst_grafo_vazio():
    resultado = prim_mst({})

    assert resultado.origem == -1
    assert resultado.arestas_mst == []
    assert resultado.custo_total == 0.0
    assert resultado.vertices_visitados == 0


def test_selecionar_municipios_alto_risco():
    bst = construir_bst_por_risco(municipios_teste())

    resultado = selecionar_municipios_alto_risco(
        bst,
        risco_minimo=0.70,
        risco_maximo=1.00
    )

    ids = [municipio[0] for municipio in resultado]

    assert 2 in ids
    assert 4 in ids
    assert 5 in ids
    assert 1 not in ids


def test_melhor_rota_prioritaria():
    grafo = grafo_teste()
    bst = construir_bst_por_risco(municipios_teste())

    resultado = melhor_rota_prioritaria(
        grafo=grafo,
        origem=1,
        bst=bst,
        risco_minimo=0.70,
        risco_maximo=1.00
    )

    assert resultado is not None
    assert resultado.origem == 1
    assert resultado.destino in [2, 4, 5]

    if resultado.destino == 5:
        assert resultado.caminho == []

    else:
        assert resultado.caminho[0] == 1