"""
ejecutar_experimentos.py
========================
Ejecuta TODOS los experimentos del proyecto PageRank y guarda
los resultados en archivos CSV en la carpeta resultados/.

Experimentos:
    E1. Conteo de enlaces recibidos (in-degree)
    E2. PageRank uniforme (α = 0.85)
    E3. PageRank personalizado — preferencia tecnología
    E4. PageRank personalizado — preferencia deportes
    E5. Efecto de α ∈ {0.50, 0.85, 0.95, 0.99}
    E6. Añadir enlaces y comparar
    E7. Quitar enlaces y comparar
    E8. Crear un dangling node (nodo sin salidas)
"""

import os
import sys
import numpy as np
import pandas as pd
import networkx as nx
import copy

# Asegurar que los imports locales funcionen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from red_definicion import (
    crear_grafo, NODOS_ORDEN, NODOS_INFO,
    NODOS_TECH, NODOS_DEP, NODOS_CUL
)
from pagerank_core import (
    construir_matriz_P,
    vector_reinicio_uniforme,
    vector_reinicio_personalizado,
    pagerank_iterativo,
    pagerank_sistema_lineal,
    pagerank_networkx,
    dict_personalizacion_nx,
    verificar_resultado,
)

# Directorio de resultados
DIR_RESULTADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resultados')
os.makedirs(DIR_RESULTADOS, exist_ok=True)


def guardar_csv(df, nombre):
    """Guarda un DataFrame como CSV."""
    ruta = os.path.join(DIR_RESULTADOS, nombre)
    df.to_csv(ruta, index=True, encoding='utf-8-sig')
    print(f"  → Guardado: {ruta}")


# =====================================================================
# EJEMPLO DE 3 NODOS DEL DOCENTE (verificación previa)
# =====================================================================

def ejemplo_3_nodos():
    """
    Reproduce el ejemplo exacto de 3 nodos del docente (Prof. Oswaldo Velásquez).
    Referencia: Sección 6 del artículo de cátedra 'PageRank y PageRank personalizado'.

    Aristas: 1 → 2, 2 → 1, 2 → 3, 3 → 1, todas de peso 1.
    Matriz de transición:
        P = [
            [0,   1/2, 1],
            [1,   0,   0],
            [0,   1/2, 0]
        ]

    Casos teóricos del artículo:
    1. Reinicio uniforme (α = 1/2, v = [1/3, 1/3, 1/3]^T):
       Solución analítica exacta: r = 1/39 * [15, 14, 10]^T ≈ [0.384615, 0.358974, 0.256410]^T
    2. Reinicio personalizado en nodo 3 (α = 1/2, v = [0, 0, 1]^T):
       Solución analítica exacta: r = 1/13 * [4, 2, 7]^T ≈ [0.307692, 0.153846, 0.538462]^T
    """
    print("=" * 65)
    print("VERIFICACIÓN: EJEMPLO DE 3 NODOS (ARTÍCULO DEL DOCENTE)")
    print("=" * 65)

    nodos3 = ['1', '2', '3']
    G3 = nx.DiGraph()
    G3.add_edges_from([('1', '2'), ('2', '1'), ('2', '3'), ('3', '1')])

    P3 = np.array([
        [0.0, 0.5, 1.0],  # fila 1
        [1.0, 0.0, 0.0],  # fila 2
        [0.0, 0.5, 0.0],  # fila 3
    ])

    alpha = 0.5

    # --- Caso 1: Reinicio Uniforme ---
    print("\n--- Caso 1: Reinicio Uniforme (α = 1/2, v = [1/3, 1/3, 1/3]^T) ---")
    v_uni = np.ones(3) / 3.0
    r_teorico_uni = np.array([15.0, 14.0, 10.0]) / 39.0

    r_iter_uni, iters_uni, _ = pagerank_iterativo(P3, alpha=alpha, v=v_uni, tol=1e-12)
    r_lin_uni = pagerank_sistema_lineal(P3, alpha=alpha, v=v_uni)
    pr_nx_uni = nx.pagerank(G3, alpha=alpha, tol=1e-12)
    r_nx_uni = np.array([pr_nx_uni[nd] for nd in nodos3])

    print("Nodo | Teórico (1/39) | Iterativo | Sistema Lineal | NetworkX")
    for i, nd in enumerate(nodos3):
        print(f"  {nd}  |    {r_teorico_uni[i]:.6f}    |  {r_iter_uni[i]:.6f} |    {r_lin_uni[i]:.6f}    | {r_nx_uni[i]:.6f}")

    dif_teorico_uni = np.linalg.norm(r_iter_uni - r_teorico_uni, ord=1)
    print(f"Error frente a solución teórica exacta (1/39): {dif_teorico_uni:.2e}")
    verificar_resultado(r_iter_uni, P3, alpha, v_uni, "Ejemplo 3 nodos – Uniforme")

    # --- Caso 2: Reinicio Personalizado (v = e3) ---
    print("\n--- Caso 2: Reinicio Personalizado (α = 1/2, v = e3 = [0, 0, 1]^T) ---")
    v_pers = np.array([0.0, 0.0, 1.0])
    r_teorico_pers = np.array([4.0, 2.0, 7.0]) / 13.0

    r_iter_pers, iters_pers, _ = pagerank_iterativo(P3, alpha=alpha, v=v_pers, tol=1e-12)
    r_lin_pers = pagerank_sistema_lineal(P3, alpha=alpha, v=v_pers)
    pr_nx_pers = nx.pagerank(G3, alpha=alpha, personalization={'1': 0.0, '2': 0.0, '3': 1.0}, tol=1e-12)
    r_nx_pers = np.array([pr_nx_pers[nd] for nd in nodos3])

    print("Nodo | Teórico (1/13) | Iterativo | Sistema Lineal | NetworkX")
    for i, nd in enumerate(nodos3):
        print(f"  {nd}  |    {r_teorico_pers[i]:.6f}    |  {r_iter_pers[i]:.6f} |    {r_lin_pers[i]:.6f}    | {r_nx_pers[i]:.6f}")

    dif_teorico_pers = np.linalg.norm(r_iter_pers - r_teorico_pers, ord=1)
    print(f"Error frente a solución teórica exacta (1/13): {dif_teorico_pers:.2e}")
    verificar_resultado(r_iter_pers, P3, alpha, v_pers, "Ejemplo 3 nodos – Personalizado (v=e3)")

    return True


