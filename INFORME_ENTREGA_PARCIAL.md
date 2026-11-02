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
| **Luciana Carpio Cárdenas**        | [Código] | Delimitación del problema, formulación de la pregunta de investigación, alcance, gobernanza del repositorio y documentación de procedencia de la red.                       |
| **Manuel Sialer**                  | [Código] | Diseño topológico de la red de 20 nodos, implementación computacional en Python, ejecución de la batería experimental (E1–E8) y generación de figuras.                      |
| **Marianela Usnayo Gutierrez**     | [Código] | Verificaciones numéricas (residuos, estocasticidad, sumas unitarias), contraste inter-algorítmico (Iterativo vs. Lineal vs. NetworkX) y estructuración del guion del video. |

---

## 1. Definición Actualizada del Problema, Objetivo y Alcance

### 1.1. Contexto y Planteamiento del Problema

En el ecosistema de la World Wide Web, los hipervínculos estructuran un grafo dirigido masivo donde las páginas actúan como nodos y los enlaces como aristas orientadas. La aproximación elemental para determinar la centralidad o importancia de un nodo consiste en el cómputo de su grado de entrada (_in-degree_):

$$\text{deg}_{\text{in}}(i) = \sum_{j=1}^{n} A_{ij}$$

No obstante, esta formulación presenta limitaciones teóricas insalvables:

1. **Ponderación uniforme ingenua:** Asume que todos los votos entrantes poseen idéntica autoridad, ignorando que un enlace proveniente de un portal altamente reconocido confiere mayor credibilidad que decenas de enlaces desde páginas marginales.
2. **Vulnerabilidad a manipulación local:** Es fácilmente alterable mediante redes artificiales de enlaces (_link farms_).
3. **Falta de contextualización temática:** Una clasificación universal no distingue los perfiles de interés del usuario (por ejemplo, búsquedas orientadas a computación frente a contenidos deportivos).

El algoritmo **PageRank**, formulado originalmente por Sergey Brin y Larry Page (1998), resuelve estas deficiencias modelando la navegación mediante una **cadena de Markov ergódica**, donde la relevancia de una página se retroalimenta iterativamente de la relevancia de las páginas que la enlazan, ponderada inversamente por el número de enlaces salientes de estas. Asimismo, su variante **PageRank Personalizado** (_Personalized PageRank_ - PPR) introduce un sesgo controlado en el vector de reinicio, permitiendo canalizar la autoridad hacia comunidades temáticas específicas.

### 1.2. Pregunta de Investigación

> _¿De qué manera varía la jerarquización de relevancia en una red dirigida de 20 páginas web al contrastar el conteo de enlaces entrantes (in-degree), PageRank uniforme y PageRank personalizado, y qué sensibilidad exhiben las puntuaciones, el Top 5 y la tasa de convergencia ante alteraciones en el factor de amortiguamiento $\alpha$ y modificaciones en la topología de la red?_

### 1.3. Objetivo General

Implementar, verificar y analizar computacional y matemáticamente los algoritmos de PageRank uniforme y personalizado sobre una red simulada de 20 páginas web con tres categorías temáticas, contrastando rigurosamente los resultados contra soluciones algebraicas directas y bibliotecas científicas de referencia, cuantificando la sensibilidad del modelo ante variaciones del parámetro $\alpha \in \{0.50, 0.85, 0.95, 0.99\}$ y perturbaciones estructurales en los enlaces.

### 1.4. Objetivos Específicos

