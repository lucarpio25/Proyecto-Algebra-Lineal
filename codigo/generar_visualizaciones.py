"""
generar_visualizaciones.py
==========================
Genera TODAS las figuras del proyecto y las guarda en figuras/.

Figuras:
    1. Red base coloreada por categoría
    2. Red con nodos proporcionales a PageRank uniforme
    3. Red con nodos proporcionales a PageRank personalizado (tech)
    4. Red con nodos proporcionales a PageRank personalizado (deportes)
    5. Gráfica de convergencia (residuo vs iteraciones) para cada α
    6. Barras comparativas de los top 10 rankings
    7. Comparación antes/después de modificaciones de enlaces
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from red_definicion import (
    crear_grafo, NODOS_ORDEN, NODOS_INFO,
    NODOS_TECH, NODOS_DEP, NODOS_CUL,
    obtener_categorias_color,
)
from pagerank_core import (
    construir_matriz_P,
    vector_reinicio_uniforme,
    vector_reinicio_personalizado,
    pagerank_iterativo,
    pagerank_networkx,
    dict_personalizacion_nx,
)

DIR_FIGURAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figuras')
os.makedirs(DIR_FIGURAS, exist_ok=True)

# Configuración global de matplotlib
plt.rcParams.update({
    'figure.dpi': 150,
    'font.size': 10,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
})


def obtener_layout(G):
    """Layout fijo para todas las figuras de la red."""
    return nx.spring_layout(G, seed=42, k=1.8, iterations=60)


def colores_nodos(G):
    """Lista de colores según categoría de cada nodo."""
    cat_col = obtener_categorias_color()
    return [cat_col[G.nodes[n]['categoria']] for n in G.nodes()]


def leyenda_categorias():
    """Parches para la leyenda de categorías."""
    cat_col = obtener_categorias_color()
    return [
        mpatches.Patch(color=cat_col['tecnologia'], label='Tecnología'),
        mpatches.Patch(color=cat_col['deportes'],   label='Deportes'),
        mpatches.Patch(color=cat_col['cultura'],    label='Cultura'),
    ]


# =====================================================================
# FIG 1. RED BASE COLOREADA POR CATEGORÍA
# =====================================================================

def fig1_red_base(G):
    print("Generando Fig 1: Red base...")
    pos = obtener_layout(G)
    fig, ax = plt.subplots(figsize=(14, 10))

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#bdc3c7',
                           arrows=True, arrowsize=15, width=1.0,
                           connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colores_nodos(G),
                           node_size=800, edgecolors='white', linewidths=1.5)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight='bold')

    ax.set_title('Red de 20 páginas web — Estructura de enlaces')
    ax.legend(handles=leyenda_categorias(), loc='upper left', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_FIGURAS, 'fig1_red_base.png'), bbox_inches='tight')
    plt.close(fig)
    print("  → fig1_red_base.png")


# =====================================================================
# FIG 2-4. RED CON TAMAÑOS PROPORCIONALES A PAGERANK
# =====================================================================

def fig_red_pagerank(G, scores_dict, titulo, nombre_archivo, pos=None):
    """Dibuja la red con tamaños de nodo proporcionales a las puntuaciones."""
    if pos is None:
        pos = obtener_layout(G)

    fig, ax = plt.subplots(figsize=(14, 10))

    # Área de los nodos proporcional a PageRank.
    # Se utiliza la misma escala para las tres variantes.
    scores = np.array([scores_dict[n] for n in G.nodes()])
    tamaños = 25000 * scores

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#bdc3c7',
                           arrows=True, arrowsize=12, width=0.8,
                           connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colores_nodos(G),
                           node_size=tamaños, edgecolors='white', linewidths=1.5)

    # Etiquetas con puntuación
    labels = {n: f"{n}\n{scores_dict.get(n, 0):.3f}" for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7)

    ax.set_title(titulo)
    ax.legend(handles=leyenda_categorias(), loc='upper left', fontsize=10)
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_FIGURAS, nombre_archivo), bbox_inches='tight')
    plt.close(fig)
    print(f"  → {nombre_archivo}")


def fig2_3_4_redes_pagerank(G, P):
    print("Generando Fig 2-4: Redes con PageRank...")
    pos = obtener_layout(G)
    alpha = 0.85
    n = len(NODOS_ORDEN)

    # Uniforme
    v_uni = vector_reinicio_uniforme(n)
    r_uni, _, _ = pagerank_iterativo(P, alpha, v_uni)
    scores_uni = {NODOS_ORDEN[i]: r_uni[i] for i in range(n)}
    fig_red_pagerank(G, scores_uni,
                     'PageRank Uniforme (α = 0.85)',
                     'fig2_red_pagerank_uniforme.png', pos)

    # Personalizado tecnología
    v_tech = vector_reinicio_personalizado('tecnologia')
    r_tech, _, _ = pagerank_iterativo(P, alpha, v_tech)
    scores_tech = {NODOS_ORDEN[i]: r_tech[i] for i in range(n)}
    fig_red_pagerank(G, scores_tech,
                     'PageRank Personalizado — Preferencia Tecnología (α = 0.85)',
                     'fig3_red_pagerank_tech.png', pos)

    # Personalizado deportes
    v_dep = vector_reinicio_personalizado('deportes')
    r_dep, _, _ = pagerank_iterativo(P, alpha, v_dep)
    scores_dep = {NODOS_ORDEN[i]: r_dep[i] for i in range(n)}
    fig_red_pagerank(G, scores_dep,
                     'PageRank Personalizado — Preferencia Deportes (α = 0.85)',
                     'fig4_red_pagerank_deportes.png', pos)


# =====================================================================
# FIG 5. CONVERGENCIA POR α
# =====================================================================

def fig5_convergencia(P):
    print("Generando Fig 5: Convergencia por α...")
    alphas = [0.50, 0.85, 0.95, 0.99]
    colores_alpha = ['#3498db', '#2ecc71', '#e67e22', '#e74c3c']
    n = len(NODOS_ORDEN)
    v = vector_reinicio_uniforme(n)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Panel izquierdo: residuo vs iteraciones
    ax1 = axes[0]
    max_iters_plot = 0
    for alpha, color in zip(alphas, colores_alpha):
        _, iters, residuos = pagerank_iterativo(P, alpha, v)
        ax1.semilogy(range(1, len(residuos)+1), residuos,
                     label=f'α = {alpha} ({iters} iter.)',
                     color=color, linewidth=2)
        max_iters_plot = max(max_iters_plot, len(residuos))

    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Residuo $\\|r - \\alpha P r - (1-\\alpha)v\\|_1$')
    ax1.set_title('Convergencia del método iterativo')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, min(max_iters_plot + 5, 200))

    # Panel derecho: número de iteraciones (barras)
    ax2 = axes[1]
    iters_list = []
    for alpha in alphas:
        _, iters, _ = pagerank_iterativo(P, alpha, v)
        iters_list.append(iters)

    bars = ax2.bar([f'α = {a}' for a in alphas], iters_list,
                   color=colores_alpha, edgecolor='white', linewidth=1.5)
    for bar, it in zip(bars, iters_list):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 str(it), ha='center', va='bottom', fontweight='bold')

    ax2.set_ylabel('Número de iteraciones')
    ax2.set_title('Iteraciones necesarias para converger')
    ax2.grid(True, alpha=0.3, axis='y')

    fig.suptitle('Efecto del parámetro α en la convergencia de PageRank',
                 fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_FIGURAS, 'fig5_convergencia_alpha.png'),
                bbox_inches='tight')
    plt.close(fig)
    print("  → fig5_convergencia_alpha.png")


# =====================================================================
# FIG 6. BARRAS COMPARATIVAS DE RANKINGS
# =====================================================================

def fig6_barras_rankings(G, P):
    print("Generando Fig 6: Barras comparativas de rankings...")
    alpha = 0.85
    n = len(NODOS_ORDEN)

    # Calcular todos los rankings
    in_deg = np.array([G.in_degree(nd) for nd in NODOS_ORDEN])

    v_uni = vector_reinicio_uniforme(n)
    r_uni, _, _ = pagerank_iterativo(P, alpha, v_uni)

    v_tech = vector_reinicio_personalizado('tecnologia')
    r_tech, _, _ = pagerank_iterativo(P, alpha, v_tech)

    v_dep = vector_reinicio_personalizado('deportes')
    r_dep, _, _ = pagerank_iterativo(P, alpha, v_dep)

    # Ordenar por PR uniforme
    orden = np.argsort(-r_uni)

    fig, axes = plt.subplots(2, 1, figsize=(16, 12))

    # Panel superior: In-degree vs PageRank uniforme
    ax1 = axes[0]
    x = np.arange(n)
    width = 0.35

    nodos_ord = [NODOS_ORDEN[i] for i in orden]
    cat_col = obtener_categorias_color()
    colores = [cat_col[NODOS_INFO[nd]['categoria']] for nd in nodos_ord]

    # Normalizar in-degree para comparar visualmente
    in_deg_norm = in_deg[orden] / in_deg.max()
    r_uni_norm  = r_uni[orden] / r_uni.max()

    ax1.bar(x - width/2, in_deg_norm, width, label='In-Degree (normalizado)',
            color='#95a5a6', edgecolor='white')
    ax1.bar(x + width/2, r_uni_norm, width, label='PageRank Uniforme (normalizado)',
            color=colores, edgecolor='white')

    ax1.set_xticks(x)
    ax1.set_xticklabels(nodos_ord, rotation=45, ha='right')
    ax1.set_ylabel('Puntuación normalizada')
    ax1.set_title('In-Degree vs. PageRank Uniforme (α = 0.85)')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')

    # Panel inferior: Los 3 PageRank comparados
    ax2 = axes[1]
    width = 0.25

    ax2.bar(x - width, r_uni[orden], width, label='PR Uniforme',
            color='#3498db', edgecolor='white')
    ax2.bar(x, r_tech[orden], width, label='PR Tecnología',
            color='#e67e22', edgecolor='white')
    ax2.bar(x + width, r_dep[orden], width, label='PR Deportes',
            color='#2ecc71', edgecolor='white')

    ax2.set_xticks(x)
    ax2.set_xticklabels(nodos_ord, rotation=45, ha='right')
    ax2.set_ylabel('Puntuación PageRank')
    ax2.set_title('Comparación: Uniforme vs. Personalizado Tecnología vs. Personalizado Deportes')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')

    fig.tight_layout()
    fig.savefig(os.path.join(DIR_FIGURAS, 'fig6_barras_rankings.png'),
                bbox_inches='tight')
    plt.close(fig)
    print("  → fig6_barras_rankings.png")


# =====================================================================
# FIG 7. SENSIBILIDAD — ANTES Y DESPUÉS
# =====================================================================

def fig7_sensibilidad(G, P):
    print("Generando Fig 7: Sensibilidad a cambios...")
    alpha = 0.85
    n = len(NODOS_ORDEN)
    v = vector_reinicio_uniforme(n)

    # Base
    r_base, _, _ = pagerank_iterativo(P, alpha, v)

    # Modificaciones
    # Añadir
    G_add = G.copy()
    G_add.add_edges_from([('D3', 'T1'), ('C6', 'D1'), ('T5', 'C1')])
    P_add = construir_matriz_P(G_add)
    r_add, _, _ = pagerank_iterativo(P_add, alpha, v)

    # Quitar
    G_rm = G.copy()
    G_rm.remove_edges_from([('T2', 'T1'), ('D3', 'D1'), ('C3', 'C1')])
    P_rm = construir_matriz_P(G_rm)
    r_rm, _, _ = pagerank_iterativo(P_rm, alpha, v)

    # Dangling
    G_dang = G.copy()
    salidas_D6 = list(G_dang.successors('D6'))
    G_dang.remove_edges_from([('D6', s) for s in salidas_D6])
    P_dang = construir_matriz_P(G_dang)
    r_dang, _, _ = pagerank_iterativo(P_dang, alpha, v)

    fig, axes = plt.subplots(3, 1, figsize=(16, 15))

    x = np.arange(n)
    nodos_labels = NODOS_ORDEN

    # Panel 1: Añadir enlaces
    ax = axes[0]
    cambio = r_add - r_base
    colors = ['#2ecc71' if c >= 0 else '#e74c3c' for c in cambio]
    ax.bar(x, cambio, color=colors, edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels(nodos_labels, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Cambio en puntuación')
    ax.set_title('E6: Efecto de añadir enlaces (D3→T1, C6→D1, T5→C1)')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3, axis='y')

    # Panel 2: Quitar enlaces
    ax = axes[1]
    cambio = r_rm - r_base
    colors = ['#2ecc71' if c >= 0 else '#e74c3c' for c in cambio]
    ax.bar(x, cambio, color=colors, edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels(nodos_labels, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Cambio en puntuación')
    ax.set_title('E7: Efecto de quitar enlaces (T2→T1, D3→D1, C3→C1)')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3, axis='y')

    # Panel 3: Dangling node
    ax = axes[2]
    cambio = r_dang - r_base
    colors = ['#2ecc71' if c >= 0 else '#e74c3c' for c in cambio]
    ax.bar(x, cambio, color=colors, edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels(nodos_labels, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Cambio en puntuación')
    ax.set_title('E8: Efecto de convertir D6 en dangling node (sin enlaces de salida)')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3, axis='y')

    fig.suptitle('Sensibilidad de PageRank a cambios en la red',
                 fontsize=14, fontweight='bold', y=1.01)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_FIGURAS, 'fig7_sensibilidad.png'),
                bbox_inches='tight')
    plt.close(fig)
    print("  → fig7_sensibilidad.png")


# =====================================================================
# FIG 8. EFECTO DE α EN EL TOP 5
# =====================================================================

def fig8_top5_por_alpha(P):
    print("Generando Fig 8: Top 5 por α...")
    alphas = [0.50, 0.85, 0.95, 0.99]
    n = len(NODOS_ORDEN)
    v = vector_reinicio_uniforme(n)
    cat_col = obtener_categorias_color()

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    for idx, alpha in enumerate(alphas):
        ax = axes[idx]
        r, _, _ = pagerank_iterativo(P, alpha, v)

        # Top 10
        top10_idx = np.argsort(-r)[:10]
        nodos_top = [NODOS_ORDEN[i] for i in top10_idx]
        scores_top = r[top10_idx]
        colores = [cat_col[NODOS_INFO[nd]['categoria']] for nd in nodos_top]

        bars = ax.barh(range(9, -1, -1), scores_top, color=colores, edgecolor='white')
        ax.set_yticks(range(9, -1, -1))
        ax.set_yticklabels(nodos_top)
        ax.set_xlabel('Puntuación PageRank')
        ax.set_title(f'α = {alpha}')
        ax.grid(True, alpha=0.3, axis='x')

        # Anotar puntuaciones
        for bar, score in zip(bars, scores_top):
            ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                    f'{score:.4f}', va='center', fontsize=8)

    fig.suptitle('Top 10 de PageRank para distintos valores de α',
                 fontsize=14, fontweight='bold')
    fig.legend(handles=leyenda_categorias(), loc='lower center',
               ncol=3, fontsize=11, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_FIGURAS, 'fig8_top5_por_alpha.png'),
                bbox_inches='tight')
    plt.close(fig)
    print("  → fig8_top5_por_alpha.png")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     GENERANDO TODAS LAS VISUALIZACIONES                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    G = crear_grafo()
    P = construir_matriz_P(G)

    fig1_red_base(G)
    fig2_3_4_redes_pagerank(G, P)
    fig5_convergencia(P)
    fig6_barras_rankings(G, P)
    fig7_sensibilidad(G, P)
    fig8_top5_por_alpha(P)

    print(f"\n✓ Todas las figuras generadas en: {os.path.abspath(DIR_FIGURAS)}")


if __name__ == '__main__':
    main()