# =====================================================================
# E1. CONTEO DE ENLACES RECIBIDOS (IN-DEGREE)
# =====================================================================

def experimento_E1(G):
    print("\n" + "=" * 65)
    print("E1. CONTEO DE ENLACES RECIBIDOS (IN-DEGREE)")
    print("=" * 65)

    in_deg = {n: G.in_degree(n) for n in NODOS_ORDEN}

    df = pd.DataFrame({
        'Nodo': NODOS_ORDEN,
        'Nombre': [NODOS_INFO[n]['nombre'] for n in NODOS_ORDEN],
        'Categoría': [NODOS_INFO[n]['categoria'] for n in NODOS_ORDEN],
        'In-Degree': [in_deg[n] for n in NODOS_ORDEN],
    }).set_index('Nodo')

    df = df.sort_values('In-Degree', ascending=False)
    print(df.to_string())
    guardar_csv(df, 'E1_in_degree.csv')

    return in_deg


# =====================================================================
# E2. PAGERANK UNIFORME (α = 0.85)
# =====================================================================

def experimento_E2(G, P):
    print("\n" + "=" * 65)
    print("E2. PAGERANK UNIFORME (α = 0.85)")
    print("=" * 65)

    alpha = 0.85
    tolerancia = 1e-10
    n = len(NODOS_ORDEN)
    v = vector_reinicio_uniforme(n)

    # Calcular PageRank por los tres procedimientos.
    r_iter, iters, residuos = pagerank_iterativo(
        P, alpha, v, tol=tolerancia
    )
    r_lin = pagerank_sistema_lineal(P, alpha, v)
    r_nx = pagerank_networkx(G, alpha)

    print(f"\nIteraciones del método propio: {iters}")

    # Comparar las puntuaciones obtenidas.
    dif_iter_lin = np.linalg.norm(r_iter - r_lin, ord=1)
    dif_iter_nx = np.linalg.norm(r_iter - r_nx, ord=1)
    dif_lin_nx = np.linalg.norm(r_lin - r_nx, ord=1)

    print(f"||iterativo − lineal||₁   = {dif_iter_lin:.2e}")
    print(f"||iterativo − NetworkX||₁ = {dif_iter_nx:.2e}")
    print(f"||lineal − NetworkX||₁    = {dif_lin_nx:.2e}")

    # Verificar cada resultado con la misma ecuación y tolerancia.
    metodos = {
        'Iterativo': r_iter,
        'Sistema lineal': r_lin,
        'NetworkX': r_nx,
    }

    comprobaciones = []

    for nombre, r in metodos.items():
        residuo = np.linalg.norm(
            r - alpha * (P @ r) - (1 - alpha) * v,
            ord=1,
        )
        cota_error = residuo / (1 - alpha)

        verificado = verificar_resultado(
            r,
            P,
            alpha,
            v,
            nombre=f"PR uniforme – {nombre}",
            tol=tolerancia,
        )

        comprobaciones.append({
            'Metodo': nombre,
            'Suma': float(np.sum(r)),
            'Minimo': float(np.min(r)),
            'Residuo': float(residuo),
            'Cota_error': float(cota_error),
            'Tolerancia': tolerancia,
            'Diferencia_con_lineal': float(
                np.linalg.norm(r - r_lin, ord=1)
            ),
            'Verificado': verificado,
        })

    # Guardar las comprobaciones en una tabla independiente.
    df_verificaciones = pd.DataFrame(
        comprobaciones
    ).set_index('Metodo')

    guardar_csv(
        df_verificaciones,
        'E2_verificaciones.csv',
    )

    if not all(fila['Verificado'] for fila in comprobaciones):
        raise RuntimeError(
            "Algún procedimiento de E2 no superó la verificación. "
            "Revisar E2_verificaciones.csv."
        )

    # Conservar la tabla de puntuaciones que utilizan los gráficos.
    df = pd.DataFrame({
        'Nodo': NODOS_ORDEN,
        'Nombre': [
            NODOS_INFO[nodo]['nombre']
            for nodo in NODOS_ORDEN
        ],
        'Categoría': [
            NODOS_INFO[nodo]['categoria']
            for nodo in NODOS_ORDEN
        ],
        'PR_Iterativo': r_iter,
        'PR_Lineal': r_lin,
        'PR_NetworkX': r_nx,
    }).set_index('Nodo')

    df = df.sort_values('PR_Iterativo', ascending=False)

    print(f"\nRanking PageRank uniforme (α = {alpha}):")
    print(df.to_string(float_format='%.6f'))

    guardar_csv(df, 'E2_pagerank_uniforme.csv')

    return r_iter, residuos


