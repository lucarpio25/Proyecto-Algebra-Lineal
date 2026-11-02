"""
red_definicion.py
=================
Define la red dirigida de 20 páginas web con tres categorías:
tecnología (T1–T7), deportes (D1–D7) y cultura (C1–C6).

Cada nodo representa una página web simulada y cada arista dirigida
representa un hipervínculo de la página origen hacia la página destino.

Las reglas de construcción están documentadas en datos/reglas_red.md.
"""

import networkx as nx

# =====================================================================
# 1. DEFINICIÓN DE NODOS
# =====================================================================

# Nodos con su categoría y nombre descriptivo
NODOS_INFO = {
    # ---------- TECNOLOGÍA ----------
    'T1': {'categoria': 'tecnologia', 'nombre': 'Portal Tecnología'},
    'T2': {'categoria': 'tecnologia', 'nombre': 'Blog de IA'},
    'T3': {'categoria': 'tecnologia', 'nombre': 'Reviews de Gadgets'},
    'T4': {'categoria': 'tecnologia', 'nombre': 'Noticias de Software'},
    'T5': {'categoria': 'tecnologia', 'nombre': 'Startups'},
    'T6': {'categoria': 'tecnologia', 'nombre': 'Programación'},
    'T7': {'categoria': 'tecnologia', 'nombre': 'Hardware'},
    # ---------- DEPORTES ----------
    'D1': {'categoria': 'deportes', 'nombre': 'Portal Deportes'},
    'D2': {'categoria': 'deportes', 'nombre': 'Fútbol'},
    'D3': {'categoria': 'deportes', 'nombre': 'Básquetbol'},
    'D4': {'categoria': 'deportes', 'nombre': 'Olimpiadas'},
    'D5': {'categoria': 'deportes', 'nombre': 'Tenis'},
    'D6': {'categoria': 'deportes', 'nombre': 'Fitness'},
    'D7': {'categoria': 'deportes', 'nombre': 'Esports'},
    # ---------- CULTURA ----------
    'C1': {'categoria': 'cultura', 'nombre': 'Portal Cultura'},
    'C2': {'categoria': 'cultura', 'nombre': 'Música'},
    'C3': {'categoria': 'cultura', 'nombre': 'Cine'},
    'C4': {'categoria': 'cultura', 'nombre': 'Literatura'},
    'C5': {'categoria': 'cultura', 'nombre': 'Museos'},
    'C6': {'categoria': 'cultura', 'nombre': 'Teatro'},
}

# Orden fijo de nodos (para matrices)
NODOS_ORDEN = [
    'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7',
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7',
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
]

# Agrupados por categoría
NODOS_TECH = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7']
NODOS_DEP  = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']
NODOS_CUL  = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']

# =====================================================================
# 2. DEFINICIÓN DE ENLACES (ARISTAS DIRIGIDAS)
# =====================================================================
# Cada tupla (A, B) significa: la página A contiene un enlace hacia B.
#
# Reglas aplicadas:
#   - Cada nodo tiene entre 2 y 5 enlaces de salida.
#   - ~65 % intra-categoría, ~35 % inter-categoría.
#   - Los portales (T1, D1, C1) reciben la mayor cantidad de enlaces.
#   - Hay enlaces cruzados para conectar las tres comunidades.

ENLACES = [
    # ---- Tecnología ----
    ('T1', 'T2'), ('T1', 'T3'), ('T1', 'T5'), ('T1', 'D1'), ('T1', 'C1'),   # T1: 5 salidas (hub cross-category)
    ('T2', 'T1'), ('T2', 'T3'), ('T2', 'T5'),                                 # T2: 3 salidas
    ('T3', 'T1'), ('T3', 'T4'),                                                # T3: 2 salidas
    ('T4', 'T1'), ('T4', 'T5'), ('T4', 'T7'),                                 # T4: 3 salidas
    ('T5', 'T2'), ('T5', 'T6'),                                                # T5: 2 salidas
    ('T6', 'T1'), ('T6', 'T7'), ('T6', 'D7'),                                 # T6: 3 salidas (cross → esports)
    ('T7', 'T3'), ('T7', 'T6'),                                                # T7: 2 salidas

    # ---- Deportes ----
    ('D1', 'D2'), ('D1', 'D3'), ('D1', 'D5'), ('D1', 'T1'),                   # D1: 4 salidas (hub cross → tech)
    ('D2', 'D1'), ('D2', 'D4'), ('D2', 'D6'),                                 # D2: 3 salidas
    ('D3', 'D1'), ('D3', 'D2'),                                                # D3: 2 salidas
    ('D4', 'D1'), ('D4', 'D3'), ('D4', 'C4'),                                 # D4: 3 salidas (cross → cultura)
    ('D5', 'D1'), ('D5', 'D6'), ('D5', 'D7'),                                 # D5: 3 salidas
    ('D6', 'D2'), ('D6', 'D7'),                                                # D6: 2 salidas
    ('D7', 'D5'), ('D7', 'T6'), ('D7', 'C2'),                                 # D7: 3 salidas (cross → tech, cultura)

    # ---- Cultura ----
    ('C1', 'C2'), ('C1', 'C3'), ('C1', 'C5'),                                 # C1: 3 salidas
    ('C2', 'C1'), ('C2', 'C4'), ('C2', 'D2'),                                 # C2: 3 salidas (cross → deportes)
    ('C3', 'C1'), ('C3', 'C6'),                                                # C3: 2 salidas
    ('C4', 'C1'), ('C4', 'C3'), ('C4', 'C5'),                                 # C4: 3 salidas
    ('C5', 'C1'), ('C5', 'C6'), ('C5', 'T3'),                                 # C5: 3 salidas (cross → tech)
    ('C6', 'C3'), ('C6', 'C4'),                                                # C6: 2 salidas
]


def crear_grafo():
    """
    Crea y devuelve el grafo dirigido con los 20 nodos y sus atributos.

    Returns
    -------
    G : nx.DiGraph
        Grafo dirigido con atributos 'categoria' y 'nombre' en cada nodo.
    """
    G = nx.DiGraph()

    # Agregar nodos con atributos
    for nodo, attrs in NODOS_INFO.items():
        G.add_node(nodo, **attrs)

    # Agregar aristas
    G.add_edges_from(ENLACES)

    return G


def obtener_categorias_color():
    """Devuelve un diccionario de colores por categoría."""
    return {
        'tecnologia': '#3498db',  # Azul
        'deportes':   '#2ecc71',  # Verde
        'cultura':    '#e74c3c',  # Rojo
    }


if __name__ == '__main__':
    G = crear_grafo()
    print(f"Nodos: {G.number_of_nodes()}")
    print(f"Aristas: {G.number_of_edges()}")
    print(f"\nEnlaces de salida (out-degree) por nodo:")
    for nodo in NODOS_ORDEN:
        cat = NODOS_INFO[nodo]['categoria']
        nombre = NODOS_INFO[nodo]['nombre']
        print(f"  {nodo} ({nombre:.<25s}) out={G.out_degree(nodo)}, in={G.in_degree(nodo)}  [{cat}]")

