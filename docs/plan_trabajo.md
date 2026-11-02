## Cronograma y distribución de responsabilidades

El siguiente cronograma organiza las actividades del proyecto durante las semanas 12, 13 y 14. En la tabla, las celdas marcadas (■) indican los días asignados a cada actividad.

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


## Distribución de responsabilidades

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