# =====================================================================
# E3 y E4. PAGERANK PERSONALIZADO
# =====================================================================

def experimento_E3_E4(G, P):
    print("\n" + "=" * 65)
    print("E3–E4. PAGERANK PERSONALIZADO")
    print("=" * 65)

    alpha = 0.85
    resultados = {}

    for preferencia in ['tecnologia', 'deportes']:
        v = vector_reinicio_personalizado(preferencia)
        pers_nx = dict_personalizacion_nx(preferencia)

        r_iter, iters, _ = pagerank_iterativo(P, alpha, v)
        r_nx = pagerank_networkx(G, alpha, personalization=pers_nx)

        dif = np.linalg.norm(r_iter - r_nx, ord=1)
        print(f"\n{'TECNOLOGÍA' if preferencia == 'tecnologia' else 'DEPORTES'}:")
        print(f"  Iteraciones: {iters}")
        print(f"  ||iterativo − NetworkX||₁ = {dif:.2e}")

        verificar_resultado(r_iter, P, alpha, v,
                            f"PR Personalizado ({preferencia})")

        resultados[preferencia] = r_iter

    # Tabla conjunta
    v_uni = vector_reinicio_uniforme(len(NODOS_ORDEN))
    r_uni, _, _ = pagerank_iterativo(P, alpha, v_uni)

    df = pd.DataFrame({
        'Nodo': NODOS_ORDEN,
        'Nombre': [NODOS_INFO[n]['nombre'] for n in NODOS_ORDEN],
        'Categoría': [NODOS_INFO[n]['categoria'] for n in NODOS_ORDEN],
        'PR_Uniforme': r_uni,
        'PR_Tech': resultados['tecnologia'],
        'PR_Deportes': resultados['deportes'],
    }).set_index('Nodo')

    # Agregar rankings
    df['Rank_Uniforme']  = df['PR_Uniforme'].rank(ascending=False).astype(int)
    df['Rank_Tech']      = df['PR_Tech'].rank(ascending=False).astype(int)
    df['Rank_Deportes']  = df['PR_Deportes'].rank(ascending=False).astype(int)

    df = df.sort_values('PR_Uniforme', ascending=False)
    print(f"\nComparación de rankings:")
    print(df.to_string(float_format='%.6f'))
    guardar_csv(df, 'E3_E4_personalizados.csv')

    return resultados


