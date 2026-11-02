# Reglas de Construcción de la Red Simulada de 20 Páginas Web

## Descripción general

La red simula un ecosistema de 20 páginas web distribuidas en tres categorías
temáticas. Cada nodo representa una página web y cada arista dirigida representa
un hipervínculo de una página hacia otra.

## Categorías y nodos

| Categoría    | ID     | Nombre simulado           | Cantidad |
|-------------|--------|---------------------------|----------|
| Tecnología  | T1–T7  | Portal Tech, Blog IA, Reviews, etc. | 7 nodos  |
| Deportes    | D1–D7  | Portal Deportes, Fútbol, Basket, etc. | 7 nodos  |
| Cultura     | C1–C6  | Portal Cultura, Música, Cine, etc. | 6 nodos  |

### Detalle de cada nodo

| ID  | Nombre simulado        | Rol en la red                        |
|-----|------------------------|--------------------------------------|
| T1  | Portal Tecnología      | Hub principal de tecnología          |
| T2  | Blog de IA             | Página especializada                 |
| T3  | Reviews de Gadgets     | Página con enlaces cruzados          |
| T4  | Noticias de Software   | Página periférica                    |
| T5  | Startups               | Página con pocas conexiones          |
| T6  | Programación           | Enlace entre tech y esports          |
| T7  | Hardware               | Página especializada                 |
| D1  | Portal Deportes        | Hub principal de deportes            |
| D2  | Fútbol                 | Página popular dentro de deportes    |
| D3  | Básquetbol             | Página con pocas conexiones          |
| D4  | Olimpiadas             | Enlace cruzado con cultura           |
| D5  | Tenis                  | Página intermedia                    |
| D6  | Fitness                | Página con pocas conexiones          |
| D7  | Esports                | Enlace cruzado con tecnología        |
| C1  | Portal Cultura         | Hub principal de cultura             |
| C2  | Música                 | Página intermedia                    |
| C3  | Cine                   | Enlace con portal                    |
| C4  | Literatura             | Enlace cruzado con deportes          |
| C5  | Museos                 | Página intermedia                    |
| C6  | Teatro                 | Página periférica                    |

## Reglas de construcción

1. **Número de enlaces de salida**: Cada nodo tiene entre 2 y 5 enlaces de salida.
2. **Predominancia intra-categoría**: La mayoría de los enlaces de cada nodo apuntan
   a páginas de su misma categoría (aproximadamente 60–70 % de sus enlaces).
3. **Enlaces inter-categoría**: Entre el 30–40 % de los enlaces conectan categorías
   distintas, simulando que las páginas referencian contenido de otros temas.
4. **Hubs de categoría**: Cada categoría tiene un nodo "portal" (T1, D1, C1)
   que recibe un número elevado de enlaces, simulando un sitio de referencia.
5. **Nodos periféricos**: Algunos nodos (T4, D4, C6) reciben pocos enlaces,
   simulando páginas menos conocidas.
6. **Nodo sin enlaces de salida (dangling node)**: En el experimento de sensibilidad,
   se eliminan todos los enlaces de salida de D6 para analizar el efecto.
   En la red base, D6 sí tiene enlaces de salida.
7. **No hay auto-enlaces**: Ningún nodo enlaza a sí mismo.
8. **Red conectada**: Todos los nodos son alcanzables desde al menos un nodo,
   garantizando que la red no tiene componentes aisladas.

## Procedencia

Los datos son **simulados**. Los nodos y enlaces fueron diseñados manualmente
para producir una estructura que permita observar diferencias entre el conteo
de enlaces recibidos, PageRank uniforme y PageRank personalizado. La red no
representa sitios web reales.

