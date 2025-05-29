"""
Sistema de Optimización de Rutas con Árbol AVL
Autor: Ricardo Rincón
Fecha: 28/04/2025
"""

from collections import deque

class NodoUbicacionArbol:
    """**Clase NodoUbicacionArbol**

    Representa una ubicación dentro del árbol AVL.
    Cada nodo almacena su nombre, altura y rutas disponibles hacia otros nodos.
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.izquierda = None
        self.derecha = None
        self.altura = 1
        self.rutas = set()

class ArbolUbicaciones:
    """**Clase ArbolUbicaciones**

    Implementa un Árbol AVL para gestionar ubicaciones y sus rutas disponibles.
    """

    def __init__(self):
        self.raiz = None

    ## **MÉTODOS AUXILIARES** ##

    def _altura(self, nodo):
        """Calcula la altura de un nodo."""
        return nodo.altura if nodo else 0

    def _balance_factor(self, nodo):
        """Calcula el factor de balance de un nodo."""
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha) if nodo else 0

    def _rotar_derecha(self, y):
        """Realiza una rotación simple a la derecha."""
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        x.altura = 1 + max(self._altura(x.izquierda), self._altura(x.derecha))
        return x

    def _rotar_izquierda(self, x):
        """Realiza una rotación simple a la izquierda."""
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        x.altura = 1 + max(self._altura(x.izquierda), self._altura(x.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        return y

    ## **MÉTODOS DE INSERCIÓN Y BÚSQUEDA** ##

    def insertar(self, nombre: str):
        """Inserta una nueva ubicación en el árbol AVL."""
        self.raiz = self._insertar_recursivo(self.raiz, nombre)

    def _insertar_recursivo(self, nodo, nombre):
        """Inserta recursivamente y balancea el árbol."""
        if not nodo:
            return NodoUbicacionArbol(nombre)

        if nombre < nodo.nombre:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, nombre)
        elif nombre > nodo.nombre:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, nombre)
        else:
            return nodo  # No permite duplicados

        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        balance = self._balance_factor(nodo)

        # Casos de rotaciones
        if balance > 1 and nombre < nodo.izquierda.nombre:
            return self._rotar_derecha(nodo)
        if balance < -1 and nombre > nodo.derecha.nombre:
            return self._rotar_izquierda(nodo)
        if balance > 1 and nombre > nodo.izquierda.nombre:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1 and nombre < nodo.derecha.nombre:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo

    def buscar(self, nombre: str):
        """Busca una ubicación en el árbol AVL."""
        actual = self.raiz
        while actual:
            if nombre == actual.nombre:
                return actual
            elif nombre < actual.nombre:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return None

    ## **MÉTODOS DE RUTAS** ##

    def establecerRuta(self, origen: str, destino: str):
        """Establece una conexión bidireccional entre dos ubicaciones."""
        nodo_origen = self.buscar(origen)
        nodo_destino = self.buscar(destino)
        if nodo_origen and nodo_destino:
            nodo_origen.rutas.add(destino)
            nodo_destino.rutas.add(origen)
            return True
        return False

    def buscarRutaDFS(self, origen: str, destino: str):
        """Busca una ruta usando búsqueda en profundidad (DFS)."""
        nodo_origen = self.buscar(origen)
        if not nodo_origen:
            return f"Origen '{origen}' no encontrado"

        ruta = []
        visitados = set()

        def dfs(actual_nombre):
            if actual_nombre == destino:
                ruta.append(actual_nombre)
                return True
            visitados.add(actual_nombre)
            actual_nodo = self.buscar(actual_nombre)
            if not actual_nodo:
                return False
            for vecino in actual_nodo.rutas:
                if vecino not in visitados:
                    if dfs(vecino):
                        ruta.append(actual_nombre)
                        return True
            return False

        if dfs(origen):
            return list(reversed(ruta))
        else:
            return f"No hay ruta de '{origen}' a '{destino}'"

    def buscarRutaBFS(self, origen: str, destino: str):
        """Busca una ruta usando búsqueda en amplitud (BFS)."""
        nodo_origen = self.buscar(origen)
        if not nodo_origen:
            return f"Origen '{origen}' no encontrado"

        cola = deque()
        visitados = set()
        cola.append((origen, [origen]))

        while cola:
            actual_nombre, ruta = cola.popleft()
            if actual_nombre == destino:
                return ruta

            visitados.add(actual_nombre)
            actual_nodo = self.buscar(actual_nombre)
            if not actual_nodo:
                continue

            for vecino in actual_nodo.rutas:
                if vecino not in visitados:
                    cola.append((vecino, ruta + [vecino]))

        return f"No hay ruta de '{origen}' a '{destino}'"
    
#========================= **IMPLEMENTACIÓN ADICIONAL** ========================= #
    def sugerirRutaMasCercana(self, origen: str):
        """Sugiere la ruta más cercana alfabéticamente desde una ubicación dada."""
        nodo_origen = self.buscar(origen)
        if not nodo_origen:
            return f"Origen '{origen}' no encontrado"
        if nodo_origen.rutas:
            return min(nodo_origen.rutas)
        return "No hay rutas disponibles para sugerir"

    ## **MÉTODO DE RECORRIDO** ##
    def recorridoInOrder(self):
        """Muestra en consola el recorrido in-order del árbol AVL."""
        def in_order(nodo):
            if nodo:
                in_order(nodo.izquierda)
                print(f"{nodo.nombre} → {list(nodo.rutas)}")
                in_order(nodo.derecha)
        in_order(self.raiz)

# ========================= **PRUEBAS** ========================= #

if __name__ == "__main__":
    arbol = ArbolUbicaciones()

    for nombre in ["M", "C", "R", "A", "E", "P", "T"]:
        arbol.insertar(nombre)

    arbol.establecerRuta("M", "C")
    arbol.establecerRuta("M", "R")
    arbol.establecerRuta("C", "A")
    arbol.establecerRuta("C", "E")
    arbol.establecerRuta("R", "P")
    arbol.establecerRuta("R", "T")

    print("\nRecorrido In-Order:")
    arbol.recorridoInOrder()

    print("\nBúsqueda de ruta DFS de 'M' a 'T':", arbol.buscarRutaDFS("M", "T"))
    print("Búsqueda de ruta BFS de 'M' a 'T':", arbol.buscarRutaBFS("M", "T"))

    print("\nSugerencia de ruta más cercana desde 'M':", arbol.sugerirRutaMasCercana("M"))
