
# 6. Fundamentos matemáticos del proyecto

El algoritmo PageRank utiliza conceptos de álgebra lineal para determinar la relevancia relativa de páginas web a partir de su estructura de enlaces. En este proyecto, se emplearán matrices de transición, sistemas de ecuaciones lineales, valores y vectores propios, y convergencia de métodos iterativos.

## 6.1. Matrices de transición

La red de páginas web se representará mediante una matriz de transición $P$, que describe las probabilidades de desplazamiento entre páginas al seguir sus enlaces. Para las 20 páginas simuladas, la matriz tendrá 20 filas y 20 columnas. Cada entrada $P_{ij}$ indicará la probabilidad de pasar desde la página $j$ hacia la página $i$. Por tanto, las columnas representan las páginas de origen y las filas, las páginas de destino.

Se considerarán enlaces de igual peso. Si una página tiene $d_j$ enlaces de salida, la probabilidad de seguir cada uno será $1/d_j$. Por ejemplo, si la página A enlaza únicamente a B y C, las probabilidades de pasar de A hacia esas páginas serán $1/2$ y $1/2$. Los destinos que no estén enlazados desde A tendrán probabilidad cero.

La matriz será **estocástica por columnas**: sus entradas serán no negativas y cada columna sumará uno, porque representa todas las posibilidades de destino desde una página. Cuando una página no tenga enlaces de salida, se reemplazará su columna por una distribución uniforme, asignando una probabilidad de $1/20$ a cada página. Esta regla se mantendrá tanto en PageRank uniforme como en el personalizado.

Si un vector $x$ contiene la distribución actual de probabilidad entre las páginas, el producto $Px$ representa la distribución después de seguir un enlace, aplicando la regla de redistribución en las páginas sin salida. Así, la matriz permite transformar la estructura de conexiones en una operación matemática que se utilizará para actualizar las puntuaciones.

## 6.2. Sistemas de ecuaciones lineales

Las puntuaciones de PageRank se organizan en un vector $r$, que contiene un valor por cada página de la red. Cada puntuación representa la proporción de visitas que recibiría esa página a largo plazo bajo las reglas de navegación del modelo. Los valores son no negativos y suman uno. Por ejemplo, una puntuación de 0.20 representa el 20 % de las visitas a largo plazo; no significa que la página tenga un 20 % de calidad.

El vector PageRank se determina mediante la ecuación:

$$
r = \alpha Pr + (1-\alpha)v
$$

Donde:

- $r$ es el vector de relevancia.
- $P$ es la matriz de transición.
- $\alpha$ es el parámetro de seguimiento de enlaces.
- $v$ es el vector de reinicio.

El modelo combina dos formas de navegación: seguir uno de los enlaces de la página actual o reiniciar la navegación en una página elegida según una distribución de probabilidades. El parámetro $\alpha$ determina la probabilidad de seguir un enlace, mientras que $1-\alpha$ indica la probabilidad de reiniciar. Se utilizarán valores de alfa mayores que cero y menores que uno. Por ejemplo, con $\alpha=0.85$, existe un 85 % de probabilidad de seguir un enlace y un 15 % de reiniciar.

Al reorganizar la expresión se obtiene:

$$
(I-\alpha P)r = (1-\alpha)v
$$

Donde $I$ representa la matriz identidad de dimensión $20 \times 20$.

Este sistema permitirá calcular directamente las puntuaciones de PageRank y contrastarlas con las obtenidas mediante métodos iterativos y la biblioteca NetworkX.

El vector $v$, denominado **vector de reinicio**, determina la probabilidad de elegir cada página cuando ocurre un reinicio. Sus componentes son no negativas y suman uno.

En PageRank uniforme, las 20 páginas tendrán la misma probabilidad de reinicio:

$$
v_i = \frac{1}{20} = 0.05
$$

En PageRank personalizado, se asignan probabilidades que favorezcan las páginas de tecnología o de deportes, según la preferencia estudiada.

El reinicio permite continuar la navegación sin depender exclusivamente de las conexiones existentes. Modificar el vector $v$ cambia las preferencias del modelo y puede modificar las puntuaciones finales; no equivale a cambiar únicamente las puntuaciones iniciales del cálculo.

## 6.3. Valores y vectores propios

Un vector propio de una matriz es un vector distinto de cero que, al multiplicarse por esa matriz, queda multiplicado por un número llamado valor propio. Esta relación se expresa como:

$$
Gr = \lambda r
$$

Si $\lambda=1$, el vector permanece sin cambios después de la multiplicación. Esta es la propiedad que interesa en PageRank: las puntuaciones finales deben mantenerse iguales al aplicar nuevamente las reglas de navegación.

Los valores y vectores propios permiten comprender el comportamiento estacionario del algoritmo PageRank.

Se define la **matriz Google** como:

$$
G = \alpha P + (1-\alpha)v\mathbf{1}^{T}
$$

En esta expresión:

