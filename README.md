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

### 1.1. Contexto y problema

Las páginas web y sus enlaces forman una red dirigida: cada página es un nodo y cada enlace tiene un origen y un destino. Una forma sencilla de clasificar las páginas consiste en contar cuántos enlaces recibe cada una. Esta medida se denomina grado de entrada o in-degree. Sin embargo, considera todos los enlaces recibidos por igual, sin distinguir la relevancia de las páginas que los proporcionan.

PageRank incorpora esa diferencia: cada página reparte su puntuación entre sus enlaces de salida. Por ello, la puntuación de una página depende tanto de los enlaces que recibe como de las puntuaciones de las páginas que la enlazan. El modelo puede interpretarse como una persona que navega siguiendo enlaces y que, de vez en cuando, reinicia la navegación. Las puntuaciones representan la proporción de visitas que recibiría cada página a largo plazo bajo esas reglas. En PageRank uniforme, los reinicios asignan la misma probabilidad a todas las páginas. En PageRank personalizado, se modifican esas probabilidades para favorecer determinados temas, como tecnología o deportes.

El proyecto comparará estas clasificaciones en una red simulada y analizará cómo cambian al modificar las preferencias, algunos enlaces y el parámetro de seguimiento de enlaces. La relevancia calculada depende de la estructura de la red y de las decisiones del modelo. No garantiza la calidad, credibilidad o veracidad del contenido de las páginas.

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

### 2.1. Construcción de la matriz de transición P

La red se representa mediante una matriz P de 20 filas y 20 columnas. La entrada P_ij indica la probabilidad de pasar desde la página j hacia la página i.

Las columnas representan páginas de origen y las filas representan páginas de destino.

Si una página j tiene d_j enlaces de salida, se asigna la misma probabilidad a cada uno:

$$
P_{ij}=
\begin{cases}
1/d_j & \text{si existe un enlace de } j \text{ hacia } i,\\
0 & \text{en otro caso},
\end{cases}
\qquad d_j>0.
$$

Por ejemplo, si A enlaza únicamente a B y C, desde A se asigna una probabilidad de 1/2 a cada destino.

P es estocástica por columnas: sus entradas son no negativas y cada columna suma uno.

$$
P_{ij}\geq 0,
\qquad
\sum_{i=1}^{n}P_{ij}=1.
$$

Si x contiene las puntuaciones actuales, el producto Px las redistribuye según los enlaces de la red.

#### Tratamiento de páginas sin enlaces de salida

Una página sin salidas produciría una columna de ceros. Sin una corrección, el reparto no conservaría toda la probabilidad.

Para evitarlo, se reemplaza esa columna por una distribución uniforme:

$$
P_{ij}=\frac{1}{n}
\quad \text{para todo } i,
\quad \text{si } d_j=0.
$$

En nuestra red, cada entrada de esa columna vale 1/20 = 0.05, incluida la correspondiente a la propia página.

Esta redistribución es una regla del modelo: no añade enlaces a la lista del grafo.

La regla se mantiene uniforme tanto en PageRank general como en el personalizado. También se configura explícitamente en NetworkX mediante el parámetro `dangling`, para comparar los mismos modelos.

---

### 2.2. Parámetro de Amortiguamiento $\alpha$ y Vector de Reinicio $v$

Para evitar trampas de ciclo cerrado (*spider traps*) y componentes desconectadas, se incorpora el modelo de teletransportación:

- Con probabilidad $\alpha \in (0, 1)$, el navegante sigue un enlace saliente.
- Con probabilidad $(1 - \alpha)$, salta al azar según la distribución de un vector de reinicio $v \in \mathbb{R}^n$, con $v_i \ge 0$ y $\sum v_i = 1$.
- **Uniforme:** $v = \frac{1}{n}\mathbf{1}$.
- **Personalizado:** $v$ concentra probabilidad (por ejemplo, 70 %) en un subconjunto de nodos temáticos.

---

### 2.3. Tres formulaciones algebraicas equivalentes