1. Formular analíticamente la matriz de transición estocástica $P$ y formalizar la regla estocástica para nodos sin enlaces de salida (_dangling nodes_).
2. Deducir y demostrar la equivalencia entre las tres formulaciones del problema: punto fijo iterativo, sistema de ecuaciones lineales no homogéneo $(I - \alpha P)r = (1-\alpha)v$ y vector propio dominante de la matriz Google $G$.
3. Construir una implementación propia en Python basada en el método de las potencias (_Power Method_), validando su reproducibilidad con el ejemplo patrón de 3 nodos y contrastándola contra la inversión matricial exacta y `networkx.pagerank`.
4. Diseñar y ejecutar ocho experimentos numéricos (E1 a E8) para medir el impacto de la personalización temática, la tasa de contracción y el fenómeno de inversión de rangos (_rank reversal_).
5. Cuantificar el residuo $\|r - \alpha P r - (1-\alpha)v\|_1$ como certificado riguroso de precisión numérica.

### 1.5. Alcance y Delimitación

- **Dominio experimental:** Se diseñó una red simulada y reproducible de 20 nodos y 56 aristas dirigidas, dividida en Tecnología (7 nodos), Deportes (7 nodos) y Cultura (6 nodos).
- **Parámetros evaluados:** Factores de amortiguamiento $\alpha \in \{0.50, 0.85, 0.95, 0.99\}$; vectores de reinicio uniforme ($v_{\text{uni}}$) y personalizados ($v_{\text{tech}}$, $v_{\text{dep}}$) con una concentración del 70 % en la categoría de interés.
- **Límites:** El estudio evalúa exclusivamente la autoridad derivada de la estructura de enlaces topológica y las preferencias de reinicio; no analiza contenido textual, semántico ni veracidad intrínseca de las páginas.

---

## 2. Fundamentación y Desarrollo Matemático Riguroso

### 2.1. De la Red a la Matriz de Transición Estocástica $P$

Sea un grafo dirigido $G = (V, E)$ con conjunto de vértices $V = \{1, 2, \dots, n\}$ y conjunto de aristas dirigidas $E \subseteq V \times V$. Para cada nodo $j \in V$, definimos su conjunto de enlaces salientes como $\text{Out}(j) = \{i \in V : (j \to i) \in E\}$ y su grado de salida como $d_j^{\text{out}} = |\text{Out}(j)|$.

La probabilidad condicional de que un navegante aleatorio ubicado en el nodo $j$ elija transitar hacia el nodo $i$ siguiendo un enlace saliente viene dada por los coeficientes de la matriz de adyacencia normalizada $P \in \mathbb{R}^{n \times n}$:

$$P_{ij} = \begin{cases} \frac{1}{d_j^{\text{out}}} & \text{si } (j \to i) \in E \\ 0 & \text{en otro caso} \end{cases}$$

#### Tratamiento Riguroso de Nodos sin Salidas (_Dangling Nodes_)

Si un nodo $j$ carece de enlaces salientes ($d_j^{\text{out}} = 0$), la columna $j$ de la matriz resultaría idénticamente nula ($\sum_{i=1}^n P_{ij} = 0$), quebrantando la propiedad estocástica y generando una disipación continua de probabilidad en el proceso markoviano ($\|r^{(k)}\|_1 \to 0$).

Para preservar la conservación de la probabilidad, se define formalmente la corrección estocástica: cuando el navegante arriba a un sumidero, salta con idéntica probabilidad hacia cualquier nodo de la red:

$$P_{ij} = \frac{1}{n} \quad \forall i \in \{1, \dots, n\} \quad \text{si } d_j^{\text{out}} = 0$$

Con esta regla, $P$ es estrictamente **estocástica por columnas**:
$$\sum_{i=1}^{n} P_{ij} = 1 \quad \forall j \in \{1, \dots, n\}, \quad P_{ij} \ge 0$$

---

### 2.2. Parámetro de Amortiguamiento $\alpha$ y Vector de Reinicio $v$

Para garantizar la ergodicidad (irreducibilidad y aperiodicidad) de la cadena de Markov y resolver el problema de trampas cerradas (_spider traps_), se introduce el modelo del navegante aleatorio con teletransportación:

- Con probabilidad $\alpha \in (0, 1)$, el usuario sigue uno de los hipervínculos disponibles en la página actual.
- Con probabilidad complementaria $(1 - \alpha)$, el usuario abandona la secuencia de navegación y se teletransporta hacia una página elegida según una distribución de probabilidad dada por el **vector de reinicio** $v \in \mathbb{R}^n$, donde:

$$v_i \ge 0, \quad \sum_{i=1}^{n} v_i = 1$$

- **PageRank Uniforme:** $v = \mathbf{1}/n$, donde cada nodo recibe probabilidad de reinicio $1/n$.
- **PageRank Personalizado:** $v$ concentra peso probabilístico sobre un subconjunto de nodos semilla $S \subset V$:
  $$v_i = \begin{cases} \frac{\beta}{|S|} & \text{si } i \in S \\ \frac{1 - \beta}{n - |S|} & \text{si } i \notin S \end{cases}$$
  En nuestro proyecto, adoptamos $\beta = 0.70$ para privilegiar de forma contundente la categoría de interés.

---

### 2.3. Tres Formulaciones Algebraicas Equivalentes

#### Formulación 1: Ecuación de Punto Fijo (Forma Iterativa)

La distribución estacionaria de probabilidad $r \in \mathbb{R}^n$ satisface el balance de flujo invariante:

$$r = \alpha P r + (1 - \alpha) v$$

Sujeto a las restricciones de probabilidad:
$$r \ge \mathbf{0}, \quad \|r\|_1 = \sum_{i=1}^{n} r_i = 1$$

#### Formulación 2: Sistema de Ecuaciones Lineales No Homogéneo

Reordenando los términos algebraicamente:
$$r - \alpha P r = (1 - \alpha) v \implies (I - \alpha P) r = (1 - \alpha) v$$

Donde $I \in \mathbb{R}^{n \times n}$ es la matriz identidad.

**Teorema de Existencia y Unicidad de la Solución:**

1. Como la matriz $P$ es estocástica por columnas, su norma matricial inducida por la norma 1 es $\|P\|_1 = \max_{j} \sum_{i=1}^n |P_{ij}| = 1$.
2. Por las propiedades del radio espectral $\rho(A) \le \|A\|$, se tiene que $\rho(P) \le 1$.
3. Al multiplicar por el escalar $\alpha \in [0, 1)$, se cumple estrictamente:
   $$\rho(\alpha P) = \alpha \rho(P) \le \alpha < 1$$
4. En virtud del teorema de las series de Neumann, si el radio espectral de una matriz $M$ es estrictamente menor que 1, la matriz $(I - M)$ es invertible y su inversa se expresa como la serie convergente:
   $$(I - \alpha P)^{-1} = \sum_{m=0}^{\infty} (\alpha P)^m$$
5. Por consiguiente, la matriz $(I - \alpha P)$ es estrictamente no singular, garantizando la **existencia y unicidad** de la solución:
   $$r^* = (1 - \alpha) (I - \alpha P)^{-1} v$$

#### Formulación 3: Problema de Vectores y Valores Propios (Matriz Google $G$)

Observando que $\mathbf{1}^T r = \sum_{i=1}^n r_i = 1$, podemos reescribir $(1 - \alpha) v$ como $(1 - \alpha) v (\mathbf{1}^T r)$. Sustituyendo en la ecuación de punto fijo:

$$r = \alpha P r + (1 - \alpha) v \mathbf{1}^T r = \left( \alpha P + (1 - \alpha) v \mathbf{1}^T \right) r$$

Definiendo la **Matriz Google** $G \in \mathbb{R}^{n \times n}$:
$$G = \alpha P + (1 - \alpha) v \mathbf{1}^T$$

La ecuación se reduce a:
$$G r = 1 \cdot r$$

