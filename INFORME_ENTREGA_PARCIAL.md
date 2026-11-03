# INFORME DE ENTREGA PARCIAL

## Proyecto: Análisis de Relevancia de Páginas Web mediante PageRank y PageRank Personalizado

---

**Curso:** Álgebra Lineal (UP 26-2)  
**Institución:** Universidad del Pacífico  
**Docente:** Oswaldo Jose Velasquez Castañon
**Etiqueta de entrega (Git Tag):** `avance-parcial`  
**Fecha:** Noviembre de 2026

---

### Integrantes del Equipo y Distribución de Responsabilidades

| Nombre Completo                    |  Código  | Responsabilidad Principal en la Entrega Parcial                                                                                                                             |
| ---------------------------------- | :------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sofía Catherine Briceño Rosado** | [Código] | Fundamentación matemática, deducción de las tres formulaciones, demostración de existencia, unicidad y convergencia analítica.                                              |
| **Luciana Carpio Cárdenas**        | 325728 | Delimitación del problema, formulación de la pregunta de investigación, alcance, gobernanza del repositorio y documentación de procedencia de la red.                       |
| **Manuel Sialer**                  | [Código] | Diseño topológico de la red de 20 nodos, implementación computacional en Python, ejecución de la batería experimental (E1–E8) y generación de figuras.                      |
| **Marianela Usnayo Gutierrez**     | [Código] | Verificaciones numéricas (residuos, estocasticidad, sumas unitarias), contraste inter-algorítmico (Iterativo vs. Lineal vs. NetworkX) y estructuración del guion del video. |

---

## 1. Definición Actualizada del Problema, Objetivo y Alcance

### 1.1. Contexto y Planteamiento del Problema

En el ecosistema de la World Wide Web, los hipervínculos estructuran un grafo dirigido masivo donde las páginas actúan como nodos y los enlaces como aristas orientadas. La aproximación elemental para determinar la centralidad o importancia de un nodo consiste en el cómputo de su grado de entrada (_in-degree_):

$$
\text{deg}_{\text{in}}(i) = \sum_{j=1}^{n} A_{ij}
$$

Sin embargo, contar enlaces no considera las puntuaciones de las páginas de origen ni cómo estas las reparten entre sus enlaces de salida. Además, el conteo no incorpora preferencias temáticas del usuario.

PageRank considera estas relaciones para calcular la relevancia de cada página dentro de la red. Su variante personalizada permite modificar las probabilidades de reinicio para favorecer determinados temas.

Estas puntuaciones describen la relevancia según la estructura de enlaces y las preferencias definidas. No garantizan la calidad o veracidad del contenido ni eliminan la posibilidad de manipulación mediante enlaces artificiales.

### 1.2. Pregunta de Investigación

> _¿De qué manera varía la jerarquización de relevancia en una red dirigida de 20 páginas web al contrastar el conteo de enlaces entrantes (in-degree), PageRank uniforme y PageRank personalizado, y qué sensibilidad exhiben las puntuaciones, el Top 5 y la tasa de convergencia ante alteraciones en el factor de amortiguamiento α y modificaciones en la topología de la red?_

### 1.3. Objetivo General

Implementar, verificar y analizar computacional y matemáticamente los algoritmos de PageRank uniforme y personalizado sobre una red simulada de 20 páginas web con tres categorías temáticas, contrastando rigurosamente los resultados contra soluciones algebraicas directas y bibliotecas científicas de referencia, cuantificando la sensibilidad del modelo ante variaciones del parámetro $\alpha \in \{0.50, 0.85, 0.95, 0.99\}$ y perturbaciones estructurales en los enlaces.

### 1.4. Objetivos Específicos

1. Formular analíticamente la matriz de transición estocástica $P$ y formalizar la regla estocástica para nodos sin enlaces de salida (_dangling nodes_).
2. Deducir y demostrar la equivalencia entre las tres formulaciones del problema: punto fijo iterativo, sistema de ecuaciones lineales no homogéneo $(I - \alpha P)r = (1-\alpha)v$ y vector propio dominante de la matriz Google $G$.
3. Construir una implementación propia en Python basada en actualizaciones iterativas, comprobarla con el ejemplo de tres nodos del docente y comparar sus resultados con la solución numérica directa del sistema lineal y con `networkx.pagerank`.
4. Diseñar y ejecutar ocho experimentos numéricos (E1 a E8) para medir el impacto de la personalización temática, la tasa de contracción y el fenómeno de inversión de rangos (_rank reversal_).
5. Cuantificar el residuo $\lVert r - \alpha P r - (1-\alpha)v \rVert_1$ como certificado riguroso de precisión numérica.

### 1.5. Alcance y Delimitación

- **Dominio experimental:** Se diseñó una red simulada y reproducible de 20 nodos y 56 aristas dirigidas, dividida en Tecnología (7 nodos), Deportes (7 nodos) y Cultura (6 nodos).
- **Parámetros evaluados:** Factores de amortiguamiento $\alpha \in \{0.50, 0.85, 0.95, 0.99\}$; vectores de reinicio uniforme ($v_{\text{uni}}$) y personalizados ($v_{\text{tech}}$, $v_{\text{dep}}$) con una concentración del 70 % en la categoría de interés.
- **Límites:** El estudio evalúa exclusivamente la autoridad derivada de la estructura de enlaces topológica y las preferencias de reinicio; no analiza contenido textual, semántico ni veracidad intrínseca de las páginas.

