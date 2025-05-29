## Estructuras de Datos y Análisis de Algoritmos
# Proyecto: Optimizador de Rutas Turísticas

Autor: Ricardo Sneyder Rincón Gamboa-2210639

## Resumen del Problema

**Monterrey Tours Express** es una propuesta innovadora pensada para facilitar la planificación de recorridos turísticos por la ciudad de Monterrey. Su objetivo principal es ayudar tanto a visitantes como a guías a explorar los lugares más emblemáticos de la ciudad de forma eficiente, reduciendo al mínimo las distancias recorridas y potenciando al máximo la experiencia cultural. Uno de los problemas más comunes que enfrentan los turistas es la pérdida de tiempo al intentar organizar por su cuenta rutas que, en muchos casos, resultan poco prácticas o innecesariamente largas. Este sistema resuelve ese inconveniente calculando automáticamente el mejor itinerario posible, siempre partiendo y concluyendo en la icónica Macroplaza, y permitiendo al usuario elegir hasta cinco destinos que se adapten a sus intereses.

## Etapas de Desarrollo

Primera etapa: se optó por una implementación básica utilizando **listas enlazadas**. Esta estructura permitía gestionar ubicaciones de manera lineal, conectando puntos de interés uno tras otro. Aunque funcionaba como una primera aproximación, presentaba serias limitaciones en términos de eficiencia. Las operaciones de búsqueda o inserción eran lentas (O(n)) y requerían ordenamientos manuales (O(n²)), lo que dificultaba ofrecer una experiencia ágil a los usuarios.

Segunda etapa: se implementó un **Árbol AVL auto-balanceado**. Este cambio mejoró notablemente el rendimiento, ya que tanto las inserciones como las búsquedas pasaron a realizarse en tiempo logarítmico (O(log n)). Además, se añadieron funcionalidades como la sugerencia automática de rutas similares desde un punto de vista alfabético y una gestión mucho más rápida y ordenada de las rutas posibles, utilizando recorridos DFS y BFS. Esta etapa sentó las bases para una solución escalable, capaz de adaptarse a redes de logística más complejas.

Tercera etapa: implementación de una **plataforma basada en un grafo denso**. En este modelo, la Macroplaza actúa como nodo central obligatorio y cada destino se conecta estratégicamente con al menos tres ubicaciones, una de ellas siempre siendo la Macroplaza. Las conexiones se definen según distancias reales, calculadas a partir de coordenadas geográficas. Este enfoque permite aplicar algoritmos de optimización como el TSP (Problema del Viajante) de forma mejorada, asegurando recorridos eficientes y visualmente claros. La plataforma también incluye una visualización interactiva de las rutas y mantiene el límite de cinco destinos seleccionables, buscando siempre ofrecer una experiencia realista y sencilla para el usuario, sin sacrificar velocidad ni precisión en los resultados.