Esto demuestra que el vector de PageRank $r$ es el **vector propio dominante por la derecha** de la matriz estocástica y positiva $G$, asociado al valor propio $\lambda = 1$.  
Dado que $G_{ij} = \alpha P_{ij} + (1 - \alpha) v_i > 0$ (para $v_i > 0$), la matriz $G$ es estrictamente positiva y primitiva. Conforme al **Teorema de Perron-Frobenius**, el valor propio $\lambda_1 = 1$ es simple, estrictamente mayor en módulo que cualquier otro valor propio ($|\lambda_j| < 1 \quad \forall j \ge 2$), y su vector propio asociado admite una normalización con todas sus componentes estrictamente positivas ($r_i > 0$).

---

### 2.4. Demostración de Convergencia del Método Iterativo (_Power Method_)

El cómputo sucesivo se define mediante la relación de recurrencia:
$$r^{(k+1)} = \alpha P r^{(k)} + (1 - \alpha) v, \quad k = 0, 1, 2, \dots$$

Partiendo de una inicialización uniforme $r^{(0)} = \frac{1}{n} \mathbf{1}$.

#### Contracción y Cota de Error $\alpha^k$:

Restando el punto fijo exacto $r^* = \alpha P r^* + (1 - \alpha) v$ de la relación iterativa:
$$r^{(k+1)} - r^* = \alpha P (r^{(k)} - r^*)$$

Tomando la norma 1 a ambos lados y empleando la submultiplicatividad:
$$\|r^{(k+1)} - r^*\|_1 = \|\alpha P (r^{(k)} - r^*)\|_1 \le \alpha \|P\|_1 \|r^{(k)} - r^*\|_1$$

Como $\|P\|_1 = 1$:
$$\|r^{(k+1)} - r^*\|_1 \le \alpha \|r^{(k)} - r^*\|_1$$

Aplicando inducción matemática desde el paso inicial $k=0$:
$$\|r^{(k)} - r^*\|_1 \le \alpha^k \|r^{(0)} - r^*\|_1$$

Dado que $0 \le \alpha < 1$, se deduce directamente que $\lim_{k \to \infty} \alpha^k = 0$, lo que demuestra la **convergencia lineal global independiente del vector inicial**.

#### Criterio de Parada y Certificado de Error mediante el Residuo:

En la práctica computacional no se dispone de $r^*$. Se evalúa el vector residual:
$$\delta^{(k)} = r^{(k)} - \left( \alpha P r^{(k)} + (1 - \alpha) v \right) = (I - \alpha P) r^{(k)} - (1 - \alpha) v$$

Observando que $(I - \alpha P)(r^{(k)} - r^*) = \delta^{(k)}$:
$$r^{(k)} - r^* = (I - \alpha P)^{-1} \delta^{(k)}$$

Aplicando normas:
$$\|r^{(k)} - r^*\|_1 \le \|(I - \alpha P)^{-1}\|_1 \|\delta^{(k)}\|_1$$

Expandiendo mediante serie de Neumann:
$$\|(I - \alpha P)^{-1}\|_1 = \left\| \sum_{m=0}^\infty (\alpha P)^m \right\|_1 \le \sum_{m=0}^\infty \alpha^m \|P\|_1^m = \sum_{m=0}^\infty \alpha^m = \frac{1}{1 - \alpha}$$

Por consiguiente, se obtiene el **certificado formal de error**:
$$\|r^{(k)} - r^*\|_1 \le \frac{1}{1 - \alpha} \|\delta^{(k)}\|_1$$

Este resultado garantiza que controlar el residuo $\|\delta^{(k)}\|_1 < \tau (1 - \alpha)$ certifica que el error absoluto frente a la solución matemática exacta no supera la tolerancia deseada $\tau$.

---

## 3. Desarrollo Práctico e Implementación Computacional

### 3.1. Validación Preliminar con el Ejemplo de 3 Nodos del Docente

Para validar la corrección de nuestras funciones antes de procesar el grafo principal, se reprodujo el ejemplo canónico de 3 nodos ($A \to B, A \to C, B \to C, C \to A$) con $\alpha = 0.85$:

$$P_3 = \begin{pmatrix} 0 & 0 & 1 \\ 0.5 & 0 & 0 \\ 0.5 & 1 & 0 \end{pmatrix}, \quad v = \begin{pmatrix} 1/3 \\ 1/3 \\ 1/3 \end{pmatrix}$$

#### Resultados de la Validación Cruzada:

| Nodo  | Método Iterativo (_Power Method_) | Solución Analítica $(I - \alpha P)^{-1} b$ | Referencia NetworkX |
| :---: | :-------------------------------: | :----------------------------------------: | :-----------------: |
| **A** |           **0.387790**            |                **0.387790**                |    **0.387790**     |
| **B** |           **0.214811**            |                **0.214811**                |    **0.214811**     |
| **C** |           **0.397400**            |                **0.397400**                |    **0.397400**     |

- **Iteraciones:** 45 pasos hasta tolerancia $10^{-10}$.
- **Discrepancia Iterativo vs. Analítico:** $\|r_{\text{iter}} - r_{\text{lin}}\|_1 = 2.90 \times 10^{-11}$.
- **Discrepancia Iterativo vs. NetworkX:** $\|r_{\text{iter}} - r_{\text{nx}}\|_1 = 2.94 \times 10^{-11}$.
- **Residuo:** $\|r - \alpha P r - (1-\alpha)v\|_1 = 4.50 \times 10^{-11}$.
- **Verificación estocástica:** $\sum r_i = 1.000000000000$; $\min r_i = 0.2148 > 0$.

---

### 3.2. Topología de la Red Simulada de 20 Nodos

Se diseñó un grafo dirigido $G = (V, E)$ de $n = 20$ nodos y $|E| = 56$ aristas dirigidas, articulado en tres comunidades temáticas:

| Categoría      | Prefijo | Nodos         | Cantidad | Enlaces Salientes (Media) | Rol Estructural                                                                |
| -------------- | :-----: | ------------- | :------: | :-----------------------: | ------------------------------------------------------------------------------ |
| **Tecnología** |   `T`   | $T_1$ a $T_7$ |    7     |           2.85            | $T_1$ es portal dominante; $T_6$ actúa como puente hacia esports ($D_7$).      |
| **Deportes**   |   `D`   | $D_1$ a $D_7$ |    7     |           2.85            | $D_1$ es portal principal; $D_2$ es nodo de alto flujo; $D_6$ nodo periférico. |
| **Cultura**    |   `C`   | $C_1$ a $C_6$ |    6     |           2.50            | $C_1$ es portal central; subgrafo densamente interconectado.                   |

#### Reglas de Diseño Documentadas:

1. **Densidad moderada:** Grado de salida controlado entre 2 y 5 aristas por nodo.
2. **Homofilia temático-estructural:** 65 % de conexiones internas intra-categoría y 35 % de enlaces puente inter-categoría ($T_1 \to D_1, C_1$; $D_4 \to C_4$; $C_5 \to T_3$; $D_7 \to T_6, C_2$).
3. **Ausencia de auto-enlaces:** $P_{ii} = 0 \quad \forall i$.

---

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