---

## 2. Fundamentación y Desarrollo Matemático Riguroso

### 2.1. De la Red a la Matriz de Transición Estocástica $P$

Sea un grafo dirigido $G = (V, E)$ con conjunto de vértices $V = \{1, 2, \dots, n\}$ y conjunto de aristas dirigidas $E \subseteq V \times V$. Para cada nodo $j \in V$, definimos su conjunto de enlaces salientes como $\text{Out}(j) = \{i \in V : (j \to i) \in E\}$ y su grado de salida como $d_j^{\text{out}} = |\text{Out}(j)|$.

La probabilidad condicional de que un navegante aleatorio ubicado en el nodo $j$ elija transitar hacia el nodo $i$ siguiendo un enlace saliente viene dada por los coeficientes de la matriz de adyacencia normalizada $P \in \mathbb{R}^{n \times n}$:

$$
P_{ij} = \begin{cases} \frac{1}{d_j^{\text{out}}} & \text{si } (j \to i) \in E \\ 0 & \text{en otro caso} \end{cases}
$$

#### Tratamiento Riguroso de Nodos sin Salidas (_Dangling Nodes_)

Si un nodo j no tiene enlaces de salida, su columna en la matriz quedaría formada por ceros. En ese caso, la matriz dejaría de ser estocástica por columnas: al aplicar P a una distribución que asigne probabilidad positiva a ese nodo, la suma de las componentes sería menor que uno. Por ello, es necesario establecer una regla que redistribuya esa probabilidad.

Para preservar la conservación de la probabilidad, se define formalmente la corrección estocástica: cuando el navegante arriba a un sumidero, salta con idéntica probabilidad hacia cualquier nodo de la red:

$$
P_{ij} = \frac{1}{n} \quad \forall i \in \{1, \dots, n\} \quad \text{si } d_j^{\text{out}} = 0
$$

Con esta regla, $P$ es estrictamente **estocástica por columnas**:

$$
\sum_{i=1}^{n} P_{ij} = 1 \quad \forall j \in \{1, \dots, n\}, \quad P_{ij} \ge 0
$$

---

### 2.2. Parámetro de Amortiguamiento $\alpha$ y Vector de Reinicio $v$

Se incorpora un reinicio que permite continuar la navegación sin depender exclusivamente de los enlaces existentes. Si todas las componentes del vector de reinicio v son positivas, la matriz Google es positiva y la cadena de Markov es irreducible y aperiódica. Esta condición se cumple en las tres distribuciones de reinicio utilizadas en la red de 20 páginas.

- Con probabilidad $\alpha \in (0, 1)$, el usuario sigue uno de los hipervínculos disponibles en la página actual.
- Con probabilidad complementaria $(1 - \alpha)$, el usuario abandona la secuencia de navegación y se teletransporta hacia una página elegida según una distribución de probabilidad dada por el **vector de reinicio** $v \in \mathbb{R}^n$, donde:

$$
v_i \ge 0, \quad \sum_{i=1}^{n} v_i = 1
$$

- **PageRank Uniforme:** $v = \mathbf{1}/n$, donde cada nodo recibe probabilidad de reinicio $1/n$.
- **PageRank Personalizado:** $v$ concentra peso probabilístico sobre un subconjunto de nodos semilla $S \subset V$:
  

$$
v_i = \begin{cases} \frac{\beta}{|S|} & \text{si } i \in S \\ \frac{1 - \beta}{n - |S|} & \text{si } i \notin S \end{cases}
$$

  En nuestro proyecto, adoptamos $\beta = 0.70$ para privilegiar de forma contundente la categoría de interés.

---

### 2.3. Tres Formulaciones Algebraicas Equivalentes

#### Formulación 1: Ecuación de Punto Fijo (Forma Iterativa)

La distribución estacionaria de probabilidad $r \in \mathbb{R}^n$ satisface el balance de flujo invariante:

$$
r = \alpha P r + (1 - \alpha) v
$$

Sujeto a las restricciones de probabilidad:

$$
r \ge \mathbf{0}, \quad \lVert r \rVert_1 = \sum_{i=1}^{n} r_i = 1
$$

#### Formulación 2: Sistema de Ecuaciones Lineales No Homogéneo

Reordenando los términos algebraicamente:

$$
r - \alpha P r = (1 - \alpha) v \implies (I - \alpha P) r = (1 - \alpha) v
$$

Donde $I \in \mathbb{R}^{n \times n}$ es la matriz identidad.

**Teorema de Existencia y Unicidad de la Solución:**

1. Como la matriz $P$ es estocástica por columnas, su norma matricial inducida por la norma 1 es $\lVert P \rVert_1 = \max_{j} \sum_{i=1}^n |P_{ij}| = 1$.
2. Por las propiedades del radio espectral $\rho(A) \le \lVert A \rVert$, se tiene que $\rho(P) \le 1$.
3. Al multiplicar por el escalar $\alpha \in [0, 1)$, se cumple estrictamente:
   

$$
\rho(\alpha P) = \alpha \rho(P) \le \alpha < 1
$$

4. En virtud del teorema de las series de Neumann, si el radio espectral de una matriz $M$ es estrictamente menor que 1, la matriz $(I - M)$ es invertible y su inversa se expresa como la serie convergente:
   

