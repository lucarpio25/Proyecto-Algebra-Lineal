# Análisis de Relevancia de Páginas Web mediante PageRank y PageRank Personalizado

---

**Curso:** Álgebra Lineal (UP 26-2)  
**Institución:** Universidad del Pacífico  
**Docente:** Oswaldo Jose Velasquez Castañon  
**Versión evaluada (Git Tag):** `avance-parcial` (Entrega Parcial) / `entrega-final` (Entrega Final)  
**Enlace al video explicativo (10 min):** *[Próximamente disponible en Blackboard]*

---

## Integrantes del Equipo

| Nombre Completo | Rol Principal en el Proyecto |
|---|---|
| **Sofía Catherine Briceño Rosado** | Fundamentación matemática, deducción analítica de formulaciones y demostración de convergencia. |
| **Luciana Carpio Cárdenas** | Planteamiento del problema, delimitación del alcance, mantenimiento del repositorio y documentación de la red. |
| **Manuel Sialer** | Diseño de la red de 20 nodos, implementación computacional, ejecución de experimentos y análisis de sensibilidad. |
| **Marianela Usnayo Gutierrez** | Control de calidad, verificaciones numéricas, comparación inter-algorítmica y edición audiovisual del video. |

---

## 1. Planteamiento del Problema, Objetivo y Alcance

### 1.1. Contexto y Problema

En la World Wide Web, las páginas y sus hipervínculos conforman un grafo dirigido. La aproximación elemental para medir la relevancia de una página consiste en contar cuántos enlaces recibe (*in-degree*). No obstante, esta medida presenta limitaciones críticas:

1. **Ponderación uniforme ingenua:** Asume que todos los votos entrantes tienen idéntica autoridad, ignorando que un hipervínculo proveniente de un portal de alto prestigio debe conferir mayor credibilidad que enlaces de sitios periféricos.
2. **Carencia de personalización temática:** Un ranking global único no contempla los intereses específicos del usuario (por ejemplo, alguien que navega buscando contenidos de tecnología frente a uno interesado en deportes).

El algoritmo **PageRank** resuelve estas deficiencias modelando la navegación como una **cadena de Markov ergódica**, donde la importancia de una página se retroalimenta iterativamente de la relevancia de las páginas que la enlazan, ponderada inversamente por el número de enlaces de salida de estas. Asimismo, su variante **PageRank Personalizado** (*Personalized PageRank* - PPR) permite sesgar el vector de reinicio para canalizar la relevancia hacia categorías temáticas de interés sin alterar la topología de la red.

### 1.2. Pregunta de Investigación

> *¿Cómo cambia la clasificación de relevancia de una red de páginas web al comparar el número de enlaces recibidos, PageRank uniforme y PageRank personalizado, y qué sensibilidad presenta ante cambios en las conexiones y en el parámetro de seguimiento de enlaces?*

### 1.3. Objetivo General

Implementar, verificar y analizar computacional y matemáticamente los algoritmos de PageRank uniforme y personalizado en una red dirigida y simulada de 20 páginas web divididas en tres categorías temáticas, contrastando rigurosamente los resultados contra soluciones algebraicas directas y bibliotecas científicas de referencia, cuantificando la sensibilidad del modelo ante variaciones del parámetro $\alpha \in \{0.50, 0.85, 0.95, 0.99\}$ y perturbaciones en los enlaces.

### 1.4. Alcance y Delimitación

- **Red experimental:** Grafo dirigido de 20 nodos y 56 aristas, estructurado en tres categorías: Tecnología (7 nodos), Deportes (7 nodos) y Cultura (6 nodos).
- **Parámetros:** Factor de amortiguamiento $\alpha \in \{0.50, 0.85, 0.95, 0.99\}$ y vectores de reinicio uniforme y con 70 % de peso en categorías seleccionadas.
- **Límites:** El estudio evalúa exclusivamente la autoridad derivada de la estructura de enlaces y las preferencias de reinicio; no analiza contenido textual, semántica ni veracidad de las páginas.

---

## 2. Fundamentos Matemáticos

### 2.1. Construcción de la Matriz de Transición Estocástica $P$

Sea una red representada por un grafo dirigido $G = (V, E)$ de $n$ vértices. Para cada nodo $j$ con conjunto de enlaces salientes $\text{Out}(j)$ y grado saliente $d_j^{\text{out}} = |\text{Out}(j)|$:

$$
P_{ij} = \begin{cases} \dfrac{1}{d_j^{\text{out}}} & \text{si } (j \to i) \in E \\ 0 & \text{en otro caso} \end{cases}
$$

#### Tratamiento de Nodos sin Salidas (*Dangling Nodes*)

Si una página no tiene enlaces salientes ($d_j^{\text{out}} = 0$), su columna sería nula, lo que provocaría que la suma de probabilidades decaiga a cero. Para mantener la propiedad estocástica, se asume que un navegante que llega a un sumidero salta con igual probabilidad hacia cualquier página de la red:

$$
P_{ij} = \frac{1}{n} \quad \forall i \in \{1, \dots, n\} \quad \text{si } d_j^{\text{out}} = 0
$$

De este modo, $P \in \mathbb{R}^{n \times n}$ es una matriz estocástica por columnas:

$$
\sum_{i=1}^{n} P_{ij} = 1 \quad \forall j \in \{1, \dots, n\}
$$

---

### 2.2. Parámetro de Amortiguamiento $\alpha$ y Vector de Reinicio $v$

Para evitar trampas de ciclo cerrado (*spider traps*) y componentes desconectadas, se incorpora el modelo de teletransportación:

- Con probabilidad $\alpha \in (0, 1)$, el navegante sigue un enlace saliente.
- Con probabilidad $(1 - \alpha)$, salta al azar según la distribución de un vector de reinicio $v \in \mathbb{R}^n$, con $v_i \ge 0$ y $\sum v_i = 1$.
- **Uniforme:** $v = \frac{1}{n}\mathbf{1}$.
- **Personalizado:** $v$ concentra probabilidad (por ejemplo, 70 %) en un subconjunto de nodos temáticos.

---

### 2.3. Tres Formulaciones Algebraicas Equivalentes

#### 1. Formulación de Punto Fijo (Forma Iterativa)

La distribución estacionaria $r \in \mathbb{R}^n$ satisface el balance de flujo:

$$
r = \alpha P r + (1 - \alpha) v, \quad r \ge \mathbf{0}, \quad \lVert r \rVert_1 = 1
$$

#### 2. Formulación de Sistema de Ecuaciones Lineales

Reordenando los términos algebraicamente:

$$
(I - \alpha P) r = (1 - \alpha) v
$$

**Teorema de Existencia y Unicidad:**

Como la matriz $P$ es estocástica por columnas, su norma de matriz inducida cumple $\lVert P \rVert_1 = 1$ y su radio espectral satisface $\rho(P) \le 1$. Al ser $\alpha \in [0, 1)$, se cumple estrictamente:

$$
\rho(\alpha P) = \alpha \rho(P) \le \alpha < 1
$$

Por el teorema de las series de Neumann, la matriz $(I - \alpha P)$ es invertible y su inversa se expresa como la serie geométrica convergente:

$$
(I - \alpha P)^{-1} = \sum_{m=0}^{\infty} (\alpha P)^m
$$

La serie converge absolutamente y la matriz no es singular. Por lo tanto, la solución **existe y es única**:

$$
r^{\ast} = (1 - \alpha) (I - \alpha P)^{-1} v
$$

#### 3. Formulación de Vector Propio (Matriz Google $G$)

Dado que $\mathbf{1}^T r = 1$, expresamos $(1 - \alpha) v = (1 - \alpha) v \mathbf{1}^T r$. Al sustituir en la ecuación de punto fijo:

$$
r = \left( \alpha P + (1 - \alpha) v \mathbf{1}^T \right) r = G r
$$

Donde $G = \alpha P + (1 - \alpha) v \mathbf{1}^T$ es la **Matriz Google**. Así, $r$ es el vector propio dominante de $G$ asociado al valor propio $\lambda = 1$.

Por el **Teorema de Perron-Frobenius**, al ser $G$ positiva y primitiva, $\lambda_1 = 1$ es un valor propio simple y estrictamente mayor en módulo que cualquier otro valor propio ($|\lambda_j| < 1$ para $j \ge 2$), garantizando un vector propio estacionario con todas sus entradas estrictamente positivas ($r_i > 0$).

---

### 2.4. Convergencia del Método Iterativo (*Power Method*)

El cómputo sucesivo se define por la relación de recurrencia:

$$
r^{(k+1)} = \alpha P r^{(k)} + (1 - \alpha) v
$$

