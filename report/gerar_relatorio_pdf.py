from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Image,
    PageBreak,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "relatorio_final.pdf"
FIG = ROOT / "report" / "figuras"


INTEGRANTES = [
    "RM561474 - Eduardo Santiago Bassan",
    "RM562622 - Henry Andrade Browne",
    "RM561446 - João Victor Abe",
]


styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=15,
        leading=18,
        spaceAfter=8,
        textColor=colors.HexColor("#183A59"),
    )
)

styles.add(
    ParagraphStyle(
        name="H1Custom",
        parent=styles["Heading1"],
        fontSize=11.5,
        leading=13,
        spaceBefore=5,
        spaceAfter=4,
        textColor=colors.HexColor("#183A59"),
    )
)

styles.add(
    ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontSize=8.2,
        leading=10.2,
        spaceAfter=3,
    )
)

styles.add(
    ParagraphStyle(
        name="Caption",
        parent=styles["BodyText"],
        fontSize=7,
        leading=8.2,
        spaceBefore=2,
        spaceAfter=5,
    )
)


P = styles["BodyCustom"]
H = styles["H1Custom"]
C = styles["Caption"]


def p(txt):
    return Paragraph(txt, P)


def h(txt):
    return Paragraph(txt, H)


def caption(txt):
    return Paragraph(txt, C)


def tabela(dados, col_widths=None, font_size=7.3):
    t = Table(dados, colWidths=col_widths, repeatRows=1)

    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#183A59")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F4F7FA")),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    return t


def imagem(caminho, largura, altura_max):
    caminho = Path(caminho)

    if not caminho.exists():
        return tabela(
            [
                ["Figura não encontrada"],
                [str(caminho)],
            ],
            [largura],
            font_size=7,
        )

    img = Image(str(caminho))
    escala = min(largura / img.imageWidth, altura_max / img.imageHeight)

    img.drawWidth = img.imageWidth * escala
    img.drawHeight = img.imageHeight * escala

    return img


def bloco_figura(caminho, texto, largura=7.5 * cm, altura=4.7 * cm):
    return [
        imagem(caminho, largura, altura),
        caption(texto),
    ]


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0] - 1.5 * cm, 0.9 * cm, f"Página {doc.page}")
    canvas.restoreState()