$$
(I - \alpha P)^{-1} = \sum_{m=0}^{\infty} (\alpha P)^m
$$

5. Por consiguiente, la matriz $(I - \alpha P)$ es estrictamente no singular, garantizando la **existencia y unicidad** de la solución:
   

$$
r^{\ast} = (1 - \alpha) (I - \alpha P)^{-1} v
$$

#### Formulación 3: Problema de Vectores y Valores Propios (Matriz Google $G$)

Observando que $\mathbf{1}^T r = \sum_{i=1}^n r_i = 1$, podemos reescribir $(1 - \alpha) v$ como $(1 - \alpha) v (\mathbf{1}^T r)$. Sustituyendo en la ecuación de punto fijo:

$$
r = \alpha P r + (1 - \alpha) v \mathbf{1}^T r = \left( \alpha P + (1 - \alpha) v \mathbf{1}^T \right) r
$$

Definiendo la **Matriz Google** $G \in \mathbb{R}^{n \times n}$:

$$
G = \alpha P + (1 - \alpha) v \mathbf{1}^T
$$

La ecuación se reduce a:

$$
G r = 1 \cdot r
$$

El vector PageRank es un vector propio por la derecha de la matriz Google G, asociado al valor propio uno y normalizado para que sus componentes sumen uno.

Cuando todas las componentes de v son positivas, todas las entradas de G también son positivas. Por el teorema de Perron-Frobenius, el valor propio uno es simple, los demás valores propios tienen módulo menor que uno y el vector PageRank tiene componentes estrictamente positivas.

Si v contiene ceros, la positividad de G no está garantizada. Sin embargo, la existencia y unicidad de PageRank siguen siendo válidas para una matriz P estocástica por columnas y un parámetro alfa entre cero y uno, como demuestra la formulación mediante el sistema lineal.

---

### 2.4. Demostración de Convergencia del Método Iterativo (_Power Method_)

El cómputo sucesivo se define mediante la relación de recurrencia:

$$
r^{(k+1)} = \alpha P r^{(k)} + (1 - \alpha) v, \quad k = 0, 1, 2, \dots
$$

Partiendo de una inicialización uniforme $r^{(0)} = \frac{1}{n} \mathbf{1}$.

#### Contracción y Cota de Error $\alpha^k$:

Restando el punto fijo exacto $r^{\ast} = \alpha P r^{\ast} + (1 - \alpha) v$ de la relación iterativa:

$$
r^{(k+1)} - r^{\ast} = \alpha P (r^{(k)} - r^{\ast})
$$

Tomando la norma 1 a ambos lados y empleando la submultiplicatividad:

$$
\lVert r^{(k+1)} - r^{\ast} \rVert_1 = \lVert \alpha P (r^{(k)} - r^{\ast}) \rVert_1 \le \alpha \lVert P \rVert_1 \lVert r^{(k)} - r^{\ast} \rVert_1
$$

Como $\lVert P \rVert_1 = 1$:

$$
\lVert r^{(k+1)} - r^{\ast} \rVert_1 \le \alpha \lVert r^{(k)} - r^{\ast} \rVert_1
$$

Aplicando inducción matemática desde el paso inicial $k=0$:

$$
\lVert r^{(k)} - r^{\ast} \rVert_1 \le \alpha^k \lVert r^{(0)} - r^{\ast} \rVert_1
$$

Dado que $0 \le \alpha < 1$, se deduce directamente que $\lim_{k \to \infty} \alpha^k = 0$, lo que demuestra la **convergencia lineal global independiente del vector inicial**.

#### Criterio de Parada y Certificado de Error mediante el Residuo:

En la práctica computacional no se dispone de $r^{\ast}$. Se evalúa el vector residual:

$$
\delta^{(k)} = r^{(k)} - \left( \alpha P r^{(k)} + (1 - \alpha) v \right) = (I - \alpha P) r^{(k)} - (1 - \alpha) v
$$

Observando que $(I - \alpha P)(r^{(k)} - r^{\ast}) = \delta^{(k)}$:

$$
r^{(k)} - r^{\ast} = (I - \alpha P)^{-1} \delta^{(k)}
$$

Aplicando normas:

$$
\lVert r^{(k)} - r^{\ast} \rVert_1 \le \lVert (I - \alpha P)^{-1} \rVert_1 \lVert \delta^{(k)} \rVert_1
$$

Expandiendo mediante serie de Neumann:

$$
\lVert (I - \alpha P)^{-1} \rVert_1 = \left\lVert  \sum_{m=0}^\infty (\alpha P)^m \right \rVert_1 \le \sum_{m=0}^\infty \alpha^m \lVert P \rVert_1^m = \sum_{m=0}^\infty \alpha^m = \frac{1}{1 - \alpha}
$$

Por consiguiente, se obtiene el **certificado formal de error**:

$$
\lVert r^{(k)} - r^{\ast} \rVert_1 \le \frac{1}{1 - \alpha} \lVert \delta^{(k)} \rVert_1
$$

Este resultado garantiza que controlar el residuo $\lVert \delta^{(k)} \rVert_1 < \tau (1 - \alpha)$ certifica que el error absoluto frente a la solución matemática exacta no supera la tolerancia deseada $\tau$.

