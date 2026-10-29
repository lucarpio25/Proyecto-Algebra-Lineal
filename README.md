# Proyecto-Algebra-Lineal
# Análisis de relevancia de páginas web mediante PageRank y PageRank personalizado

## Integrantes del equipo

- Luciana Carpio
- Sofía Briceño
- Manuel Sialer
- Marianela Usnayo

## 1. Tema del proyecto

El proyecto aplica PageRank para analizar la importancia de páginas web dentro de una red de enlaces. Este algoritmo considera tanto los enlaces que recibe una página como la importancia de las páginas que la enlazan. Además, se utilizará PageRank personalizado para estudiar cómo cambia la relevancia al incorporar preferencias por determinados temas.

## 2. Planteamiento del problema

Las páginas web se conectan mediante enlaces que permiten pasar de una página a otra. Estas conexiones forman una red en la que algunas páginas reciben más enlaces que otras. Por ende, una forma sencilla de clasificarlas consiste en contar cuántos enlaces recibe cada una; sin embargo, esta medida no distingue la importancia de las páginas de origen. Una página enlazada por pocas páginas relevantes podría tener una posición más importante dentro de la red que otra que recibe numerosos enlaces de páginas con poca relevancia.

PageRank permite estudiar esta diferencia al asignar puntuaciones que dependen tanto de los enlaces recibidos como de la importancia de quienes los proporcionan. Así, la relevancia de cada página depende de la estructura completa de la red. Esto plantea la necesidad de comparar sus resultados con el conteo de enlaces para identificar cuándo coinciden las clasificaciones y cuándo aparecen diferencias.

Además, la relevancia puede variar según los intereses del usuario. Una clasificación general considera un reinicio uniforme entre todas las páginas, mientras que PageRank personalizado permite favorecer páginas relacionadas con un tema determinado. En una red que contiene páginas sobre tecnología, deportes y cultura, resulta pertinente analizar cómo cambia la clasificación al introducir preferencias temáticas y si estas también afectan a páginas de otras categorías a través de sus conexiones.

Los resultados también dependen de las decisiones del modelo y de la estructura de la red. Modificar el parámetro α, que representa la probabilidad de seguir un enlace en lugar de reiniciar la navegación, puede cambiar las puntuaciones y el número de iteraciones necesarias para calcularlas. Asimismo, añadir o eliminar enlaces puede alterar las posiciones del ranking e incluso dejar páginas sin enlaces de salida, situación que requiere una regla explícita de tratamiento.

Por ello, el proyecto estudiará una red simulada de 20 páginas web para comparar el número de enlaces recibidos, PageRank uniforme y PageRank personalizado. Se evaluarán los cambios en las puntuaciones y en las primeras cinco posiciones ante modificaciones de los enlaces y del parámetro α. También se verificará la precisión de los cálculos mediante el residuo y la comparación con otros procedimientos de solución. El propósito es comprender qué noción de relevancia produce cada clasificación y cuáles son sus limitaciones, sin interpretar los puntajes como una garantía de calidad o veracidad del contenido.

## 3. Pregunta de investigación

¿Cómo cambia la clasificación de relevancia de una red de páginas web al comparar el número de enlaces recibidos, PageRank uniforme y PageRank personalizado, y qué sensibilidad presenta ante cambios en las conexiones y en el parámetro de seguimiento de enlaces?

## 4. Objetivo general

Implementar y verificar PageRank uniforme y personalizado en una red simulada de páginas web, comparando sus clasificaciones con el número de enlaces recibidos y evaluando los cambios en las puntuaciones, las primeras cinco posiciones y la convergencia al modificar las preferencias, las conexiones y el parámetro de seguimiento de enlaces.

## 5. Alcance del proyecto

El proyecto comprenderá una red dirigida y simulada de 20 páginas web, distribuidas en tres categorías: tecnología, deportes y cultura. Cada nodo representará una página y cada enlace dirigido indicará que una página contiene un vínculo hacia otra. Se documentarán las reglas utilizadas para construir la red; no será necesario crear sitios web reales.

El trabajo incluirá:

- La reproducción del ejemplo de tres nodos proporcionado por el docente.
- La construcción de la matriz de transición y la definición del tratamiento de páginas sin enlaces de salida.
- Una implementación propia de PageRank en Python, contrastada con la solución directa del sistema lineal y con NetworkX.
- La comparación del número de enlaces recibidos, PageRank uniforme y dos versiones personalizadas: una con preferencia por tecnología y otra por deportes.
- La evaluación de los valores de α de 0.50, 0.85, 0.95 y 0.99, donde α representa la probabilidad de seguir un enlace.
- El análisis del residuo, el número de iteraciones y los cambios en las primeras cinco posiciones.
- La modificación de enlaces seleccionados, incluyendo un caso donde una página quede sin enlaces de salida.
- La presentación de gráficos de la red con tamaños de nodo proporcionales a sus puntuaciones y tablas reproducibles de resultados.

El estudio se limitará a la red construida. Sus resultados describirán la relevancia según la estructura de enlaces y las preferencias definidas, sin evaluar la calidad o veracidad del contenido de las páginas ni generalizar las conclusiones a toda la web.
