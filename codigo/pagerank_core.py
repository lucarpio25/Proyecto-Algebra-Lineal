"""
pagerank_core.py
================
Tres implementaciones de PageRank para la red de 20 páginas:

1. Implementación propia — método iterativo (Power Method)
2. Solución directa — sistema lineal  (I − αP) r = (1 − α) v
3. Referencia — función nx.pagerank de NetworkX

Todas reciben la misma red, el mismo α y el mismo vector de reinicio v,
de modo que sus resultados puedan compararse directamente.
"""

import numpy as np
import networkx as nx
from red_definicion import NODOS_ORDEN


# =====================================================================
# UTILIDADES
# =====================================================================

def construir_matriz_P(G, nodos=None):
    """
    Construye la matriz de transición P, estocástica por columnas.

    P[i, j] = probabilidad de pasar del nodo j al nodo i.

    Si un nodo j no tiene enlaces de salida (dangling node), su columna
    se llena con 1/n (distribución uniforme), garantizando que la matriz
    siga siendo estocástica.

    Parameters
    ----------
    G : nx.DiGraph
    nodos : list[str], opcional
        Orden de nodos. Por defecto NODOS_ORDEN.

    Returns
    -------
    P : np.ndarray de forma (n, n)
    """
    if nodos is None:
        nodos = NODOS_ORDEN
    n = len(nodos)
    indice = {nodo: i for i, nodo in enumerate(nodos)}
    P = np.zeros((n, n))

    for j, nodo_j in enumerate(nodos):
        sucesores = list(G.successors(nodo_j))
        if len(sucesores) > 0:
            prob = 1.0 / len(sucesores)
            for suc in sucesores:
                i = indice[suc]
                P[i, j] = prob
        else:
            # Dangling node: distribuir uniformemente
            P[:, j] = 1.0 / n

    return P


def vector_reinicio_uniforme(n):
    """Vector de reinicio uniforme: v_i = 1/n para todo i."""
    return np.ones(n) / n


def vector_reinicio_personalizado(preferencia, nodos=None):
    """
    Vector de reinicio personalizado.

    Asigna el 70 % de la probabilidad de reinicio a los nodos de la
    categoría preferida y el 30 % restante se reparte equitativamente
    entre las demás categorías.

    Parameters
    ----------
    preferencia : str
        'tecnologia' o 'deportes'.
    nodos : list[str]
        Orden de los nodos.

    Returns
    -------
    v : np.ndarray de forma (n,)
    """
    if nodos is None:
        nodos = NODOS_ORDEN
    n = len(nodos)
    v = np.zeros(n)

    # Clasificar nodos por categoría según su prefijo
    idx_tech = [i for i, nd in enumerate(nodos) if nd.startswith('T')]
    idx_dep  = [i for i, nd in enumerate(nodos) if nd.startswith('D')]
    idx_cul  = [i for i, nd in enumerate(nodos) if nd.startswith('C')]

    if preferencia == 'tecnologia':
        favoritos = idx_tech
        resto     = idx_dep + idx_cul
    elif preferencia == 'deportes':
        favoritos = idx_dep
        resto     = idx_tech + idx_cul
    else:
        raise ValueError(f"Preferencia no reconocida: {preferencia}")

    # 70 % repartido entre favoritos, 30 % entre el resto
    peso_fav = 0.70 / len(favoritos) if len(favoritos) > 0 else 0
    peso_res = 0.30 / len(resto)     if len(resto) > 0     else 0

    for i in favoritos:
        v[i] = peso_fav
    for i in resto:
        v[i] = peso_res

    return v


# =====================================================================
# 1. IMPLEMENTACIÓN PROPIA — MÉTODO ITERATIVO (POWER METHOD)
# =====================================================================

def pagerank_iterativo(P, alpha=0.85, v=None, tol=1e-10, max_iter=5000):
    """
    Calcula PageRank mediante actualizaciones sucesivas.

    tol representa la tolerancia del error en norma uno.
    Se detiene cuando:
        residuo / (1 - alpha) <= tol

    Devuelve:
        r: aproximación final.
        iteraciones: número de actualizaciones realizadas.
        residuos: residuo de cada aproximación calculada.

    Si alcanza max_iter sin certificar la precisión, lanza un error.

    Se supone que P es estocástica por columnas y que v contiene
    probabilidades no negativas que suman uno.
    """
    if not 0 < alpha < 1:
        raise ValueError("alpha debe estar entre 0 y 1, sin incluirlos.")

    if not np.isfinite(tol) or tol <= 0:
        raise ValueError("tol debe ser positiva y finita.")

    if not isinstance(max_iter, (int, np.integer)) or max_iter < 1:
        raise ValueError("max_iter debe ser un entero positivo.")

    n = P.shape[0]

    if v is None:
        v = vector_reinicio_uniforme(n)

    # Puntuaciones iniciales uniformes.
    r = np.ones(n) / n
    residuos = []

    for k in range(max_iter):
        # Actualizar las puntuaciones.
        r_nuevo = alpha * (P @ r) + (1 - alpha) * v

        # Calcular el residuo de la nueva aproximación.
        residuo = np.linalg.norm(
            r_nuevo - alpha * (P @ r_nuevo) - (1 - alpha) * v,
            ord=1,
        )
        residuos.append(float(residuo))

        # Calcular el límite del error respecto del equilibrio.
        cota_error = residuo / (1 - alpha)

        # Devolver exactamente el vector cuya precisión se comprobó.
        if cota_error <= tol:
            return r_nuevo, k + 1, residuos

        r = r_nuevo

    # No presentar una aproximación sin certificar como convergida.
    raise RuntimeError(
        f"No se certificó la tolerancia {tol:.2e} "
        f"después de {max_iter} iteraciones. "
        f"Última cota de error: {cota_error:.2e}."
    )