# =====================================================================
# E5. EFECTO DE α EN CONVERGENCIA
# =====================================================================

def experimento_E5(P):
    print("\n" + "=" * 65)
    print("E5. EFECTO DE α EN LA CONVERGENCIA")
    print("=" * 65)

    alphas = [0.50, 0.85, 0.95, 0.99]
    tolerancia = 1e-10

    n = len(NODOS_ORDEN)
    v = vector_reinicio_uniforme(n)

    resultados_alpha = {}
    filas = []

    for alpha in alphas:
        r, iters, residuos = pagerank_iterativo(
            P,
            alpha=alpha,
            v=v,
            tol=tolerancia,
        )

        residuo_final = residuos[-1]
        cota_error = residuo_final / (1 - alpha)

        # Comparación con la solución directa del sistema.
        r_lineal = pagerank_sistema_lineal(P, alpha, v)
        diferencia_lineal = np.linalg.norm(r - r_lineal, ord=1)

        indices_top5 = np.argsort(-r)[:5]
        top5 = [
            (NODOS_ORDEN[i], f"{r[i]:.6f}")
            for i in indices_top5
        ]

        print(f"\nα = {alpha}:")
        print(f"  Iteraciones: {iters}")
        print(f"  Residuo final: {residuo_final:.2e}")
        print(f"  Cota del error: {cota_error:.2e}")
        print(f"  Tolerancia: {tolerancia:.2e}")
        print(f"  Diferencia con solución directa: {diferencia_lineal:.2e}")
        print(f"  Top 5: {[t[0] for t in top5]}")

        verificado = verificar_resultado(
            r,
            P,
            alpha,
            v,
            nombre=f"α = {alpha}",
            tol=tolerancia,
        )

        if not verificado:
            raise RuntimeError(
                f"La verificación falló para alpha = {alpha}."
            )

        resultados_alpha[alpha] = {
            'r': r,
            'iteraciones': iters,
            'residuo_final': residuo_final,
            'cota_error': cota_error,
            'tolerancia': tolerancia,
            'diferencia_lineal': diferencia_lineal,
            'residuos': residuos,
            'top5': top5,
        }

        filas.append({
            'alpha': alpha,
            'iteraciones': iters,
            'residuo_final': residuo_final,
            'cota_error': cota_error,
            'tolerancia': tolerancia,
            'diferencia_lineal': diferencia_lineal,
            'verificado': verificado,
            'top_1': top5[0][0],
            'top_2': top5[1][0],
            'top_3': top5[2][0],
            'top_4': top5[3][0],
            'top_5': top5[4][0],
        })

    df = pd.DataFrame(filas).set_index('alpha')

    print("\nResumen de convergencia por α:")
    print(df.to_string())

    guardar_csv(df, 'E5_convergencia_alpha.csv')

    return resultados_alpha

# =====================================================================
# E6, E7, E8. SENSIBILIDAD A CAMBIOS DE ENLACES
# =====================================================================

