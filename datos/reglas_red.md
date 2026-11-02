# Reglas de construcción de la red simulada

## Descripción general

La red base contiene 20 páginas web ficticias y 56 enlaces dirigidos, organizados en tres categorías: tecnología, deportes y cultura.

Cada nodo representa una página. Una conexión A → B significa que la página A contiene un enlace hacia la página B.

Todos los enlaces tienen el mismo peso.

## Categorías y nodos

| Categoría | Identificadores | Cantidad |
|---|---|---:|
| Tecnología | T1–T7 | 7 |
| Deportes | D1–D7 | 7 |
| Cultura | C1–C6 | 6 |
| **Total** | | **20** |

### Detalle de cada nodo

| ID | Nombre simulado | Categoría |
|---|---|---|
| T1 | Portal Tecnología | Tecnología |
| T2 | Blog de IA | Tecnología |
| T3 | Reviews de Gadgets | Tecnología |
| T4 | Noticias de Software | Tecnología |
| T5 | Startups | Tecnología |
| T6 | Programación | Tecnología |
| T7 | Hardware | Tecnología |
| D1 | Portal Deportes | Deportes |
| D2 | Fútbol | Deportes |
| D3 | Básquetbol | Deportes |
| D4 | Olimpiadas | Deportes |
| D5 | Tenis | Deportes |
| D6 | Fitness | Deportes |
| D7 | Esports | Deportes |
| C1 | Portal Cultura | Cultura |
| C2 | Música | Cultura |
| C3 | Cine | Cultura |
| C4 | Literatura | Cultura |
| C5 | Museos | Cultura |
| C6 | Teatro | Cultura |

## Reglas de la red base

1. **Enlaces de salida:** cada página tiene entre 2 y 5 enlaces de salida.
2. **Enlaces dentro de categorías:** 47 de los 56 enlaces conectan páginas de la misma categoría, aproximadamente el 83.9 %.
3. **Enlaces entre categorías:** 9 de los 56 enlaces conectan páginas de categorías distintas, aproximadamente el 16.1 %.
4. **Portales:** T1, D1 y C1 representan portales temáticos y reciben 5 enlaces cada uno.
5. **Sin autoenlaces:** ninguna página de la red base enlaza hacia sí misma.
6. **Sin duplicados:** cada conexión dirigida entre dos páginas aparece una sola vez.
7. **Sin páginas sin salida en la red base:** todas tienen al menos dos enlaces de salida.

Los porcentajes describen el conjunto de la red, no la proporción de enlaces de cada página individual.

### Enlaces entre categorías

- T1 → D1
- T1 → C1
- T6 → D7
- D1 → T1
- D4 → C4
- D7 → T6
- D7 → C2
- C2 → D2
- C5 → T3

La lista completa de los 56 enlaces está definida en `codigo/red_definicion.py`.

## Construcción de la matriz de transición

Las columnas de P representan páginas de origen y las filas representan páginas de destino.

Si una página tiene d enlaces de salida, cada destino recibe una probabilidad de 1/d. Los destinos sin enlace desde esa página reciben probabilidad cero.

De esta manera, las entradas de P son no negativas y cada columna suma uno.

## Tratamiento de páginas sin enlaces de salida

En el experimento E8 se eliminan las conexiones D6 → D2 y D6 → D7. Como resultado, D6 queda sin salidas.

Su columna en P se reemplaza por una distribución uniforme: cada una de las 20 páginas, incluida D6, recibe probabilidad 1/20 = 0.05.

Esta corrección es una regla matemática de redistribución. No añade enlaces reales a la lista del grafo.

La misma regla se utiliza en la implementación propia y en NetworkX, tanto para reinicio uniforme como personalizado.

## Preferencias de reinicio

Se utilizan tres distribuciones:

- **Uniforme:** cada página recibe probabilidad 1/20 = 0.05.
- **Tecnología:** el 70 % se reparte entre T1–T7 y el 30 % entre las otras trece páginas.
- **Deportes:** el 70 % se reparte entre D1–D7 y el 30 % entre las otras trece páginas.

En las variantes personalizadas, cada página favorita recibe 0.70/7 = 0.10 y cada página restante recibe 0.30/13.

La distribución uniforme para páginas sin salida se mantiene fija al cambiar las preferencias de reinicio.

## Modificaciones experimentales

Cada modificación parte de una copia independiente de la red base:

| Experimento | Modificación |
|---|---|
| E6 | Añadir D3 → T1, C6 → D1 y T5 → C1. |
| E7 | Eliminar T2 → T1, D3 → D1 y C3 → C1. |
| E8 | Eliminar todas las salidas de D6: D6 → D2 y D6 → D7. |

Después de cada modificación se reconstruye P para actualizar las probabilidades y conservar la suma de uno por columna.

## Procedencia y limitaciones

Los nodos y enlaces fueron diseñados manualmente con fines académicos. La red no representa sitios reales ni conexiones extraídas de internet.

Los resultados permiten comparar formas de medir relevancia dentro de esta simulación. No evalúan la calidad o veracidad de contenidos ni representan un ranking de toda la web.