#### Cota de Error $\alpha^k$:

Restando el punto fijo exacto $r^{\ast} = \alpha P r^{\ast} + (1 - \alpha) v$:

$$
r^{(k+1)} - r^{\ast} = \alpha P (r^{(k)} - r^{\ast})
$$

Tomando la norma 1:

$$
\lVert r^{(k+1)} - r^{\ast} \rVert_1 \le \alpha \lVert P \rVert_1 \lVert r^{(k)} - r^{\ast} \rVert_1 = \alpha \lVert r^{(k)} - r^{\ast} \rVert_1
$$

Aplicando inducción matemática desde el paso $k = 0$:

$$
\lVert r^{(k+1)} - r^{\ast} \rVert_1 \le \alpha^k \lVert r^{(0)} - r^{\ast} \rVert_1
$$

Dado que $0 \le \alpha < 1$, se cumple $\lim_{k \to \infty} \alpha^k = 0$, lo que demuestra la **convergencia lineal global**. El número de iteraciones necesarias escala como:

$$
k \approx \frac{\log(\tau)}{\log(\alpha)}
$$

#### Certificado de Error a través del Residuo:

Evaluando el vector residual $\delta^{(k)} = (I - \alpha P) r^{(k)} - (1 - \alpha) v$:

$$
r^{(k)} - r^{\ast} = (I - \alpha P)^{-1} \delta^{(k)}
$$

Aplicando normas:

$$
\lVert r^{(k)} - r^{\ast} \rVert_1 \le \lVert (I - \alpha P)^{-1} \rVert_1 \lVert \delta^{(k)} \rVert_1 \le \frac{1}{1 - \alpha} \lVert \delta^{(k)} \rVert_1
$$

Para $\alpha = 0.85$, se tiene $\frac{1}{1-\alpha} \approx 6.67$. Un residuo medido menor que $10^{-11}$ certifica matemáticamente que la distancia a la solución exacta es inferior a $10^{-10}$.

---

## 3. Organización del Repositorio

El repositorio en GitHub presenta una estructura limpia, modular y reproducible:

```text
├── README.md                      # Documentación completa del proyecto (este archivo)
├── requirements.txt               # Dependencias de Python requeridas
├── .gitignore                     # Exclusión de entornos virtuales, cachés y borradores
├── codigo/                        # Código fuente modular en Python
│   ├── red_definicion.py          # Definición formal del grafo (20 nodos, categorías)
│   ├── pagerank_core.py           # Algoritmos: Power Method, Sistema Lineal, NetworkX
│   ├── ejecutar_experimentos.py   # Suite de experimentos E1 a E8 y guardado de datos
│   └── generar_visualizaciones.py # Generación de figuras científicas en alta resolución
├── datos/
│   └── reglas_red.md              # Documentación de reglas y procedencia de la red
├── resultados/                    # Tablas y matrices de resultados en formato CSV
│   ├── E1_in_degree.csv           # Grado de entrada por nodo
│   ├── E2_pagerank_uniforme.csv   # PageRank uniforme y contraste de 3 métodos
│   ├── E3_E4_personalizados.csv   # PageRank personalizado (Tecnología y Deportes)
│   ├── E5_convergencia_alpha.csv  # Iteraciones, residuos y Top 5 según α
│   ├── E6_E7_E8_sensibilidad.csv  # Resumen de perturbaciones topológicas
│   ├── E6_E7_E8_detalle.csv       # Variación diferencial nodo a nodo
│   └── tabla_resumen_top5.csv     # Matriz comparativa de rankings
└── figuras/                       # Gráficos y diagramas científicos (.png)
    ├── fig1_red_base.png          # Topología del grafo con colores por categoría
    ├── fig2_red_pagerank_uniforme.png # Red con nodos proporcionales a PR uniforme
    ├── fig3_red_pagerank_tech.png     # Red con nodos proporcionales a PR tecnológico
    ├── fig4_red_pagerank_deportes.png # Red con nodos proporcionales a PR deportivo
    ├── fig5_convergencia_alpha.png    # Curvas de residuo e histograma de iteraciones
    ├── fig6_barras_rankings.png       # Comparación de in-degree vs PageRanks
    ├── fig7_sensibilidad.png          # Histogramas diferenciales ante cambios
    └── fig8_top5_por_alpha.png        # Evolución de los 10 primeros según α
```

