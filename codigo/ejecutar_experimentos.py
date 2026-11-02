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
    tolerancia = 1e-10
    resultados = {}
    comprobaciones = []

    for preferencia in ['tecnologia', 'deportes']:
        v = vector_reinicio_personalizado(preferencia)
        pers_nx = dict_personalizacion_nx(preferencia)

        # Calcular con los mismos parámetros por tres procedimientos.
        r_iter, iters, _ = pagerank_iterativo(
            P, alpha, v, tol=tolerancia
        )
        r_lin = pagerank_sistema_lineal(P, alpha, v)
        r_nx = pagerank_networkx(
            G, alpha, personalization=pers_nx
        )

        print(f"\nPreferencia: {preferencia}")
        print(f"  Iteraciones del método propio: {iters}")
        print(
            "  Diferencia iterativo–lineal: "
            f"{np.linalg.norm(r_iter - r_lin, ord=1):.2e}"
        )
        print(
            "  Diferencia iterativo–NetworkX: "
            f"{np.linalg.norm(r_iter - r_nx, ord=1):.2e}"
        )

        metodos = {
            'Iterativo': r_iter,
            'Sistema lineal': r_lin,
            'NetworkX': r_nx,
        }

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
                nombre=f"{preferencia} – {nombre}",
                tol=tolerancia,
            )

            comprobaciones.append({
                'Preferencia': preferencia,
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

        resultados[preferencia] = r_iter

    # Guardar las seis comprobaciones: tres por preferencia.
    df_verificaciones = pd.DataFrame(
        comprobaciones
    ).set_index(['Preferencia', 'Metodo'])

    guardar_csv(
        df_verificaciones,
        'E3_E4_verificaciones.csv',
    )

    if not all(fila['Verificado'] for fila in comprobaciones):
        raise RuntimeError(
            "Algún procedimiento de E3–E4 no superó la verificación. "
            "Revisar E3_E4_verificaciones.csv."
        )

    # Calcular la referencia uniforme para comparar rankings.
    v_uni = vector_reinicio_uniforme(len(NODOS_ORDEN))
    r_uni, _, _ = pagerank_iterativo(
        P, alpha, v_uni, tol=tolerancia
    )

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
        'PR_Uniforme': r_uni,
        'PR_Tech': resultados['tecnologia'],
        'PR_Deportes': resultados['deportes'],
    }).set_index('Nodo')

    # Las puntuaciones iguales comparten posición.
    for puntuacion, ranking in [
        ('PR_Uniforme', 'Rank_Uniforme'),
        ('PR_Tech', 'Rank_Tech'),
        ('PR_Deportes', 'Rank_Deportes'),
    ]:
        df[ranking] = df[puntuacion].rank(
            ascending=False,
            method='min',
        ).astype(int)

    df = df.sort_values('PR_Uniforme', ascending=False)

    print("\nComparación de rankings:")
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
    tolerancia = 1e-10
    n = len(NODOS_ORDEN)
    v = vector_reinicio_uniforme(n)

    # Cada modificación parte de la red original.
    enlaces_nuevos = [
        ('D3', 'T1'),
        ('C6', 'D1'),
        ('T5', 'C1'),
    ]
    enlaces_quitar = [
        ('T2', 'T1'),
        ('D3', 'D1'),
        ('C3', 'C1'),
    ]

    G_add = G_original.copy()
    G_add.add_edges_from(enlaces_nuevos)

    G_rm = G_original.copy()
    G_rm.remove_edges_from(enlaces_quitar)

    G_dang = G_original.copy()
    salidas_D6 = [
        ('D6', destino)
        for destino in G_dang.successors('D6')
    ]
    G_dang.remove_edges_from(salidas_D6)

    escenarios = {
        'base': ('Red original', G_original),
        'add': (f'Añadir {enlaces_nuevos}', G_add),
        'remove': (f'Quitar {enlaces_quitar}', G_rm),
        'dangling': ('D6 sin enlaces de salida (dangling)', G_dang),
    }

    resultados = {}
    comprobaciones = []

    for clave, (descripcion, grafo) in escenarios.items():
        print(f"\n--- {descripcion} ---")

        P = construir_matriz_P(grafo)

        if clave == 'base':
            if not np.allclose(
                P, P_original, rtol=0, atol=1e-14
            ):
                raise ValueError(
                    "P_original no coincide con la matriz de la red base."
                )

        if clave == 'dangling':
            idx_D6 = NODOS_ORDEN.index('D6')

            if not np.allclose(
                P[:, idx_D6], 1.0 / n, rtol=0, atol=1e-14
            ):
                raise ValueError(
                    "La columna de D6 no es uniforme."
                )

            print(f"  Enlaces eliminados de D6: {salidas_D6}")
            print(f"  Redistribución por página: {1.0 / n:.4f}")

        # Calcular por los tres procedimientos.
        r_iter, iters, _ = pagerank_iterativo(
            P, alpha, v, tol=tolerancia
        )
        r_lin = pagerank_sistema_lineal(P, alpha, v)
        r_nx = pagerank_networkx(grafo, alpha)

        print(f"  Iteraciones del método propio: {iters}")

        metodos = {
            'Iterativo': r_iter,
            'Sistema lineal': r_lin,
            'NetworkX': r_nx,
        }

        for nombre, r in metodos.items():
            residuo = np.linalg.norm(
                r - alpha * (P @ r) - (1 - alpha) * v,
                ord=1,
            )

            verificado = verificar_resultado(
                r,
                P,
                alpha,
                v,
                nombre=f"{clave} – {nombre}",
                tol=tolerancia,
            )

            comprobaciones.append({
                'Escenario': clave,
                'Metodo': nombre,
                'Suma': float(np.sum(r)),
                'Minimo': float(np.min(r)),
                'Residuo': float(residuo),
                'Cota_error': float(residuo / (1 - alpha)),
                'Tolerancia': tolerancia,
                'Diferencia_con_lineal': float(
                    np.linalg.norm(r - r_lin, ord=1)
                ),
                'Verificado': verificado,
            })

        resultados[clave] = r_iter

    df_verificaciones = pd.DataFrame(
        comprobaciones
    ).set_index(['Escenario', 'Metodo'])

    guardar_csv(
        df_verificaciones,
        'E6_E7_E8_verificaciones.csv',
    )

    if not all(fila['Verificado'] for fila in comprobaciones):
        raise RuntimeError(
            "Algún resultado de E6–E8 no superó la verificación. "
            "Revisar E6_E7_E8_verificaciones.csv."
        )

    # Comparar cada modificación con la red original.
    r_base = resultados['base']
    top5_base = [
        NODOS_ORDEN[i]
        for i in np.argsort(-r_base)[:5]
    ]

    modificaciones = []

    for clave in ['add', 'remove', 'dangling']:
        r = resultados[clave]
        cambio = r - r_base
        idx_max = np.argmax(np.abs(cambio))

        top5 = [
            NODOS_ORDEN[i]
            for i in np.argsort(-r)[:5]
        ]

        cambia_orden = top5 != top5_base
        cambia_composicion = set(top5) != set(top5_base)

        modificaciones.append({
            'Modificación': escenarios[clave][0],
            'Nodo_más_afectado': NODOS_ORDEN[idx_max],
            'Cambio_puntuación': float(cambio[idx_max]),
            'Cambia_top5': 'Sí' if cambia_orden else 'No',
            'Cambia_composicion_top5': (
                'Sí' if cambia_composicion else 'No'
            ),
            'Top5_antes': str(top5_base),
            'Top5_después': str(top5),
        })

    df = pd.DataFrame(modificaciones)

    print("\nResumen de sensibilidad:")
    print(df.to_string(index=False))

    guardar_csv(
        df.set_index('Modificación'),
        'E6_E7_E8_sensibilidad.csv',
    )

    # Mantener las columnas utilizadas por los gráficos.
    df_detalle = pd.DataFrame({
        'Nodo': NODOS_ORDEN,
        'Nombre': [
            NODOS_INFO[nodo]['nombre']
            for nodo in NODOS_ORDEN
        ],
        'PR_Base': r_base,
        'PR_Add': resultados['add'],
        'PR_Remove': resultados['remove'],
        'PR_Dangling': resultados['dangling'],
        'Cambio_Add': resultados['add'] - r_base,
        'Cambio_Remove': resultados['remove'] - r_base,
        'Cambio_Dangling': resultados['dangling'] - r_base,
    }).set_index('Nodo')

    guardar_csv(df_detalle, 'E6_E7_E8_detalle.csv')

    resultados['G_dangling'] = G_dang

    return resultados

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

