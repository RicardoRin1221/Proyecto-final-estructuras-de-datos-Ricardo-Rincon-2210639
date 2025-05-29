## Estructuras de Datos y Análisis de Algoritmos
# Proyecto: Optimizador de Rutas Turísticas

Autor: Ricardo Sneyder Rincón Gamboa-2210639

## Explicación del Problema

Este sistema fue diseñado para enfrentar el desafío de planificar recorridos turísticos óptimos en Monterrey, empleando un modelo matemático avanzado. Se basa en tres restricciones esenciales: todas las rutas deben iniciar y concluir en la Macroplaza, considerada un punto estratégico central; cada recorrido puede incluir hasta cinco destinos adicionales como máximo; y la optimización se realiza en función de distancias reales, calculadas con base en coordenadas geográficas. Para lograr esto, el corazón del sistema adapta el clásico Problema del Viajante (TSP), garantizando una ruta eficiente que minimiza tanto el tiempo como la distancia recorrida.

## Contexto del Grafo Denso

La solución se apoya en un modelo de grafo denso especialmente estructurado. La Macroplaza actúa como nodo obligatorio de inicio y fin, y todas las ubicaciones turísticas están directamente conectadas a ella. Además, cada destino mantiene al menos dos conexiones adicionales con otros puntos turísticos, estableciendo una red sólida y coherente. Estas conexiones se definen con base en una investigación previa que determinó distancias prioritarias, y todas se calculan automáticamente utilizando coordenadas normalizadas y geometría euclidiana, debidamente escalada a kilómetros. Se estableció un límite técnico de seis nodos en total —la Macroplaza más cinco destinos— y las posiciones espaciales están cuidadosamente predefinidas para evitar superposiciones o alineaciones poco realistas.

## Librerías utilizadas

Para implementar esta solución se utilizaron varias bibliotecas clave: `networkx` se encargó del modelado y manipulación del grafo; `matplotlib` fue usada para generar visualizaciones claras y profesionales; `numpy` facilitó los cálculos matemáticos de distancias; `tkinter` brindó una interfaz gráfica accesible e intuitiva; y `collections.defaultdict` permitió un manejo eficiente de las conexiones entre nodos.

## Arquitectura del Sistema

La lógica central está contenida en la clase `GrafoTurismo`, responsable de administrar las ubicaciones turísticas, gestionar las conexiones entre ellas, aplicar las reglas del grafo denso y ejecutar una versión adaptada del algoritmo de Vecino Más Cercano para resolver el TSP. Esta clase también se encarga del cálculo de las posiciones espaciales necesarias para las visualizaciones, valida el número máximo de destinos permitidos, y garantiza la conexión de cualquier nodo aislado mediante la Macroplaza. Las distancias entre los puntos se calculan en tiempo real utilizando coordenadas reales y se manejan hasta 18 conexiones predefinidas, asegurando siempre una ruta circular que parte y retorna al punto central.

La experiencia de usuario se gestiona a través de la clase `InterfazTurismo`, que permite seleccionar destinos turísticos mediante listas interactivas, gestionar las ubicaciones seleccionadas, visualizar mapas del recorrido y consultar resultados detallados. El usuario puede elegir hasta cinco destinos de una lista de ocho predefinidos, tras lo cual el sistema establece automáticamente las conexiones necesarias. Al solicitar la ruta óptima, se construye el grafo con base en conexiones reales, se aplica el algoritmo TSP adaptado y se presentan los resultados tanto en formato textual como gráfico.

## Interfaz y Visualización

El diseño de la interfaz está dividido en cuatro secciones: una lista con los destinos disponibles, un panel que muestra los destinos seleccionados junto a la Macroplaza, un panel central con los controles para añadir o eliminar ubicaciones, visualizar el mapa y calcular la ruta óptima, y finalmente un área de resultados donde se muestra la secuencia de visita y la distancia total del recorrido. Al activar la visualización, se genera un mapa con nodos de distintos colores y tamaños según su importancia (por ejemplo, dorado para la Macroplaza y azul claro para los demás destinos), líneas grises para las conexiones generales, y un trazo rojo y más grueso para la ruta óptima. Las distancias están etiquetadas, diferenciando claramente las que corresponden a la ruta principal.

El sistema también valida que no se seleccionen más de cinco destinos, impide que se elimine la Macroplaza y muestra mensajes contextuales si se intenta realizar alguna acción inválida. Toda la visualización es responsiva, clara y pensada para ofrecer una experiencia fluida. En conjunto, este proyecto representa una solución integral e inteligente para la planificación turística en Monterrey, al combinar modelos algorítmicos sofisticados con una interfaz sencilla y amigable.