# =====================================================================
# 2. SOLUCIÓN DIRECTA — SISTEMA LINEAL
# =====================================================================

def pagerank_sistema_lineal(P, alpha=0.85, v=None):
    """
    Calcula el vector PageRank resolviendo el sistema lineal:

        (I − α P) r = (1 − α) v

    Parameters
    ----------
    P     : np.ndarray  — Matriz de transición (n × n).
    alpha : float        — Damping factor.
    v     : np.ndarray   — Vector de reinicio.

    Returns
    -------
    r : np.ndarray — Vector PageRank (n,).
    """
    n = P.shape[0]
    if v is None:
        v = vector_reinicio_uniforme(n)

    I = np.eye(n)
    A = I - alpha * P
    b = (1 - alpha) * v
    r = np.linalg.solve(A, b)
    return r


# =====================================================================
# 3. REFERENCIA — NetworkX
# =====================================================================

def pagerank_networkx(G, alpha=0.85, personalization=None, nodos=None):
    """
    Calcula PageRank con NetworkX para comparar.

    Parameters
    ----------
    G               : nx.DiGraph
    alpha           : float
    personalization : dict or None — {nodo: peso} para PageRank personalizado.
    nodos           : list[str]   — Orden de los nodos para devolver un array.

    Returns
    -------
    r : np.ndarray — Vector PageRank en el orden de `nodos`.
    """
    if nodos is None:
        nodos = NODOS_ORDEN

    pr = nx.pagerank(G, alpha=alpha, personalization=personalization,
                     tol=1e-12, max_iter=10000)

    return np.array([pr[n] for n in nodos])


def dict_personalizacion_nx(preferencia, nodos=None):
    """
    Crea el diccionario de personalización para nx.pagerank().

    Parameters
    ----------
    preferencia : str — 'tecnologia' o 'deportes'.

    Returns
    -------
    pers : dict  — {nodo: peso}
    """
    if nodos is None:
        nodos = NODOS_ORDEN
    v = vector_reinicio_personalizado(preferencia, nodos)
    return {nodo: v[i] for i, nodo in enumerate(nodos)}


# =====================================================================
# VERIFICACIONES
# =====================================================================

def verificar_resultado(r, P, alpha, v, nombre=""):
    """
    Verifica que un vector PageRank cumple las propiedades esperadas.

    Comprueba:
        1. Suma de componentes ≈ 1
        2. Todas las componentes ≥ 0
        3. Residuo ||r − αPr − (1−α)v||₁ suficientemente pequeño

    Parameters
    ----------
    r      : np.ndarray — Vector PageRank.
    P      : np.ndarray — Matriz de transición.
    alpha  : float
    v      : np.ndarray — Vector de reinicio.
    nombre : str        — Etiqueta para los mensajes.
    """
    if v is None:
        v = vector_reinicio_uniforme(P.shape[0])

    suma = np.sum(r)
    minimo = np.min(r)
    residuo = np.linalg.norm(r - alpha * (P @ r) - (1 - alpha) * v, ord=1)

    print(f"\n--- Verificación: {nombre} ---")
    print(f"  Suma de componentes   : {suma:.12f}  (esperado: 1.0)")
    print(f"  Mínimo componente     : {minimo:.2e}  (esperado: ≥ 0)")
    print(f"  Residuo ||r−αPr−(1−α)v||₁ : {residuo:.2e}")

    ok = True
    if abs(suma - 1.0) > 1e-6:
        print("  ⚠ La suma no es 1.")
        ok = False
    if minimo < -1e-10:
        print("  ⚠ Hay componentes negativas.")
        ok = False
    if residuo > 1e-6:
        print("  ⚠ El residuo es alto.")
        ok = False
    if ok:
        print("  ✓ Todas las verificaciones pasaron.")
    return ok