---

## 3. Desarrollo Práctico e Implementación Computacional

### 3.1. Validación preliminar con el ejemplo de tres nodos del docente

Para comprobar los procedimientos de cálculo, se utiliza el ejemplo de la sección 6 del artículo del docente. La red contiene las aristas 1 → 2, 2 → 1, 2 → 3 y 3 → 1, todas de peso uno, con alfa = 0.50.

Su matriz de transición es:

$$
P_3 =
\begin{pmatrix}
0 & 1/2 & 1 \\
1 & 0 & 0 \\
0 & 1/2 & 0
\end{pmatrix}.
$$

#### Caso 1: reinicio uniforme

Con el vector de reinicio uniforme:

$$
v = \frac{1}{3}
\begin{pmatrix}
1\\
1\\
1
\end{pmatrix},
$$

la solución exacta es:

$$
r = \frac{1}{39}
\begin{pmatrix}
15\\
14\\
10
\end{pmatrix}.
$$

#### Caso 2: reinicio personalizado en el nodo 3

Con el vector de reinicio:

$$
v =
\begin{pmatrix}
0\\
0\\
1
\end{pmatrix},
$$

la solución exacta es:

$$
r = \frac{1}{13}
\begin{pmatrix}
4\\
2\\
7
\end{pmatrix}.
$$

Las puntuaciones de referencia son:

| Nodo | Reinicio uniforme | Reinicio personalizado en el nodo 3 |
|:---:|---:|---:|
| 1 | 0.384615 | 0.307692 |
| 2 | 0.358974 | 0.153846 |
| 3 | 0.256410 | 0.538462 |

En ambos casos, las componentes son no negativas, suman uno y satisfacen la ecuación de PageRank:

$$
r = 0.50P_3r + 0.50v.
$$

El script `ejecutar_experimentos.py` calcula ambos casos mediante el método iterativo, la solución directa del sistema lineal y NetworkX. Los resultados se contrastan con las soluciones exactas anteriores.

Las verificaciones numéricas incluyen la diferencia respecto de la solución exacta, la suma de componentes, la no negatividad y el residuo. Se utiliza el criterio de parada basado en el certificado de error: residuo dividido entre 1 − alfa menor o igual que la tolerancia establecida.

### 3.2. Topología de la red simulada de 20 nodos

Se diseñó un grafo dirigido de 20 nodos y 56 aristas. Cada nodo representa una página web ficticia y cada arista representa un enlace desde una página de origen hacia una página de destino.

La red se organiza en tres categorías temáticas:

| Categoría | Prefijo | Nodos | Cantidad de nodos | Total de enlaces de salida | Promedio de enlaces de salida |
|---|:---:|---|:---:|:---:|:---:|
| Tecnología | T | T1 a T7 | 7 | 20 | 2.86 |
| Deportes | D | D1 a D7 | 7 | 20 | 2.86 |
| Cultura | C | C1 a C6 | 6 | 16 | 2.67 |
| **Total** | | | **20** | **56** | **2.80** |

Los nodos T1, D1 y C1 representan portales de sus respectivas categorías. También se incluyen páginas especializadas y conexiones entre categorías, como T6 → D7, D4 → C4 y C5 → T3.

#### Reglas de construcción

1. **Enlaces de salida:** cada nodo de la red base tiene entre 2 y 5 enlaces de salida. Todos los enlaces tienen el mismo peso.

2. **Conexiones dentro de cada categoría:** 47 de los 56 enlaces conectan páginas de la misma categoría, equivalentes aproximadamente al 83.9 % del total.

3. **Conexiones entre categorías:** 9 de los 56 enlaces conectan páginas de categorías diferentes, equivalentes aproximadamente al 16.1 % del total. Estas conexiones permiten que la navegación pase de un tema a otro.

4. **Ausencia de autoenlaces:** ninguna página de la red base contiene un enlace hacia sí misma.

5. **Páginas sin enlaces de salida:** la red base no contiene nodos sin salidas. En el experimento E8 se eliminan todos los enlaces de salida de D6 para estudiar este caso. Su columna en la matriz de transición se reemplaza por una distribución uniforme de 1/20 en cada componente.

#### Procedencia de los datos

Los nodos y enlaces fueron diseñados manualmente con fines académicos. La red permite estudiar diferencias entre el conteo de enlaces recibidos, PageRank uniforme y PageRank personalizado.

Las páginas son ficticias y las conexiones no proceden de una extracción de sitios web reales. La definición completa de los nodos y enlaces está disponible en `codigo/red_definicion.py`, y las reglas de construcción se documentan en `datos/reglas_red.md`.

## 4. Resultados Preliminares y Comprobaciones Numéricas

Se ejecutó la batería completa de experimentos del E1 al E8 mediante el script `ejecutar_experimentos.py`. Todos los archivos de salida se encuentran archivados en `resultados/` y las representaciones gráficas en `figuras/`.

### 4.1. Experimento E1: Conteo de Enlaces Entrantes (_In-Degree_)

```text
Posición 1-3 (Empate): T1 (5 enlaces), D1 (5 enlaces), C1 (5 enlaces)
Posición 4-5 (Empate): T3 (4 enlaces), D2 (4 enlaces)
Posición 6-10: C4 (3), C3 (3), T6 (3), D7 (3), T5 (3)
```