| Ranking |   Nodo    | Nombre             | Categoría  | PageRank Uniforme | _In-Degree_ (Posición) |
| :-----: | :-------: | :----------------- | :--------- | :---------------: | :--------------------: |
|  **1**  | **$C_1$** | Portal Cultura     | Cultura    |   **0.091400**    |         5 (#3)         |
|  **2**  | **$T_1$** | Portal Tecnología  | Tecnología |   **0.082846**    |         5 (#1)         |
|  **3**  | **$D_1$** | Portal Deportes    | Deportes   |   **0.069240**    |         5 (#2)         |
|  **4**  | **$C_3$** | Cine               | Cultura    |   **0.068638**    |         3 (#7)         |
|  **5**  | **$D_2$** | Fútbol             | Deportes   |   **0.063060**    |         4 (#5)         |
|    6    |   $T_3$   | Reviews de Gadgets | Tecnología |     0.059617      |         4 (#4)         |
|    7    |   $T_6$   | Programación       | Tecnología |     0.052272      |         3 (#8)         |
|    8    |   $C_6$   | Teatro             | Cultura    |     0.050087      |        2 (#17)         |

#### Justificación del Desempate:

1. **$C_1$ se posiciona en el primer lugar absoluto (0.0914):** A pesar de compartir 5 enlaces con $T_1$ y $D_1$, las páginas que apuntan a $C_1$ ($C_2, C_3, C_4, C_5, T_1$) presentan un menor grado de salida promedio, por lo que transfieren una mayor porción de su propio rango hacia $C_1$ ($C_3$ le transfiere el 50 % de su puntaje).
2. **Efecto de Prestigio en $C_3$:** A pesar de haber recibido apenas 3 enlaces brutos (puesto 7 en in-degree), $C_3$ escala hasta la posición 4 global debido a que recibe un hipervínculo directo desde $C_1$, heredando la autoridad concentrada de dicho portal.

---

### 4.3. Experimentos E3 y E4: PageRank Personalizado (Tecnología vs. Deportes)

Se introdujeron dos vectores de reinicio sesgados con el 70 % de la masa de probabilidad asignada a su respectiva categoría:

$$\text{Top 5 Comparativo entre Variantes:}$$

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

### 4.4. Experimento E5: Análisis de Convergencia y Sensibilidad al Parámetro $\alpha$

Se evaluó la recurrencia del Power Method con tolerancia de convergencia $\tau = 10^{-10}$:

| Factor $\alpha$ | Iteraciones Requeridas | Residuo Final $\|\delta\|_1$ |    Composición del Top 5    | Fenómeno Analítico                                                            |
| :-------------: | :--------------------: | :--------------------------: | :-------------------------: | :---------------------------------------------------------------------------- |
|    **0.50**     |         **24**         |    $3.15 \times 10^{-11}$    | $[T_1, C_1, D_1, D_2, T_3]$ | Rápida convergencia; dominado por la estructura local y el reinicio uniforme. |
|    **0.85**     |         **65**         |    $6.13 \times 10^{-11}$    | $[C_1, T_1, D_1, C_3, D_2]$ | Configuración canónica; balance óptimo entre difusión y reinicio.             |
|    **0.95**     |        **101**         |    $8.06 \times 10^{-11}$    | $[C_1, T_1, C_3, D_1, D_2]$ | Crecimiento significativo del esfuerzo iterativo; $C_3$ desplaza a $D_1$.     |
|    **0.99**     |        **128**         |    $8.23 \times 10^{-11}$    | $[C_1, C_3, T_1, D_1, C_6]$ | **Rank Reversal:** $C_3$ asciende al puesto 2 y $C_6$ entra al Top 5.         |

#### Comprobación de la Tasa de Contracción Teórica:

El número de iteraciones computadas satisface estrictamente la cota analítica esperada:
$$k \approx \frac{\log(\tau)}{\log(\alpha)}$$
Al variar $\alpha$ de 0.50 a 0.99, las iteraciones pasan de 24 a 128, lo que representa un incremento computacional del **533 %**. A valores muy cercanos a 1, el caminante aleatorio explora trayectorias de gran profundidad, provocando que subgrafos cerrados como el cultural acumulen la mayor densidad de probabilidad.

---

### 4.5. Experimentos E6, E7 y E8: Sensibilidad ante Perturbaciones Topológicas

|                       Exp.                        | Modificación Efectuada                      | Nodo más Afectado | Cambio Numérico |       ¿Cambia Top 5?        | Top 5 Resultante |
| :-----------------------------------------------: | :------------------------------------------ | :---------------: | :-------------: | :-------------------------: | :--------------- |
|                      **E6**                       | **Añadir 3 enlaces hacia portales:**        |
| $(D_3 \to T_1)$, $(C_6 \to D_1)$, $(T_5 \to C_1)$ | $D_1$                                       |    $+0.011661$    |     **Sí**      | $[C_1, T_1, D_1, D_2, C_3]$ |
|                      **E7**                       | **Quitar 3 enlaces de entrada a portales:** |
| $(T_2 \to T_1)$, $(D_3 \to D_1)$, $(C_3 \to C_1)$ | $C_6$                                       |    $+0.036652$    |     **Sí**      | $[C_6, C_3, T_1, D_2, C_4]$ |
|                      **E8**                       | **Dangling Node (D6 sin salidas):**         |
|   Se eliminan $(D_6 \to D_2)$ y $(D_6 \to D_7)$   | $D_2$                                       |    $-0.015135$    |     **Sí**      | $[C_1, T_1, C_3, D_1, T_3]$ |

- **Efecto de Dangling Node en E8:** Al quedar $D_6$ sin salidas, su columna se sustituye por el vector estocástico uniforme $1/20 = 0.05$. El nodo $D_2$, que recibía el 50 % directo del flujo de $D_6$, experimenta una pérdida drástica de $-0.0151$, provocando su **expulsión inmediata del Top 5** y permitiendo el ingreso de $T_3$.

---

## 5. Guion Estructurado del Video Final (10 Minutos)

El guion ha sido planificado rigurosamente respetando la ventana reglamentaria de $10 \pm 1$ minutos, con intervenciones sustantivas de todos los miembros del equipo:

|    Intervalo     | Bloque Temático                | Contenido Específico y Recursos Visuales                                                                                                                                                                                                |     Responsable      |
| :--------------: | :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------: |
| **0:00 – 1:00**  | **Introducción y Pregunta**    | Título, integrantes y problema de ordenamiento en la Web. Pregunta de investigación, objetivos y alcance de la red de 20 páginas. <br>_Apoyo:_ Diapositiva institucional y gráfico conceptual del problema.                             |  **Luciana Carpio**  |
| **1:00 – 2:00**  | **Modelado y Matriz $P$**      | Del grafo a la matriz estocástica $P$. Tratamiento formal de nodos sin salidas (_dangling nodes_). Parámetro $\alpha$ y vector de reinicio $v$. <br>_Apoyo:_ Visualización de la matriz $P$ y fórmulas estocásticas.                    |  **Sofía Briceño**   |
| **2:00 – 3:00**  | **Tres Formulaciones**         | Demostración analítica de la equivalencia entre punto fijo, sistema lineal $(I - \alpha P)r = (1-\alpha)v$ y vector propio de la matriz Google $G$. Existencia y unicidad. <br>_Apoyo:_ Deducción algebraica en lámina clara.           |  **Sofía Briceño**   |
| **3:00 – 4:00**  | **Convergencia y Cota**        | Análisis del factor de contracción $\alpha$, cota de error $\alpha^k$ y certificado formal mediante residuo $\|r - r^*\|_1 \le \frac{1}{1-\alpha} \|\delta\|_1$. <br>_Apoyo:_ Demostración de Neumann y esquema de contracción.         |  **Sofía Briceño**   |
| **4:00 – 5:30**  | **Verificación Experimental**  | Comprobación del ejemplo de 3 nodos del docente. Contraste numérico: método propio vs. sistema lineal vs. NetworkX. Estocasticidad y residuos. <br>_Apoyo:_ Tabla de convergencia y código Python en pantalla.                          | **Marianela Usnayo** |
| **5:30 – 6:45**  | **Rankings y Personalización** | Conteo de enlaces recibidos vs. PageRank uniforme vs. personalizado (Tecnología y Deportes). Desempate analítico y evolución del Top 5. <br>_Apoyo:_ `fig6_barras_rankings.png` y mapas de red `fig2`, `fig3`, `fig4`.                  |  **Manuel Sialer**   |
| **6:45 – 8:00**  | **Sensibilidad y Redes**       | Comportamiento con $\alpha \in \{0.50, 0.85, 0.95, 0.99\}$, número de iteraciones y _rank reversal_. Perturbaciones de enlaces y caso de _dangling node_. <br>_Apoyo:_ `fig5_convergencia_alpha.png`, `fig7_sensibilidad.png` y `fig8`. |  **Manuel Sialer**   |
| **8:00 – 9:00**  | **Interpretación Matemática**  | Significado de la relevancia estacionaria. Por qué coinciden o difieren las clasificaciones. Supuestos teóricos de la cadena de Markov. <br>_Apoyo:_ Diagrama comparativo de nociones de autoridad.                                     | **Marianela Usnayo** |
| **9:00 – 10:00** | **Conclusiones y Cierre**      | Síntesis de hallazgos, limitaciones del modelo (no semántico), enlaces al repositorio de GitHub y créditos finales. <br>_Apoyo:_ Repositorio proyectado y referencias IEEE.                                                             |  **Luciana Carpio**  |

---

## 6. Registro de Contribuciones Individuales

De conformidad con los criterios de evaluación de la entrega parcial, se certifica el aporte concreto y verificable de cada integrante:

| Integrante                         | Tareas Específicas Realizadas                                                                                                                                                                                                                                                                                                           | Evidencias en Repositorio                                            |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Sofía Catherine Briceño Rosado** | • Deducción de las 3 formulaciones matemáticas.<br>• Demostración analítica de existencia y unicidad con series de Neumann.<br>• Formulación de la cota de contracción $\alpha^k$ y certificado del residuo.<br>• Redacción de la fundamentación teórica del informe.                                                                   | Sección 2 del informe; borradores teóricos en `documentos/`.         |
| **Luciana Carpio Cárdenas**        | • Planteamiento del problema, pregunta central y alcance.<br>• Redacción y estandarización del archivo `README.md` y `requirements.txt`.<br>• Estructuración y gobernanza de directorios del repositorio.<br>• Documentación de las reglas de construcción de la red junto a Manuel.                                                    | `README.md`, `requirements.txt`, `datos/reglas_red.md`.              |
| **Manuel Sialer**                  | • Construcción formal del grafo de 20 nodos y matriz de transición $P$.<br>• Programación de `red_definicion.py`, `pagerank_core.py`, `ejecutar_experimentos.py`.<br>• Ejecución automatizada de los experimentos E1 a E8 y exportación de CSVs.<br>• Desarrollo del script de visualización científica (`generar_visualizaciones.py`). | Scripts en `codigo/`, datos en `resultados/`, figuras en `figuras/`. |
| **Marianela Usnayo Gutierrez**     | • Validación cruzada con el ejemplo de 3 nodos del docente.<br>• Control de calidad de los datos (suma de componentes, no negatividad, residuo $< 10^{-10}$).<br>• Comparación numérica sistemática contra NetworkX y solución lineal.<br>• Planificación y estructuración temporal del guion audiovisual.                              | Tablas de verificación en `resultados/`; Sección 5 del informe.      |

---

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
- **Finalidad:** Apoyo en la automatización de la sintaxis de scripts en Python (estructuración de bucles de graficación con Matplotlib), formato de tablas en Markdown y corrección de estilo de la documentación.
- **Procedimientos de verificación:** Todos los procedimientos matemáticos fueron verificados analíticamente a mano y validados computacionalmente contra bibliotecas estándar (`numpy.linalg.solve`, `networkx.pagerank`). Los resultados numéricos satisfacen estrictamente los criterios de estocasticidad ($\sum r_i = 1$) y residuos de máquina ($< 10^{-10}$). Cada integrante del equipo comprende y asume la responsabilidad intelectual y académica total del contenido aquí presentado.

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