def gerar():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=1.4 * cm,
        leftMargin=1.4 * cm,
        topMargin=1.25 * cm,
        bottomMargin=1.2 * cm,
    )

    story = []

    story.append(
        Paragraph(
            "Global Solution 2026 - Dynamic Programming",
            styles["TitleCustom"],
        )
    )

    story.append(
        p(
            "<b>Tema:</b> Monitoramento de Riscos Ambientais com Árvores, Grafos e Algoritmos."
        )
    )

    story.append(
        p(
            "<b>Integrantes:</b> " + "; ".join(INTEGRANTES)
        )
    )

    story.append(
        p(
            "<b>Cenários:</b> enchentes no Rio Grande do Sul e seca no MATOPIBA. "
            "Os dados são sintéticos e controlados para permitir reprodutibilidade, "
            "comparação por tamanho N e execução local sem dependência de APIs externas."
        )
    )

    story.append(h("1. Modelagem"))

    story.append(
        p(
            "O sistema representa municípios como vértices de um grafo ponderado G=(V,E). "
            "Cada vértice é uma tupla (id_municipio, nome, indice_risco, "
            "custo_atendimento, populacao), e cada aresta (u,v,peso) representa "
            "custo/tempo estimado de deslocamento. O grafo foi implementado como "
            "dicionário de listas de adjacência, pois essa estrutura consome O(V+E) "
            "espaço e é mais adequada a redes esparsas do que uma matriz O(V²)."
        )
    )

    story.append(
        p(
            "A BST foi implementada do zero com classes Node e BinarySearchTree, "
            "usando o índice de risco como chave principal e o id como desempate. "
            "Ela permite inserir, buscar por intervalo, percorrer em ordem, calcular "
            "altura e remover nós. A consulta [0.70, 1.00] identifica municípios "
            "críticos usados na priorização do atendimento."
        )
    )

    story.append(
        tabela(
            [
                ["Estrutura", "Aplicação no projeto"],
                ["list", "adjacência, caminhos, resultados e arestas da MST"],
                ["tuple", "municípios e arestas imutáveis"],
                ["dict", "grafo, distâncias, predecessores e metadados"],
                ["set", "visitados e prevenção de ciclos"],
                ["heapq", "fila de prioridade no Dijkstra e no Prim"],
                ["BST", "consulta de municípios por índice de risco"],
            ],
            [3.2 * cm, 14.2 * cm],
        )
    )

    story.append(h("2. Algoritmos e complexidade"))

    story.append(
        tabela(
            [
                ["Algoritmo", "Papel", "Tempo", "Espaço"],
                ["Força Bruta", "baseline ótimo em N pequeno", "combinatório/exponencial", "O(V) por caminho"],
                ["Dijkstra", "caminho mínimo guloso", "O((V+E) log V)", "O(V+E)"],
                ["Prim", "MST para cobertura mínima", "O(E log V)", "O(V+E)"],
                ["BST", "priorização por risco", "O(h+k) por intervalo", "O(n)"],
            ],
            [3.0 * cm, 6.1 * cm, 4.3 * cm, 4.0 * cm],
        )
    )

    story.append(
        p(
            "A Força Bruta foi limitada a N <= 12, pois enumera caminhos simples "
            "com backtracking e cresce rapidamente. O Dijkstra usa pesos não negativos "
            "e heap, mantendo boa escalabilidade. O Prim foi usado para gerar a MST "
            "e visualizar a cobertura mínima da rede."
        )
    )

    story.append(PageBreak())

    story.append(h("3. Resultados - grafos e BST"))

    story.append(
        p(
            "As figuras mostram a MST destacada e a BST de risco. A MST evidencia "
            "uma cobertura de custo mínimo da rede; a BST evidencia a ordenação por "
            "criticidade ambiental."
        )
    )

    story.append(
        Table(
            [
                [
                    bloco_figura(
                        FIG / "rs" / "grafo_mst.png",
                        "Figura 1 - MST do cenário RS. Arestas destacadas indicam a cobertura mínima calculada por Prim.",
                    ),
                    bloco_figura(
                        FIG / "matopiba" / "grafo_mst.png",
                        "Figura 2 - MST do cenário MATOPIBA. A rede simula maior custo logístico em algumas conexões.",
                    ),
                ],
                [
                    bloco_figura(
                        FIG / "rs" / "bst_riscos.png",
                        "Figura 3 - BST do RS com amostra de 15 municípios. O percurso in-order ordena os riscos.",
                    ),
                    bloco_figura(
                        FIG / "matopiba" / "bst_riscos.png",
                        "Figura 4 - BST do MATOPIBA com amostra de 15 municípios para legibilidade.",
                    ),
                ],
            ],
            colWidths=[8.6 * cm, 8.6 * cm],
            rowHeights=[9.2 * cm, 9.2 * cm],
        )
    )

    story.append(PageBreak())

    story.append(h("4. Resultados de desempenho"))

    story.append(
        p(
            "O monitoramento usa time.perf_counter() para tempo, tracemalloc para "
            "memória e contadores internos para operações elementares. No Dijkstra, "
            "o contador principal é o número de arestas relaxadas; na Força Bruta, "
            "são chamadas recursivas."
        )
    )

    story.append(
        Table(
            [
                [
                    bloco_figura(
                        FIG / "rs" / "desempenho_tempo_n.png",
                        "Figura 5 - Tempo x N no RS. A Força Bruta cresce rapidamente e só é usada como validação.",
                    ),
                    bloco_figura(
                        FIG / "matopiba" / "desempenho_tempo_n.png",
                        "Figura 6 - Tempo x N no MATOPIBA. O Dijkstra mantém execução estável em N maior.",
                    ),
                ],
                [
                    bloco_figura(
                        FIG / "rs" / "gap_otimalidade.png",
                        "Figura 7 - Gap de otimalidade. Com Dijkstra e pesos não negativos, o gap é 0% nas instâncias comparáveis.",
                    ),
                    bloco_figura(
                        FIG / "matopiba" / "operacoes_n.png",
                        "Figura 8 - Operações elementares. A diferença evidencia melhor escalabilidade do método guloso.",
                    ),
                ],
            ],
            colWidths=[8.6 * cm, 8.6 * cm],
            rowHeights=[9.0 * cm, 9.0 * cm],
        )
    )

    story.append(PageBreak())

    story.append(h("5. Escala de decisão e interpretação"))

    story.append(
        tabela(
            [
                ["Nível", "Critério", "Decisão prática"],
                ["Excelente", "gap próximo de 0%, baixo tempo e baixa memória", "usar em operação real"],
                ["Bom", "execução eficiente e pequeno custo computacional", "usar com monitoramento"],
                ["Regular", "tempo/memória crescem de forma perceptível", "limitar a instâncias médias"],
                ["Inviável", "explosão combinatória da Força Bruta", "não usar em produção"],
            ],
            [3.0 * cm, 8.8 * cm, 5.4 * cm],
        )
    )

    story.append(
        p(
            "No RS, a rota prioritária parte do hub inicial até o município crítico "
            "identificado pela BST. No MATOPIBA, o mesmo procedimento simula atendimento "
            "a municípios sob risco de seca. A MST complementa a decisão ao indicar uma "
            "estrutura de cobertura mínima da rede."
        )
    )

    story.append(
        p(
            "A solução recomendada é usar a BST para triagem de risco, Dijkstra para "
            "rotas de atendimento e Prim para planejamento de cobertura. A Força Bruta "
            "deve permanecer apenas como oráculo de validação em N pequeno, pois seu "
            "crescimento combinatório se torna inviável conforme a rede aumenta."
        )
    )

    story.append(h("6. Conclusão e ODS"))

    story.append(
        p(
            "O projeto conecta estruturas de dados e algoritmos a uma aplicação ambiental: "
            "priorizar municípios críticos, calcular rotas de menor custo e visualizar "
            "cobertura mínima. A solução se relaciona aos ODS 2, 9, 11 e 13 ao apoiar "
            "agricultura sustentável, infraestrutura resiliente, cidades sustentáveis e "
            "resposta à mudança climática."
        )
    )

    story.append(h("7. Referências"))

    story.append(
        p(
            "NASA Earthdata; INPE PRODES/DETER; ANA HidroWeb; INMET; IBGE; ANATEL; "
            "DNIT; Cormen et al., Introduction to Algorithms; Sedgewick & Wayne, "
            "Algorithms; Skiena, The Algorithm Design Manual."
        )
    )

    doc.build(story, onFirstPage=rodape, onLaterPages=rodape)

    print(f"PDF gerado em: {OUT}")


if __name__ == "__main__":
    gerar()