def experimento_E6_E7_E8(G_original, P_original):
    print("\n" + "=" * 65)
    print("E6–E8. SENSIBILIDAD A CAMBIOS DE ENLACES")
    print("=" * 65)

    alpha = 0.85
    n = len(NODOS_ORDEN)
    v = vector_reinicio_uniforme(n)

    # Resultado base
    r_base, _, _ = pagerank_iterativo(P_original, alpha, v)

    modificaciones = []

    # ------------------------------------------------------------------
    # E6. AÑADIR ENLACES
    # ------------------------------------------------------------------
    print("\n--- E6: Añadir enlaces ---")
    enlaces_nuevos = [('D3', 'T1'), ('C6', 'D1'), ('T5', 'C1')]

    G_add = G_original.copy()
    G_add.add_edges_from(enlaces_nuevos)
    P_add = construir_matriz_P(G_add)
    r_add, _, _ = pagerank_iterativo(P_add, alpha, v)

    cambio = r_add - r_base
    idx_max_cambio = np.argmax(np.abs(cambio))
    nodo_mas_afectado = NODOS_ORDEN[idx_max_cambio]

    # Top 5 comparado
    top5_base = [NODOS_ORDEN[i] for i in np.argsort(-r_base)[:5]]
    top5_add  = [NODOS_ORDEN[i] for i in np.argsort(-r_add)[:5]]
    cambia_top5 = top5_base != top5_add

    print(f"  Enlaces añadidos: {enlaces_nuevos}")
    print(f"  Nodo más afectado: {nodo_mas_afectado} (cambio: {cambio[idx_max_cambio]:+.6f})")
    print(f"  Top 5 base : {top5_base}")
    print(f"  Top 5 nuevo: {top5_add}")
    print(f"  ¿Cambia top 5? {'Sí' if cambia_top5 else 'No'}")

    modificaciones.append({
        'Modificación': f'Añadir {enlaces_nuevos}',
        'Nodo_más_afectado': nodo_mas_afectado,
        'Cambio_puntuación': f"{cambio[idx_max_cambio]:+.6f}",
        'Cambia_top5': 'Sí' if cambia_top5 else 'No',
        'Top5_antes': str(top5_base),
        'Top5_después': str(top5_add),
    })

    # ------------------------------------------------------------------
    # E7. QUITAR ENLACES
    # ------------------------------------------------------------------
    print("\n--- E7: Quitar enlaces ---")
    enlaces_quitar = [('T2', 'T1'), ('D3', 'D1'), ('C3', 'C1')]

    G_rm = G_original.copy()
    G_rm.remove_edges_from(enlaces_quitar)
    P_rm = construir_matriz_P(G_rm)
    r_rm, _, _ = pagerank_iterativo(P_rm, alpha, v)

    cambio = r_rm - r_base
    idx_max_cambio = np.argmax(np.abs(cambio))
    nodo_mas_afectado = NODOS_ORDEN[idx_max_cambio]

    top5_rm = [NODOS_ORDEN[i] for i in np.argsort(-r_rm)[:5]]
    cambia_top5 = top5_base != top5_rm

    print(f"  Enlaces quitados: {enlaces_quitar}")
    print(f"  Nodo más afectado: {nodo_mas_afectado} (cambio: {cambio[idx_max_cambio]:+.6f})")
    print(f"  Top 5 base : {top5_base}")
    print(f"  Top 5 nuevo: {top5_rm}")
    print(f"  ¿Cambia top 5? {'Sí' if cambia_top5 else 'No'}")

    modificaciones.append({
        'Modificación': f'Quitar {enlaces_quitar}',
        'Nodo_más_afectado': nodo_mas_afectado,
        'Cambio_puntuación': f"{cambio[idx_max_cambio]:+.6f}",
        'Cambia_top5': 'Sí' if cambia_top5 else 'No',
        'Top5_antes': str(top5_base),
        'Top5_después': str(top5_rm),
    })

    # ------------------------------------------------------------------
    # E8. DANGLING NODE — quitar TODAS las salidas de D6
    # ------------------------------------------------------------------
    print("\n--- E8: Dangling node (D6 sin salidas) ---")

    G_dang = G_original.copy()
    salidas_D6 = list(G_dang.successors('D6'))
    print(f"  Enlaces eliminados de D6: {[('D6', s) for s in salidas_D6]}")
    G_dang.remove_edges_from([('D6', s) for s in salidas_D6])

    P_dang = construir_matriz_P(G_dang)
    r_dang, _, _ = pagerank_iterativo(P_dang, alpha, v)

    # Verificar que la columna de D6 en P es uniforme (dangling node)
    idx_D6 = NODOS_ORDEN.index('D6')
    print(f"  Columna D6 de P (debe ser 1/20 = 0.05 en cada fila):")
    print(f"    Min: {P_dang[:, idx_D6].min():.4f}, Max: {P_dang[:, idx_D6].max():.4f}")

    cambio = r_dang - r_base
    idx_max_cambio = np.argmax(np.abs(cambio))
    nodo_mas_afectado = NODOS_ORDEN[idx_max_cambio]

    top5_dang = [NODOS_ORDEN[i] for i in np.argsort(-r_dang)[:5]]
    cambia_top5 = top5_base != top5_dang

    print(f"  Nodo más afectado: {nodo_mas_afectado} (cambio: {cambio[idx_max_cambio]:+.6f})")
    print(f"  Top 5 base     : {top5_base}")
    print(f"  Top 5 dangling : {top5_dang}")
    print(f"  ¿Cambia top 5? {'Sí' if cambia_top5 else 'No'}")

    verificar_resultado(r_dang, P_dang, alpha, v, "Dangling node D6")

    modificaciones.append({
        'Modificación': 'D6 sin enlaces de salida (dangling)',
        'Nodo_más_afectado': nodo_mas_afectado,
        'Cambio_puntuación': f"{cambio[idx_max_cambio]:+.6f}",
        'Cambia_top5': 'Sí' if cambia_top5 else 'No',
        'Top5_antes': str(top5_base),
        'Top5_después': str(top5_dang),
    })

    # Tabla de todas las modificaciones
    df = pd.DataFrame(modificaciones)
    print(f"\nResumen de sensibilidad:")
    print(df.to_string(index=False))
    guardar_csv(df.set_index('Modificación'), 'E6_E7_E8_sensibilidad.csv')

    # Tabla detallada de puntuaciones
    df_detalle = pd.DataFrame({
        'Nodo': NODOS_ORDEN,
        'Nombre': [NODOS_INFO[n]['nombre'] for n in NODOS_ORDEN],
        'PR_Base': r_base,
        'PR_Add': r_add,
        'PR_Remove': r_rm,
        'PR_Dangling': r_dang,
        'Cambio_Add': r_add - r_base,
        'Cambio_Remove': r_rm - r_base,
        'Cambio_Dangling': r_dang - r_base,
    }).set_index('Nodo')

    guardar_csv(df_detalle, 'E6_E7_E8_detalle.csv')

    return {
        'base': r_base,
        'add': r_add,
        'remove': r_rm,
        'dangling': r_dang,
        'G_dangling': G_dang,
    }