**Diagnóstico crítico:** La métrica puramente estructural genera un empate plano entre los tres portales ($T_1, D_1, C_1$) y es incapaz de discriminar qué nodo ostenta mayor autoridad real.

---

### 4.2. Experimento E2: PageRank Uniforme ($\alpha = 0.85$) y Desempate Teórico

Al incorporar la formulación matricial completa:

| Ranking |   Nodo    | Nombre             | Categoría  | PageRank Uniforme | Enlaces recibidos |
| :-----: | :-------: | :----------------- | :--------- | :---------------: | :--------------------: |
|  **1**  | **$C_1$** | Portal Cultura     | Cultura    |   **0.091400**    |         5         |
|  **2**  | **$T_1$** | Portal Tecnología  | Tecnología |   **0.082846**    |         5         |
|  **3**  | **$D_1$** | Portal Deportes    | Deportes   |   **0.069240**    |         5         |
|  **4**  | **$C_3$** | Cine               | Cultura    |   **0.068638**    |         3         |
|  **5**  | **$D_2$** | Fútbol             | Deportes   |   **0.063060**    |         4         |
|    6    |   $T_3$   | Reviews de Gadgets | Tecnología |     0.059617      |         4         |
|    7    |   $T_6$   | Programación       | Tecnología |     0.052272      |         3         |
|    8    |   $C_6$   | Teatro             | Cultura    |     0.050087      |         2         |

#### Justificación del desempate

1. **C1 ocupa el primer lugar:** Aunque C1, T1 y D1 reciben cinco enlaces cada uno, PageRank les asigna puntuaciones diferentes. Esto ocurre porque cada enlace aporta una cantidad que depende de la puntuación de la página de origen y de cuántos enlaces de salida tiene. Para calcular la puntuación de C1, se suman los aportes de T1, C2, C3, C4 y C5, multiplicados por alfa, y se añade el reinicio. En esta red, el resultado es aproximadamente 0.0914, superior al de T1 y D1.

2. **C3 alcanza el cuarto lugar:** C3 recibe tres enlaces y está empatado con otras páginas en el conteo de enlaces recibidos. Sin embargo, alcanza una puntuación aproximada de 0.0686 en PageRank uniforme. Entre sus páginas de origen se encuentra C1, que tiene la mayor puntuación de la red. Este enlace contribuye al resultado de C3, junto con los demás enlaces recibidos y el reinicio.

---

### 4.3. Experimentos E3 y E4: PageRank Personalizado (Tecnología vs. Deportes)

Se introdujeron dos vectores de reinicio sesgados con el 70 % de la masa de probabilidad asignada a su respectiva categoría:

$$
\text{Top 5 Comparativo entre Variantes:}
$$

| Posición | _In-Degree_ | PageRank Uniforme | PR Personalizado (Tecnología) | PR Personalizado (Deportes) |
| :------: | :---------: | :---------------: | :---------------------------: | :-------------------------: |
|  **1**   |  $T_1$ (5)  |  $C_1$ (0.0914)   |      **$T_1$ (0.1174)**       |     **$D_1$ (0.1015)**      |
|  **2**   |  $D_1$ (5)  |  $T_1$ (0.0828)   |      **$T_3$ (0.0842)**       |     **$D_2$ (0.0936)**      |
|  **3**   |  $C_1$ (5)  |  $D_1$ (0.0692)   |      **$T_6$ (0.0779)**       |       $C_1$ (0.0708)        |
|  **4**   |  $T_3$ (4)  |  $C_3$ (0.0686)   |        $C_1$ (0.0722)         |       $T_1$ (0.0698)        |
|  **5**   |  $D_2$ (4)  |  $D_2$ (0.0631)   |      **$T_5$ (0.0674)**       |     **$D_7$ (0.0678)**      |

- **Sesgo Tecnológico:** Cuatro de los primeros cinco lugares corresponden a la categoría tecnológica ($T_1, T_3, T_6, T_5$). El portal $C_1$ se sostiene en el 4.º puesto debido al fuerte enlace entrante que le otorga $T_1$.
- **Sesgo Deportivo:** Los nodos $D_1$ y $D_2$ concentran casi el 20 % del rango total de la red. Asimismo, $D_7$ (Esports) emerge en el Top 5 gracias a su conectividad híbrida.

---

### 4.4. Experimento E5: convergencia y sensibilidad al parámetro alfa

Se evaluó el método iterativo con alfa = 0.50, 0.85, 0.95 y 0.99, manteniendo la misma red, el reinicio uniforme y la distribución inicial uniforme.

Para comparar las ejecuciones con una misma precisión, se estableció una tolerancia de error en norma uno de 10⁻¹⁰. El algoritmo se detuvo cuando:

$$
\frac{\rho(x)}{1-\alpha}\leq 10^{-10},
$$

donde el residuo se calcula como:

$$
\rho(x)=\|x-\alpha Px-(1-\alpha)v\|_1.
$$

Los resultados fueron:

| Alfa | Iteraciones | Residuo final aproximado | Cota del error aproximada | Primeros cinco lugares |
|:---:|:---:|:---:|:---:|---|
| 0.50 | 24 | 3.15 × 10⁻¹¹ | 6.31 × 10⁻¹¹ | T1, C1, D1, D2, T3 |
| 0.85 | 70 | 1.32 × 10⁻¹¹ | 8.78 × 10⁻¹¹ | C1, T1, D1, C3, D2 |
| 0.95 | 116 | 4.24 × 10⁻¹² | 8.49 × 10⁻¹¹ | C1, T1, C3, D1, D2 |
| 0.99 | 157 | 9.18 × 10⁻¹³ | 9.18 × 10⁻¹¹ | C1, C3, T1, D1, C6 |

Las cuatro ejecuciones cumplieron la tolerancia establecida. Las cotas se calcularon con los valores completos del residuo; en la tabla se muestran redondeadas.

#### Interpretación de las iteraciones

En esta red, el número de iteraciones aumentó al incrementar alfa. Entre alfa = 0.50 y alfa = 0.99, pasó de 24 a 157, lo que representa un aumento aproximado del 554.2 %.

Este comportamiento es compatible con la contracción: cuando alfa se acerca a uno, la reducción garantizada del error por paso es más lenta. Además, para certificar una misma tolerancia, el criterio exige un residuo menor al aumentar alfa.

La cota teórica garantiza convergencia, pero no determina exactamente el número de iteraciones observado.

#### Cambios en el ranking

Con alfa = 0.50, T1 ocupa el primer lugar. Para los otros valores evaluados, C1 pasa a la primera posición. Con alfa = 0.99, C3 asciende al segundo lugar y C6 entra en los primeros cinco.

Al aumentar alfa, se da mayor peso al seguimiento de enlaces y menor peso a los reinicios. Esto puede modificar las puntuaciones y el orden de las páginas.

Los resultados corresponden a esta red y no demuestran que un valor de alfa sea universalmente mejor que otro.

#### Comprobación con la solución directa

Las aproximaciones iterativas también se compararon con la solución obtenida mediante `numpy.linalg.solve`.

En las cuatro ejecuciones, la diferencia en norma uno entre ambos procedimientos fue menor que 10⁻¹⁰. Esta comparación complementa las comprobaciones del residuo, la suma de componentes y la no negatividad.

### 4.5. Experimentos E6, E7 y E8: sensibilidad ante cambios en los enlaces

Se estudió cómo cambian las puntuaciones y el ranking al modificar conexiones de la red. En los tres experimentos se utilizó alfa = 0.85 y reinicio uniforme.

Cada modificación se aplicó por separado sobre la red original. Después de añadir o eliminar enlaces, se reconstruyó la matriz de transición para que cada columna continuara sumando uno.

Los cambios de puntuación se calcularon restando el resultado de la red original al de la red modificada.

| Experimento | Modificación | Nodo con mayor cambio absoluto | Cambio de puntuación | Primeros cinco lugares |
|---|---|:---:|---:|---|
| E6 | Añadir D3 → T1, C6 → D1 y T5 → C1 | D1 | +0.011661 | C1, T1, D1, D2, C3 |
| E7 | Eliminar T2 → T1, D3 → D1 y C3 → C1 | C6 | +0.036652 | C6, C3, T1, D2, C4 |
| E8 | Eliminar D6 → D2 y D6 → D7, dejando D6 sin salidas | D2 | −0.015135 | C1, T1, C3, D1, T3 |

Las cifras corresponden a los experimentos repetidos con el criterio de parada basado en el certificado de error. En la red original y en los tres escenarios modificados, el método iterativo, la solución directa y NetworkX superaron las verificaciones de suma de componentes, no negatividad y cota de error menor o igual que 10⁻¹⁰.

Las comprobaciones se encuentran en `resultados/E6_E7_E8_verificaciones.csv`.

#### E6: adición de enlaces

Al añadir los tres enlaces, D1 presenta el mayor cambio absoluto de puntuación, con un aumento aproximado de 0.011661.

Los integrantes de los primeros cinco lugares se mantienen, pero cambia su orden: D2 pasa del quinto al cuarto puesto y C3 baja del cuarto al quinto.

Este caso permite distinguir entre un cambio de posiciones y un cambio en las páginas que componen los primeros cinco lugares.

#### E7: eliminación de enlaces

Al eliminar los tres enlaces seleccionados, C6 presenta el mayor cambio absoluto, con un aumento aproximado de 0.036652, y pasa al primer lugar.

Eliminar un enlace también modifica la proporción de puntuación que la página de origen reparte entre sus destinos restantes. Por ello, los efectos pueden extenderse a páginas que no participan directamente en los enlaces eliminados.

#### E8: página sin enlaces de salida

Se eliminaron las dos salidas de D6: D6 → D2 y D6 → D7. Su columna en la matriz de transición se reemplazó por una distribución uniforme de 1/20 = 0.05 para cada página.

Antes de la modificación, D6 repartía por igual su contribución de seguimiento de enlaces entre D2 y D7. Después, esa contribución se distribuye entre las 20 páginas.

D2 presenta una disminución aproximada de 0.015135 y sale de los primeros cinco lugares, mientras que T3 ingresa. También cambia el orden de C3 y D1.

#### Interpretación general

Los experimentos muestran que modificar enlaces puede cambiar tanto las puntuaciones como las posiciones del ranking. El efecto depende de las páginas involucradas y de sus conexiones con el resto de la red.