PageRank puede expresarse como una ecuación de equilibrio, un sistema lineal o un problema de vectores propios. Las tres formulaciones describen las mismas puntuaciones finales.

#### 1. Ecuación de equilibrio o punto fijo

El vector de puntuaciones r satisface:

$$
r=\alpha Pr+(1-\alpha)v,
\qquad
r_i\geq 0,
\qquad
\sum_i r_i=1.
$$

El término alfa · Pr representa el seguimiento de enlaces y el término (1 − alfa) · v representa los reinicios.

En el equilibrio, aplicar nuevamente esta actualización produce las mismas puntuaciones.

#### 2. Sistema de ecuaciones lineales

Reorganizando la ecuación:

$$
(I-\alpha P)r=(1-\alpha)v,
$$

donde I es la matriz identidad.

Las incógnitas son las puntuaciones de las páginas. En el código, el sistema se resuelve mediante `numpy.linalg.solve`, sin calcular explícitamente la inversa.

**Existencia y unicidad**

Como P es estocástica por columnas, su norma matricial inducida por la norma uno cumple:

$$
\|P\|_1=1.
$$

Por tanto:

$$
\|\alpha P\|_1=\alpha<1.
$$

Esta condición garantiza la convergencia de la serie geométrica de matrices, denominada serie de Neumann:

$$
(I-\alpha P)^{-1}
=
\sum_{m=0}^{\infty}(\alpha P)^m.
$$

Así, I − alfa · P es invertible y el sistema tiene una única solución:

$$
r=(1-\alpha)(I-\alpha P)^{-1}v.
$$

La expresión con inversa es una identidad matemática; no es el procedimiento utilizado para calcular r en el código.

Además, la serie muestra que r tiene componentes no negativas. Como cada vector P elevado a m multiplicado por v suma uno, las componentes de r también suman uno.

#### 3. Vector propio de la matriz Google

Se define la matriz Google:

$$
G=\alpha P+(1-\alpha)v\mathbf{1}^{T}.
$$

El símbolo de unos transpuesto representa un vector fila formado por unos. El producto de v por ese vector genera una matriz cuyas columnas son copias de v.

Como las componentes de r suman uno:

$$
Gr=\alpha Pr+(1-\alpha)v=r.
$$

Por tanto, r es un vector propio de G asociado al valor propio uno, normalizado para que sus componentes sumen uno.

Esta relación permite interpretar r como una distribución estacionaria: las probabilidades permanecen iguales después de aplicar las reglas de navegación.

**Condición de positividad**

Si todas las componentes de v son estrictamente positivas y alfa está entre cero y uno, todas las entradas de G son positivas. Esto ocurre en las tres variantes de la red de 20 páginas utilizadas en el proyecto.

Bajo esa condición, el teorema de Perron-Frobenius garantiza que el valor propio uno es simple, que los demás valores propios tienen módulo menor que uno y que la distribución estacionaria tiene componentes estrictamente positivas.

Si v contiene ceros, no se puede afirmar automáticamente que G sea positiva. Sin embargo, la existencia y unicidad de la solución de PageRank siguen garantizadas por la invertibilidad demostrada anteriormente. Esto permite tratar también el ejemplo del docente con reinicio concentrado en un solo nodo.

---

### 2.4. Convergencia del método iterativo

El algoritmo comienza con puntuaciones uniformes y las actualiza mediante:

$$
x^{(k+1)}=\alpha Px^{(k)}+(1-\alpha)v.
$$

Aquí, x representa una aproximación a las puntuaciones finales y k indica el número de iteración. La matriz P, alfa y el vector de reinicio v permanecen fijos durante cada ejecución.

#### Convergencia hacia el equilibrio

Sea r el vector de equilibrio. Al restar su ecuación de la actualización se obtiene:

$$
x^{(k+1)}-r=\alpha P(x^{(k)}-r).
$$

La norma uno de un vector se calcula sumando los valores absolutos de sus componentes. Como P es estocástica por columnas, su norma matricial inducida es uno. Por tanto:

$$
\|x^{(k+1)}-r\|_1
\leq
\alpha\|x^{(k)}-r\|_1.
$$

Esto significa que la distancia al equilibrio se reduce en cada paso por un factor no mayor que alfa. Aplicando la desigualdad repetidamente:

$$
\|x^{(k)}-r\|_1
\leq
\alpha^k\|x^{(0)}-r\|_1.
$$

Como 0 < alfa < 1, el factor alfa elevado a k tiende a cero. Así, las aproximaciones convergen al equilibrio desde cualquier distribución inicial de probabilidad.

Esta cota garantiza convergencia, pero no predice exactamente cuántas iteraciones necesitará una red concreta.

#### Residuo y certificado de error

El residuo de una aproximación x se define como:

$$
\rho(x)=\|x-\alpha Px-(1-\alpha)v\|_1.
$$

El residuo compara las puntuaciones actuales con las que se obtendrían al actualizarlas nuevamente. El error, en cambio, mide la distancia entre x y la solución de equilibrio r.

El residuo permite establecer la siguiente cota:

$$
\|x-r\|_1\leq\frac{\rho(x)}{1-\alpha}.
$$

Por ejemplo, con alfa = 0.85 y un residuo de 10⁻¹¹, el error no supera aproximadamente 6.67 × 10⁻¹¹.

#### Criterio de parada utilizado

En el proyecto se establece una tolerancia de error en norma uno de 10⁻¹⁰. El algoritmo se detiene cuando:

$$
\frac{\rho(x)}{1-\alpha}\leq 10^{-10}.
$$

El certificado se calcula sobre el mismo vector que devuelve la función.

También se fija un máximo de 5000 iteraciones. Si se alcanza sin cumplir el criterio, el programa genera un error e informa que no se certificó la precisión requerida.

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

### 5.3. Convergencia y sensibilidad al parámetro alfa (E5)

Se evaluaron cuatro valores de alfa utilizando la misma red, el reinicio uniforme y una distribución inicial uniforme.

El algoritmo se detuvo cuando el certificado de error —residuo dividido entre 1 − alfa— fue menor o igual que 10⁻¹⁰.

| Alfa | Iteraciones | Residuo final aproximado | Cota del error aproximada | Primeros cinco lugares |
|:---:|:---:|:---:|:---:|---|
| 0.50 | 24 | 3.15 × 10⁻¹¹ | 6.31 × 10⁻¹¹ | T1, C1, D1, D2, T3 |
| 0.85 | 70 | 1.32 × 10⁻¹¹ | 8.78 × 10⁻¹¹ | C1, T1, D1, C3, D2 |
| 0.95 | 116 | 4.24 × 10⁻¹² | 8.49 × 10⁻¹¹ | C1, T1, C3, D1, D2 |
| 0.99 | 157 | 9.18 × 10⁻¹³ | 9.18 × 10⁻¹¹ | C1, C3, T1, D1, C6 |

Las cuatro ejecuciones cumplieron la tolerancia establecida. Las cifras se muestran redondeadas; las comprobaciones utilizan los valores completos.

En esta red, las iteraciones aumentaron de 24 a 157 entre alfa = 0.50 y alfa = 0.99, un incremento aproximado del 554.2 %. Al acercarse alfa a uno, la reducción garantizada del error por paso es más lenta y se exige un residuo menor para certificar la misma precisión.

También cambió el ranking: T1 lidera con alfa = 0.50; C1 ocupa el primer puesto con los otros valores evaluados. Con alfa = 0.99, C3 asciende al segundo lugar y C6 entra en los primeros cinco.

Las diferencias en norma uno entre las aproximaciones iterativas y la solución directa fueron menores que 10⁻¹⁰ en las cuatro ejecuciones.

Los datos completos están disponibles en `resultados/E5_convergencia_alpha.csv`. Estos resultados corresponden a la red estudiada y no establecen un valor de alfa universalmente óptimo.

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