# =====================================================================
# TABLA RESUMEN: TOP 5 DE TODOS LOS RANKINGS
# =====================================================================

def tabla_resumen_top5(in_deg, r_uniforme, resultados_pers):
    print("\n" + "=" * 65)
    print("TABLA RESUMEN — TOP 5 DE CADA RANKING")
    print("=" * 65)

    filas = []
    for pos in range(5):
        # In-degree
        sorted_indeg = sorted(in_deg.items(), key=lambda x: -x[1])
        nd_indeg = sorted_indeg[pos][0]

        # PR Uniforme
        idx_uni = np.argsort(-r_uniforme)
        nd_uni = NODOS_ORDEN[idx_uni[pos]]

        # PR Tech
        r_tech = resultados_pers['tecnologia']
        idx_tech = np.argsort(-r_tech)
        nd_tech = NODOS_ORDEN[idx_tech[pos]]

        # PR Deportes
        r_dep = resultados_pers['deportes']
        idx_dep = np.argsort(-r_dep)
        nd_dep = NODOS_ORDEN[idx_dep[pos]]

        filas.append({
            'Posición': pos + 1,
            'In-Degree': f"{nd_indeg} ({sorted_indeg[pos][1]})",
            'PR Uniforme': f"{nd_uni} ({r_uniforme[idx_uni[pos]]:.4f})",
            'PR Tech': f"{nd_tech} ({r_tech[idx_tech[pos]]:.4f})",
            'PR Deportes': f"{nd_dep} ({r_dep[idx_dep[pos]]:.4f})",
        })

    df = pd.DataFrame(filas).set_index('Posición')
    print(df.to_string())
    guardar_csv(df, 'tabla_resumen_top5.csv')


# =====================================================================
# MAIN — EJECUTAR TODO
# =====================================================================

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     PROYECTO PAGERANK — ÁLGEBRA LINEAL                     ║")
    print("║     Análisis de relevancia de páginas web                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Verificar con ejemplo de 3 nodos
    ejemplo_3_nodos()

    # Crear la red
    G = crear_grafo()
    P = construir_matriz_P(G)

    print(f"\nRed creada: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")
    print(f"Columnas de P suman 1: {np.allclose(P.sum(axis=0), 1.0)}")

    # Ejecutar todos los experimentos
    in_deg = experimento_E1(G)
    r_uniforme, residuos_base = experimento_E2(G, P)
    resultados_pers = experimento_E3_E4(G, P)
    resultados_alpha = experimento_E5(P)
    resultados_sens = experimento_E6_E7_E8(G, P)

    # Tabla resumen
    tabla_resumen_top5(in_deg, r_uniforme, resultados_pers)

    print("\n" + "=" * 65)
    print("✓ TODOS LOS EXPERIMENTOS COMPLETADOS")
    print(f"  Resultados guardados en: {os.path.abspath(DIR_RESULTADOS)}")
    print("=" * 65)

    return {
        'G': G, 'P': P,
        'in_deg': in_deg,
        'r_uniforme': r_uniforme,
        'residuos_base': residuos_base,
        'resultados_pers': resultados_pers,
        'resultados_alpha': resultados_alpha,
        'resultados_sens': resultados_sens,
    }


if __name__ == '__main__':
    resultados = main()