Estos resultados corresponden a los cambios específicos evaluados. No permiten afirmar que añadir un enlace siempre mejore la posición de una página ni que eliminarlo perjudique a todas las páginas relacionadas.

## 5. Guion del video final (10 minutos)

El video tendrá una duración aproximada de 10 minutos, con una tolerancia de un minuto por exceso o defecto. Este tiempo incluye la identificación inicial y las referencias finales.

Todos los integrantes explicarán una parte sustantiva del proyecto. Se utilizarán ejemplos, tablas y gráficos legibles para conectar los conceptos matemáticos con los resultados.

| Intervalo | Bloque | Contenido y recursos visuales | Responsable |
|---|---|---|---|
| 0:00–1:00 | Introducción y pregunta | Presentar el título, integrantes, problema, pregunta, objetivo y alcance. Explicar por qué contar enlaces puede producir una clasificación distinta de PageRank. Apoyo: diapositiva inicial y ejemplo sencillo. | Luciana Carpio |
| 1:00–2:00 | Red y matriz de transición | Explicar cómo los enlaces se convierten en probabilidades, por qué las columnas de P suman uno y cómo se tratan las páginas sin salidas. Introducir alfa y el vector de reinicio v. Apoyo: red de tres nodos y su matriz. | Sofía Briceño |
| 2:00–3:00 | Tres formulaciones | Relacionar la ecuación de equilibrio, el sistema lineal y el vector propio de la matriz Google asociado al valor propio uno. Explicar brevemente por qué la solución existe y es única. Apoyo: fórmulas conectadas paso a paso. | Sofía Briceño |
| 3:00–4:00 | Convergencia y precisión | Explicar las actualizaciones sucesivas y la contracción. Distinguir residuo y error, y presentar el certificado: error menor o igual que residuo dividido entre 1 − alfa. Explicar el criterio de parada. Apoyo: esquema de iteraciones y ejemplo numérico. | Sofía Briceño |
| 4:00–5:30 | Verificación de resultados | Mostrar el ejemplo de tres nodos del docente y comparar el método iterativo, la solución directa y NetworkX. Presentar suma de componentes, no negatividad, residuo y certificado de error. Apoyo: tabla breve de comprobaciones. | Marianela Usnayo |
| 5:30–6:45 | Rankings y personalización | Comparar el conteo de enlaces, PageRank uniforme y las preferencias por tecnología y deportes. Explicar el reparto del 70 % de reinicio entre las páginas favoritas y del 30 % entre las restantes. Apoyo: tabla de primeros cinco lugares y gráficos de la red. | Manuel Sialer |
| 6:45–8:00 | Cambios de alfa y enlaces | Mostrar cómo cambian las iteraciones y el ranking con alfa = 0.50, 0.85, 0.95 y 0.99. Resumir los experimentos de adición y eliminación de enlaces y el caso de una página sin salidas. Apoyo: gráficos de convergencia y tabla de sensibilidad. | Manuel Sialer |
| 8:00–9:00 | Interpretación | Explicar las diferencias observadas entre clasificaciones. Distinguir cambios de puntuación, cambios de posición y cambios en la composición de los primeros cinco lugares. Apoyo: resultados seleccionados de los experimentos. | Marianela Usnayo |
| 9:00–10:00 | Conclusiones y cierre | Resumir los hallazgos y las limitaciones de trabajar con una red simulada. Aclarar que PageRank mide relevancia según el modelo, no calidad o veracidad del contenido. Mostrar referencias principales y enlace al repositorio. | Luciana Carpio |

Las tablas y figuras se regeneraron después de corregir el criterio de parada y repetir los experimentos. Antes de grabar, se comprobará que las cifras mostradas en el video coincidan con las publicadas en el informe y el repositorio.

Las demostraciones completas estarán disponibles en el informe. En el video se presentarán sus pasos esenciales, acompañados de ejemplos que permitan entender su función dentro del proyecto.

## 6. Registro de contribuciones individuales

La siguiente tabla registra los aportes de cada integrante y señala los archivos donde pueden revisarse. Los resultados publicados corresponden a la ejecución realizada después de corregir el criterio de parada y repetir los experimentos.

| Integrante | Contribuciones | Evidencias en el repositorio |
|---|---|---|
| **Sofía Catherine Briceño Rosado** | Desarrollo de las tres formulaciones de PageRank: punto fijo, sistema lineal y vector propio. Justificación de existencia y unicidad mediante la serie de Neumann. Desarrollo de la contracción, la cota de error y el certificado basado en el residuo. | Sección 2 del informe y fundamentos matemáticos del `README.md`. |
| **Luciana Carpio Cárdenas** | Planteamiento del problema, pregunta de investigación, objetivo y alcance. Organización del repositorio y revisión de la documentación. Documentación de las reglas de construcción de la red junto con Manuel. | `README.md`, sección 1 del informe y `datos/reglas_red.md`. |
| **Manuel Sialer** | Construcción de la red de 20 nodos. Programación de la matriz de transición y los procedimientos de cálculo. Implementación y ejecución de los experimentos E1–E8. Exportación de tablas y generación de gráficos. | `codigo/red_definicion.py`, `codigo/pagerank_core.py`, `codigo/ejecutar_experimentos.py`, `codigo/generar_visualizaciones.py`, `resultados/` y `figuras/`. |
| **Marianela Usnayo Gutierrez** | Revisión del ejemplo de tres nodos y de las comprobaciones numéricas. Comparación entre el método iterativo, la solución directa y NetworkX. Planificación del video y distribución de tiempos e intervenciones. | Procedimientos de verificación en `codigo/`, tablas en `resultados/` y sección 5 del informe. |