> **Nota sobre borradores internos:** Los borradores preliminares y bancos de estudio internos del equipo se conservan localmente y se encuentran excluidos del repositorio mediante `.gitignore` para mantener un historial limpio y profesional.

---

## 4. Instrucciones de Reproducción

El proyecto está diseñado para ser reproducido desde cualquier terminal con Python 3.10 o superior.

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/lucarpio25/Proyecto-Algebra-Lineal.git
cd Proyecto-Algebra-Lineal
```

### Paso 2: Crear y activar entorno virtual (recomendado)

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux / macOS:
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar todos los experimentos

```bash
python codigo/ejecutar_experimentos.py
```

*Salida:* Verifica el ejemplo de 3 nodos, ejecuta experimentos E1 a E8, valida residuos numéricos ($< 10^{-10}$) y exporta los archivos CSV a `resultados/`.

### Paso 5: Generar todas las visualizaciones

```bash
python codigo/generar_visualizaciones.py
```

*Salida:* Genera las 8 figuras científicas en formato PNG dentro de `figuras/`.

---

## 5. Resultados Experimentales y Comprobaciones

### 5.1. Validación Preliminar: Ejemplo Canónico de 3 Nodos del Docente

Se reprodujo el ejemplo exacto propuesto por el docente (Prof. Oswaldo Velásquez) en la Sección 6 de la guía de cátedra: aristas $1 \to 2$, $2 \to 1$, $2 \to 3$ y $3 \to 1$ con $\alpha = 1/2$.

Matriz de transición estocástica:

$$
P = \begin{pmatrix} 0 & 1/2 & 1 \\ 1 & 0 & 0 \\ 0 & 1/2 & 0 \end{pmatrix}
$$

#### Caso 1: Reinicio Uniforme ($v = \frac{1}{3}\mathbf{1}$)

- **Solución analítica exacta:**

$$
r = \frac{1}{39} \begin{pmatrix} 15 \\ 14 \\ 10 \end{pmatrix} \approx \begin{pmatrix} 0.384615 \\ 0.358974 \\ 0.256410 \end{pmatrix}
$$

- **Power Method (propio):** $[0.384615, 0.358974, 0.256410]^T$
- **Sistema Lineal $(I - \alpha P)^{-1}b$:** $[0.384615, 0.358974, 0.256410]^T$
- **NetworkX:** $[0.384615, 0.358974, 0.256410]^T$
- **Discrepancia frente a solución teórica exacta:** $1.40 \times 10^{-13}$ (residuo: $1.52 \times 10^{-13}$).

#### Caso 2: Reinicio Personalizado en Nodo 3 ($v = e_3 = (0, 0, 1)^T$)

- **Solución analítica exacta:**

$$
r = \frac{1}{13} \begin{pmatrix} 4 \\ 2 \\ 7 \end{pmatrix} \approx \begin{pmatrix} 0.307692 \\ 0.153846 \\ 0.538462 \end{pmatrix}
$$

- **Power Method (propio):** $[0.307692, 0.153846, 0.538462]^T$
- **Sistema Lineal:** $[0.307692, 0.153846, 0.538462]^T$
- **NetworkX:** $[0.307692, 0.153846, 0.538462]^T$
- **Discrepancia frente a solución teórica exacta:** $9.33 \times 10^{-14}$ (residuo: $1.14 \times 10^{-13}$).

*Ambos casos verifican estocasticidad estricta ($\sum r_i = 1.000000000000$) y no negatividad.*

---

### 5.2. Comparación de Rankings Top 5 (Red de 20 Nodos)

| Posición | In-Degree (Conteo Bruto) | PageRank Uniforme ($\alpha = 0.85$) | PR Tech ($70\%$ reinicio) | PR Deportes ($70\%$ reinicio) |
|:---:|:---:|:---:|:---:|:---:|
| **1** | $T_1$ (5 enlaces) | **$C_1$ (0.0914)** | **$T_1$ (0.1174)** | **$D_1$ (0.1015)** |
| **2** | $D_1$ (5 enlaces) | $T_1$ (0.0828) | $T_3$ (0.0842) | $D_2$ (0.0936) |
| **3** | $C_1$ (5 enlaces) | $D_1$ (0.0692) | $T_6$ (0.0779) | $C_1$ (0.0708) |
| **4** | $T_3$ (4 enlaces) | **$C_3$ (0.0686)** | $C_1$ (0.0722) | $T_1$ (0.0698) |
| **5** | $D_2$ (4 enlaces) | $D_2$ (0.0631) | $T_5$ (0.0674) | $D_7$ (0.0678) |

#### Hallazgos Clave:

1. **Desempate de Portales:** A pesar de empatar con 5 enlaces recibidos, $C_1$ supera a $T_1$ y $D_1$ debido a que sus enlaces provienen de páginas con menor grado de salida (concentran su voto) y a la mayor densidad del subgrafo cultural.
2. **Transferencia de Prestigio:** $C_3$, con solo 3 enlaces entrantes (puesto 7 en in-degree), asciende al 4.º lugar en PageRank uniforme porque recibe un enlace directo del líder $C_1$.
3. **Personalización Temática:** Al concentrar el 70 % de reinicio en tecnología o deportes, los nodos correspondientes dominan el Top 5 respetando los caminos de la red.

---

### 5.3. Convergencia y Sensibilidad al Parámetro $\alpha$ (Experimento E5)

| $\alpha$ | Iteraciones | Residuo Final $\lVert \delta \rVert_1$ | Top 1 | Top 2 | Top 3 | Top 4 | Top 5 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.50** | **24** | $3.15 \times 10^{-11}$ | $T_1$ | $C_1$ | $D_1$ | $D_2$ | $T_3$ |
| **0.85** | **65** | $6.13 \times 10^{-11}$ | $C_1$ | $T_1$ | $D_1$ | $C_3$ | $D_2$ |
| **0.95** | **101** | $8.06 \times 10^{-11}$ | $C_1$ | $T_1$ | $C_3$ | $D_1$ | $D_2$ |
| **0.99** | **128** | $8.23 \times 10^{-11}$ | $C_1$ | $C_3$ | $T_1$ | $D_1$ | $C_6$ |

- Al aumentar $\alpha$ de 0.50 a 0.99, las iteraciones se incrementan en un **533 %** (de 24 a 128), concordando con la cota de contracción $\alpha^k$.
- Se manifiesta el fenómeno de **inversión de rangos (*rank reversal*)**: a $\alpha=0.50$, $T_1$ lidera; a $\alpha \ge 0.85$, $C_1$ asume el primer puesto; y a $\alpha=0.99$, $C_3$ salta al segundo lugar y $C_6$ ingresa al Top 5.

---

### 5.4. Sensibilidad ante Modificaciones de Enlaces (E6, E7, E8)

- **Añadir 3 enlaces hacia portales (E6):** $D_1$ incrementa su puntaje en $+0.011661$ y $D_2$ supera a $C_3$.
- **Quitar 3 enlaces de entrada a portales (E7):** El flujo se redistribuye hacia páginas internas; $C_6$ aumenta $+0.036652$ y asciende a la cima del ranking.
- **Dangling Node en $D_6$ (E8):** Al eliminar todos sus enlaces de salida, se aplica el vector estocástico $1/20$ en su columna. Como consecuencia, **$D_2$ pierde $-0.015135$** de relevancia y sale del Top 5, ingresando $T_3$.

---

## 6. Guion del Video Final (10 Minutos)

| Tiempo | Sección | Contenido | Responsable |
|---|---|---|---|
| 0:00 – 1:00 | Pregunta | Título, integrantes y problema. Pregunta de investigación, objetivo y alcance (red simulada de 20 páginas). | Luciana |
| 1:00 – 2:00 | Formulación | De la red a la matriz de transición P,, tratamiento de nodos sin salidas, reinicio v y parámetro α. | Sofía |
| 2:00 – 3:00 | Formulación | Ecuación r = αPr + (1−α)v, existencia y unicidad, y las tres formulaciones (sistema lineal, vector propio, punto fijo). | Sofía |
| 3:00 – 4:00 | Convergencia | Contracción, cota de error αᵏ y certificado de error con el residuo (1/(1−α)). | Sofía |
| 4:00 – 5:30 | Experimentos: verificación | Comprobación del ejemplo de tres nodos, comparación de la implementación propia con la solución directa y NetworkX, residuo y suma de componentes. | Marianela |
| 5:30 – 6:45 | Experimentos: rankings | Enlaces recibidos vs. PageRank uniforme vs. personalizado (tecnología y deportes), cambios en el top 5. | Manuel |
| 6:45 – 8:00 | Experimentos: sensibilidad | α ∈ {0.50, 0.85, 0.95, 0.99}: residuo e iteraciones. Modificación de enlaces y caso con una página sin salidas. | Manuel |
| 8:00 – 9:00 | Interpretación | Qué noción de relevancia produce cada clasificación y cuándo coinciden o difieren. | Marianela |
| 9:00 – 10:00 | Límites y cierre | Límites, conclusiones, referencias principales y enlace al repositorio. | Luciana |

---

## 7. Registro de Contribuciones Individuales

### Marianela Usnayo Gutierrez

- Verificar los resultados: sustitución en el ejemplo de tres nodos, suma de componentes igual a 1, no negatividad, residuo y cumplimiento de la tolerancia de error.
- Comparar la implementación propia con la solución directa del sistema lineal y con NetworkX, cuidando que coincidan alfa, personalización, pesos y tratamiento de nodos sin salidas.
- Probar que el repositorio sea reproducible: ejecutarlo desde cero y confirmar que las instrucciones del README permiten obtener los resultados presentados.
- Revisar que las tablas y figuras coincidan con los resultados del código.
- Coordinar la grabación y editar el video de 10 minutos, con fórmulas y gráficos legibles y audio comprensible.
- Colocar el enlace del video en el README y comprobar que el docente pueda verlo.

### Luciana Carpio Cárdenas

- Crear el repositorio de GitHub y su estructura de carpetas.
- Redactar y actualizar el README: título, tema, problema, objetivo, integrantes, organización de archivos, instrucciones de ejecución, resultados principales y enlace al video.
- Mantener el planteamiento del problema, la pregunta de investigación, el objetivo y el alcance.
- Documentar la procedencia de la red y las reglas de construcción junto con Manuel.
- Implementar el algoritmo iterativo de PageRank en Python, incluyendo la construcción de la matriz de transición, el tratamiento uniforme de nodos sin salidas y los parámetros de reinicio y personalización.
- Incorporar el cálculo del residuo, el certificado de error, el criterio de parada y el máximo de iteraciones.
- Documentar el código y registrar las bibliotecas y versiones necesarias para ejecutarlo.

### Manuel Sialer Flores

- Construir la red simulada de 20 páginas sobre tecnología, deportes y cultura, y documentar sus reglas.
- Preparar los datos de nodos y enlaces y definir las distribuciones de reinicio para las preferencias por tecnología y deportes.
- Utilizar la implementación del grupo para calcular y comparar el conteo de enlaces recibidos, PageRank uniforme y las dos versiones personalizadas.
- Ejecutar los experimentos con alfa = 0.50, 0.85, 0.95 y 0.99, registrando residuo, certificado de error, número de iteraciones y cambios en los cinco primeros lugares.
- Modificar enlaces seleccionados, incluyendo un caso con una página sin enlaces de salida, y comparar cambios de puntuación y de orden.
- Generar los gráficos de la red con tamaños de nodo proporcionales a las puntuaciones y las tablas reproducibles.

### Sofía Catherine Briceño Rosado

- Explicar la construcción de la matriz de transición y justificar la regla para nodos sin salidas.
- Desarrollar la existencia y unicidad de la solución y las tres formulaciones: sistema lineal, vector propio e iteración de punto fijo.
- Explicar la convergencia, la norma uno, el residuo y el certificado de error utilizado para detener el algoritmo.
- Desarrollar el análisis teórico de sensibilidad respecto a la preferencia v y a cambios en P.
- Revisar la correspondencia entre las fórmulas matemáticas y la implementación junto con Luciana.
- Cuidar la notación, justificar los procedimientos e incorporar las citas y referencias en formato IEEE.

### Actividades de todo el grupo

- Reunirse para planificar, revisar el avance y actualizar el cronograma.
- Preparar la presentación inicial y la entrega parcial, incorporando la retroalimentación.
- Interpretar conjuntamente los resultados y formular conclusiones y limitaciones.
- Preparar el guion y participar en el video explicando contenido sustantivo.
- Registrar los aportes concretos de cada integrante y el uso de IA, cuando corresponda.
- Revisar el repositorio y el video antes de entregar.
- Comprender el funcionamiento general del código y los fundamentos matemáticos del proyecto.
- Prepararse para la ronda de preguntas y revisar las seis preguntas de defensa del artículo.

---

## 8. Cronograma de Actividades Pendientes (Entrega Final)

| Actividades | S12 L | S12 Ma | S12 Mi | S12 J | S12 V | S12 S | S12 D | S13 L | S13 Ma | S13 Mi | S13 J | S13 V | S13 S | S13 D | S14 L | S14 Ma | S14 Mi | S14 J | S14 V | S14 S | S14 D |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Planificación | ■ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Planteamiento del proyecto y GitHub |   | ■ | ■ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Conceptos matemáticos y fuentes |   |   |   | ■ | ■ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Diseño de la red y experimentos |   |   |   |   |   | ■ | ■ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Planificación del video |   |   |   |   |   |   | ■ |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Reproducir ejemplo de 3 nodos y verificarlo (sustitución, suma) |   |   |   |   |   |   |   | ■ | ■ |   |   |   |   |   |   |   |   |   |   |   |   |
| Construir red de 20 nodos, documentar procedencia y reglas |   |   |   |   |   |   |   |   | ■ | ■ | ■ |   |   |   |   |   |   |   |   |   |   |
| Implementación propia: P, iteración, residuo y comparación con NetworkX |   |   |   |   |   |   |   |   |   | ■ | ■ | ■ | ■ |   |   |   |   |   |   |   |   |
| Experimentos con α ∈ {0.50, 0.85, 0.95, 0.99}: residuo, iteraciones, top 5 |   |   |   |   |   |   |   |   |   |   |   |   | ■ | ■ | ■ |   |   |   |   |   |   |
| Sensibilidad: añadir/quitar aristas, caso con nodo sin salidas |   |   |   |   |   |   |   |   |   |   |   |   |   | ■ | ■ | ■ |   |   |   |   |   |
| Tabla reproducible, README y orden del repositorio |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ■ | ■ | ■ | ■ |   |   |   |
| Guión del video (10 min) y reparto de intervenciones |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ■ |   |   |   |   |
| Grabación y edición del video; enlace en README |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ■ |   |   |   |
| Revisión final y entrega |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ■ | ■ | ■ |


---

## 9. Declaración de Uso de Inteligencia Artificial

En estricto cumplimiento del numeral 9 de las indicaciones del curso:

- **Herramientas empleadas:** Antigravity (Google DeepMind) con modelos Claude Opus 4.6 y Gemini Flash.
- **Finalidad:** Apoyo en la corrección y automatización de la sintaxis de scripts en Python (estructuración de bucles de graficación con Matplotlib), formato de tablas en Markdown y corrección de estilo de la documentación.
- **Procedimientos de verificación:** Todos los procedimientos matemáticos fueron verificados analíticamente a mano y validados computacionalmente contra bibliotecas estándar (`numpy.linalg.solve`, `networkx.pagerank`). Los resultados numéricos satisfacen estrictamente los criterios de estocasticidad ($\sum r_i = 1$) y residuos de máquina ($< 10^{-10}$). Cada integrante del equipo comprende y asume la responsabilidad intelectual y académica total del contenido aquí presentado.

---

## 10. Referencias Bibliográficas (IEEE)

```text
[1] L. Page, S. Brin, R. Motwani y T. Winograd, "The PageRank Citation Ranking: Bringing Order to the Web", Stanford InfoLab, Technical Report 1999-66, 1999. [En línea]. Disponible en: https://ilpubs.stanford.edu/422/
[2] A. N. Langville y C. D. Meyer, Google’s PageRank and Beyond: The Science of Search Engine Rankings. Princeton, NJ, USA: Princeton University Press, 2006.
[3] D. F. Gleich, "PageRank Beyond the Web", SIAM Review, vol. 57, no. 3, pp. 321–363, 2015. DOI: 10.1137/140976649.
[4] S.-W. Son, C. Christensen, P. Grassberger y M. Paczuski, "PageRank and rank-reversal dependence on the damping factor", Physical Review E, vol. 86, no. 6, p. 066104, 2012. DOI: 10.1103/PhysRevE.86.066104.
[5] P. Boldi, M. Santini y S. Vigna, "PageRank: Functional Dependencies", ACM Transactions on Information Systems, vol. 27, no. 4, pp. 1–23, 2009. DOI: 10.1145/1629096.1629097.
[6] G. Strang, Introduction to Linear Algebra, 5.ª ed. Wellesley, MA, USA: Wellesley-Cambridge Press, 2016.
[7] NetworkX Developers, "pagerank — NetworkX documentation", [En línea]. Disponible en: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html
```