- $P$ es la matriz de transición.
- $\alpha$ es la probabilidad de seguir un enlace.
- $v$ es el vector de reinicio.
- $\mathbf{1}^{T}$ representa un vector fila formado por unos.

El producto $v\mathbf{1}^{T}$ genera una matriz cuyas columnas son copias de $v$, de modo que la distribución de reinicio puede aplicarse desde cualquier página de origen.

La matriz $G$ combina el seguimiento de enlaces con los reinicios. Como las puntuaciones del vector $r$ suman uno, multiplicar $G$ por $r$ equivale a realizar una actualización completa de PageRank.

En el equilibrio se cumple:

$$
Gr = r
$$

Por consiguiente, el vector PageRank corresponde a un vector propio de la matriz $G$, asociado al valor propio $\lambda=1$, normalizado para que sus componentes sumen uno.

Esta propiedad permite interpretar las puntuaciones como una **distribución estacionaria de probabilidad**, en la que la relevancia de las páginas permanece estable después de aplicar nuevamente la matriz de transición modificada.

## 6.4. Convergencia de métodos iterativos

Además de resolver el sistema lineal, PageRank puede calcularse mediante actualizaciones sucesivas de las puntuaciones.

Se parte de un vector inicial $x^{(0)}$ con componentes no negativas que suman uno. En este proyecto, se utilizará inicialmente una distribución uniforme, asignando una puntuación de $1/20$ a cada página.

En cada iteración se aplica la siguiente regla:

$$
x^{(k+1)} = \alpha Px^{(k)} + (1-\alpha)v
$$

Aquí, $x^{(k)}$ representa las puntuaciones de la iteración actual y $x^{(k+1)}$, las de la siguiente. Estos índices indican el número de actualización; no representan potencias.

La matriz $P$, el parámetro $\alpha$ y el vector de reinicio $v$ se mantienen fijos durante cada ejecución.

La **convergencia** significa que estas aproximaciones se acercan al vector de equilibrio $r$.

Como $P$ es estocástica por columnas y $\alpha$ está entre cero y uno, la actualización es una contracción: la distancia al equilibrio, medida con la norma uno, se reduce en cada paso por un factor no mayor que $\alpha$.

Esta propiedad garantiza la convergencia desde cualquier distribución inicial.

En el proyecto, se analizará la convergencia para los valores:

$$
\alpha \in \{0.50,\ 0.85,\ 0.95,\ 0.99\}
$$

Para decidir cuándo detener el procedimiento, se calculará el **residuo** de la aproximación actual $x$ usando la norma uno:

$$
\|x-\alpha Px-(1-\alpha)v\|_1
$$

La norma uno se calcula sumando los valores absolutos de las componentes del vector.

El residuo mide cuánto cambia la aproximación actual con su siguiente actualización al aplicar nuevamente la regla de PageRank.

Para certificar su precisión, se utilizará la siguiente cota:

$$
\|x-r\|_1 \leq
\frac{\|x-\alpha Px-(1-\alpha)v\|_1}{1-\alpha}
$$

Esta expresión establece un **error máximo garantizado**, calculado como:

$$
\text{Error máximo garantizado} =
\frac{\text{Residuo}}{1-\alpha}
$$

Esto significa que la distancia entre la aproximación actual y la solución de equilibrio, medida con la norma uno, no supera ese cociente.

El algoritmo se detendrá cuando este valor sea menor o igual que la tolerancia de error establecida.

También se fijará un máximo de iteraciones. Si se alcanza ese máximo sin cumplir el criterio de parada, se informará que no se logró certificar la precisión requerida.

## 6.5. Aplicación de los conceptos al proyecto

Los conceptos matemáticos descritos se utilizarán de manera conjunta para calcular, interpretar y verificar la relevancia de las páginas web.

Primero, se construirá la matriz de transición $P$ a partir de los enlaces de la red simulada. Luego, se definirán el parámetro $\alpha$ y el vector de reinicio $v$ para representar la navegación uniforme o las preferencias por tecnología y deportes.

Las puntuaciones de equilibrio se calcularán mediante dos procedimientos: la solución del sistema lineal y la actualización iterativa.

Ambos buscan el mismo vector PageRank, que también puede interpretarse como un vector propio de la matriz Google asociado al valor propio uno.

Se contrastarán los resultados de ambos procedimientos con los obtenidos mediante NetworkX.

La precisión de las aproximaciones se comprobará mediante el residuo y su certificado de error. Además, se verificará que las puntuaciones sean no negativas y que sumen uno, dentro de la precisión numérica establecida.

Finalmente, se compararán las puntuaciones y los rankings al modificar las preferencias, el parámetro $\alpha$ y algunos enlaces.

Se distinguirán los cambios en los valores de las puntuaciones de los cambios en el orden de las páginas: dos páginas con puntuaciones muy cercanas pueden intercambiar posiciones aunque sus valores cambien poco.

Estos experimentos permitirán interpretar los resultados y reconocer las limitaciones del modelo.