### Actividades compartidas

- Revisar que las fórmulas, el código, las tablas y los gráficos sean coherentes.
- Actualizar los resultados después de corregir el criterio de parada.
- Comprobar la ejecución del proyecto siguiendo las instrucciones del README.
- Interpretar los resultados y formular las conclusiones y limitaciones.
- Participar en el video y comprender el razonamiento general del proyecto.
- Prepararse para responder preguntas sobre los conceptos, procedimientos y resultados.

Antes de cada entrega, el registro se actualizará con los aportes efectivamente realizados. Las responsabilidades pendientes no se presentarán como tareas completadas.

## 7. Plan de Trabajo y Cronograma hacia la Entrega Final

El plan de trabajo restante cubre las semanas 13 y 14 de acuerdo con el calendario académico:

| Semana  |   Días    | Actividad Planificada                                                                           |      Responsable      | Entregable Esperado                                   |
| :-----: | :-------: | ----------------------------------------------------------------------------------------------- | :-------------------: | ----------------------------------------------------- |
| **S13** | Lun – Mié | Grabación individual de los bloques de audio y video según el guion estructurado.               | Todos los integrantes | Archivos de audio y tomas de pantalla limpias.        |
| **S13** | Jue – Sáb | Edición y ensamble audiovisual del video de 10 minutos (verificación de duración 9–11 min).     |   Marianela Usnayo    | Primer corte del video en plataforma (YouTube/Drive). |
| **S13** |    Dom    | Revisión grupal del video y comprobación de legibilidad de fórmulas y audio.                    |    Todo el equipo     | Acta de retroalimentación interna.                    |
| **S14** | Lun – Mar | Incorporación de la retroalimentación docente de la Entrega Parcial en el repositorio.          |    Sofía y Luciana    | Actualización de documentación y README.              |
| **S14** | Mié – Jue | Simulacro interno de la Ronda de Preguntas Individual (ensayo de las 6 preguntas clave).        |    Todo el equipo     | Dominio de respuestas a variaciones teóricas.         |
| **S14** |    Vie    | Verificación integral de reproducibilidad desde cero en equipos independientes.                 |  Marianela y Manuel   | Confirmación de ejecución limpia de scripts.          |
| **S14** |    Sáb    | Generación del tag de Git `entrega-final`, subida del enlace del video y entrega en Blackboard. |    Luciana Carpio     | Entrega formal registrada en Blackboard.              |

---

## 8. Declaración de Uso de Inteligencia Artificial

En estricto cumplimiento del numeral 9 de las indicaciones del curso:

- **Herramientas empleadas:** Antigravity (Google DeepMind) con modelos Claude Opus 4.6 y Gemini Flash.
- **ChatGPT:** apoyo en la revisión de la coherencia entre el informe y el código, para identificar inconsistencias y proponer correcciones puntuales en la documentación. 
- **Finalidad:** Apoyo en la automatización de la sintaxis de scripts en Python (estructuración de bucles de graficación con Matplotlib), formato de tablas en Markdown y corrección de estilo de la documentación.
- **Procedimientos de verificación:** Todos los procedimientos matemáticos fueron verificados analíticamente a mano y validados computacionalmente contra bibliotecas estándar (`numpy.linalg.solve`, `networkx.pagerank`). Las comprobaciones numéricas verifican que las puntuaciones sumen uno dentro de la tolerancia, que no presenten componentes negativas fuera del margen de redondeo y que el certificado de error no supere la tolerancia establecida. Cada integrante del equipo comprende y asume la responsabilidad intelectual y académica total del contenido aquí presentado.

---

## 9. Referencias Bibliográficas (Formato IEEE)

```text
[1] L. Page, S. Brin, R. Motwani y T. Winograd, "The PageRank Citation Ranking: Bringing Order to the Web", Stanford InfoLab, Technical Report 1999-66, 1999. [En línea]. Disponible en: https://ilpubs.stanford.edu/422/
[2] A. N. Langville y C. D. Meyer, Google’s PageRank and Beyond: The Science of Search Engine Rankings. Princeton, NJ, USA: Princeton University Press, 2006.
[3] D. F. Gleich, "PageRank Beyond the Web", SIAM Review, vol. 57, no. 3, pp. 321–363, 2015. DOI: 10.1137/140976649.
[4] S.-W. Son, C. Christensen, P. Grassberger y M. Paczuski, "PageRank and rank-reversal dependence on the damping factor", Physical Review E, vol. 86, no. 6, p. 066104, 2012. DOI: 10.1103/PhysRevE.86.066104.
[5] P. Boldi, M. Santini y S. Vigna, "PageRank: Functional Dependencies", ACM Transactions on Information Systems, vol. 27, no. 4, pp. 1–23, 2009. DOI: 10.1145/1629096.1629097.
[6] G. Strang, Introduction to Linear Algebra, 5.ª ed. Wellesley, MA, USA: Wellesley-Cambridge Press, 2016.
[7] NetworkX Developers, "pagerank — NetworkX documentation", [En línea]. Disponible en: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html
```
