"""
**Sistema de Optimización de Rutas con Listas Enlazadas**
Autor: [Ricardo Rincón]
Fecha: [16/03/2025]

"""
import time

class NodoUbicacion:
    """**Clase NodoUbicacion**
    
    Representa una ubicación dentro del sistema de rutas.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None  # Apunta al siguiente nodo en la lista
        self.rutas = []        # Lista de nombres de ubicaciones alcanzables

    def agregarRuta(self, nombreDestino):
        """**Método agregarRuta**
        
        Agrega un destino a las rutas disponibles desde esta ubicación.
        """
        if nombreDestino not in self.rutas:
            self.rutas.append(nombreDestino)

class ListaUbicaciones:
    """**Clase ListaUbicaciones**
    
    Lista enlazada simple para administrar ubicaciones y sus rutas.
    """

    def __init__(self):
        self.cabeza = None  # Inicio de la lista enlazada

    ## **MÉTODOS REQUERIDOS** ##
    
    def estaVacia(self):
        """**Método estaVacia**
        
        Verifica si la lista está vacía.
        
        Returns:
            bool: True si la lista está vacía, False en caso contrario.
        """
        return self.cabeza is None
        
    def contar(self):
        """**Método contar**
        
        Cuenta la cantidad de elementos existentes en la lista.
        
        Returns:
            int: Número de elementos en la lista.
        """
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador
        
    def imprimir(self):
        """**Método imprimir**
        
        Imprime en pantalla los elementos de la lista.
        """
        if self.estaVacia():
            print("La lista está vacía")
            return
            
        actual = self.cabeza
        while actual:
            print(f"Ubicación: {actual.nombre}")
            actual = actual.siguiente
    
    def bubbleSort(self):
        """**Método bubbleSort**
        
        Ordena los elementos de la lista utilizando el algoritmo Bubble Sort.
        """
        if self.estaVacia() or self.cabeza.siguiente is None:
            return  # Lista vacía o con un solo elemento ya está ordenada
            
        ordenado = False
        while not ordenado:
            ordenado = True
            actual = self.cabeza
            
            while actual.siguiente:
                if actual.nombre > actual.siguiente.nombre:
                    # Intercambia los valores (no los nodos)
                    actual.nombre, actual.siguiente.nombre = actual.siguiente.nombre, actual.nombre
                    # También intercambiamos las rutas
                    actual.rutas, actual.siguiente.rutas = actual.siguiente.rutas, actual.rutas
                    ordenado = False
                actual = actual.siguiente
    
    def buscarOrdenado(self, nombre):
        """**Método buscarOrdenado**
        
        Busca un elemento en la lista después de ordenarla usando Bubble Sort.
        
        Args:
            nombre (str): Nombre de la ubicación a buscar.
            
        Returns:
            NodoUbicacion o None: El nodo encontrado o None si no existe.
        """
        # Primero ordenamos la lista
        self.bubbleSort()
        
        # Ahora realizamos la búsqueda en la lista ordenada
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre:
                return actual
            elif actual.nombre > nombre:  # Como está ordenada, podemos parar antes
                return None
            actual = actual.siguiente
        return None

    ## **MÉTODOS DE INSERCIÓN** ##

    def agregarInicio(self, nombre):
        """**Método agregarInicio**
        
        Agrega una nueva ubicación al inicio de la lista.
        """
        nuevo = NodoUbicacion(nombre)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        return nuevo

    def agregarFinal(self, nombre):
        """**Método agregarFinal**
        
        Agrega una nueva ubicación al final de la lista.
        """
        nuevo = NodoUbicacion(nombre)
        if not self.cabeza:
            self.cabeza = nuevo
            return nuevo
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo
        return nuevo

    def insertarAntes(self, referencia, nombre):
        """**Método insertarAntes**
        
        Inserta un nodo antes de una ubicación de referencia.
        """
        if not self.cabeza or self.cabeza.nombre == referencia:
            return self.agregarInicio(nombre)
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.nombre != referencia:
            actual = actual.siguiente
        if actual.siguiente:
            nuevo = NodoUbicacion(nombre)
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
            return nuevo
        return None

    def insertarDespues(self, referencia, nombre):
        """**Método insertarDespues**
        
        Inserta un nodo después de una ubicación de referencia.
        """
        actual = self.buscar(referencia)
        if actual:
            nuevo = NodoUbicacion(nombre)
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
            return nuevo
        return None

    ## **MÉTODOS DE MANIPULACIÓN** ##

    def buscar(self, nombre):
        """**Método buscar**
        
        Busca una ubicación por su nombre y devuelve el nodo correspondiente.
        """
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def eliminar(self, nombre):
        """**Método eliminar**
        
        Elimina una ubicación de la lista enlazada y actualiza las rutas.
        """
        if not self.cabeza:
            return False
            
        # Si el nodo a eliminar es la cabeza
        if self.cabeza.nombre == nombre:
            self.cabeza = self.cabeza.siguiente
            # Actualizar rutas en todos los nodos que apuntan al eliminado
            self._eliminarRutasHacia(nombre)
            return True
            
        # Buscar el nodo anterior al que queremos eliminar
        actual = self.cabeza
        while actual.siguiente and actual.siguiente.nombre != nombre:
            actual = actual.siguiente
            
        # Si se encontró el nodo
        if actual.siguiente:
            actual.siguiente = actual.siguiente.siguiente
            # Actualizar rutas en todos los nodos que apuntan al eliminado
            self._eliminarRutasHacia(nombre)
            return True
            
        return False
        
    def _eliminarRutasHacia(self, nombre):
        """**Método _eliminarRutasHacia**
        
        Elimina todas las rutas que apuntan hacia un nombre específico.
        """
        actual = self.cabeza
        while actual:
            if nombre in actual.rutas:
                actual.rutas.remove(nombre)
            actual = actual.siguiente

    ## **MÉTODOS DE CONEXIÓN DE RUTAS** ##

    def establecerRuta(self, origen, destino, bidireccional=True):
        """**Método establecerRuta**
        
        Establece una ruta entre dos ubicaciones.
        
        Args:
            origen (str): Nombre de la ubicación de origen
            destino (str): Nombre de la ubicación de destino
            bidireccional (bool): Si es True, crea ruta en ambos sentidos
        """
        nodo_origen = self.buscar(origen)
        nodo_destino = self.buscar(destino)
        
        if nodo_origen and nodo_destino:
            nodo_origen.agregarRuta(destino)
            if bidireccional:
                nodo_destino.agregarRuta(origen)
            return True
        return False

    ## **MÉTODOS DE BÚSQUEDA DE RUTAS** ##

    def buscarRuta(self, origen, destino):
        """**Método buscarRuta**
        
        Busca una ruta entre dos ubicaciones utilizando búsqueda secuencial.
        
        Args:
            origen (str): Nombre de la ubicación de origen
            destino (str): Nombre de la ubicación de destino
            
        Returns:
            list o str: Lista con la ruta encontrada o mensaje si no hay ruta
        """
        # Verificar que ambas ubicaciones existen
        if not self.buscar(origen) or not self.buscar(destino):
            return "Al menos una de las ubicaciones no existe"
        
        # Si origen y destino son el mismo
        if origen == destino:
            return [origen]
        
        # Lista para almacenar todas las posibles rutas
        todas_rutas = []
        
        # Función para explorar rutas desde un punto dado
        def explorar_ruta(ruta_actual):
            # Último nodo en la ruta actual
            ultimo = ruta_actual[-1]
            
            # Si llegamos al destino, agregamos esta ruta a las encontradas
            if ultimo == destino:
                todas_rutas.append(list(ruta_actual))
                return
            
            # Obtenemos el nodo para acceder a sus conexiones
            nodo = self.buscar(ultimo)
            
            # Exploramos todas las conexiones que no creen ciclos
            for siguiente in nodo.rutas:
                if siguiente not in ruta_actual:  # Evitamos ciclos
                    ruta_actual.append(siguiente)
                    explorar_ruta(ruta_actual)
                    ruta_actual.pop()  # Backtracking
        
        # Comenzamos la exploración desde el origen
        explorar_ruta([origen])
        
        # Si no encontramos rutas
        if not todas_rutas:
            return "No hay ruta disponible"
        
        # Encontramos la ruta más corta
        ruta_mas_corta = min(todas_rutas, key=len)
        return ruta_mas_corta

    ## **MÉTODO PARA MOSTRAR** ##

    def mostrar(self):
        """**Método mostrar**
        
        Muestra la lista de ubicaciones y sus rutas disponibles.
        """
        actual = self.cabeza
        while actual:
            print(f"{actual.nombre} → Rutas disponibles hacia: {actual.rutas}")
            actual = actual.siguiente

# ========================= **PRUEBAS** ========================= #

if __name__ == "__main__":
    lista = ListaUbicaciones()
    
    # Verificar si la lista está vacía
    print("\n¿La lista está vacía?", "Sí" if lista.estaVacia() else "No")
    
    # Agregar ubicaciones
    a = lista.agregarInicio("A")
    b = lista.agregarFinal("B")
    c = lista.agregarFinal("C")
    d = lista.agregarFinal("D")
    x = lista.insertarAntes("C", "X")
    y = lista.insertarDespues("B", "Y")
    
    # Verificar si la lista está vacía después de agregar elementos
    print("\n¿La lista está vacía después de agregar elementos?", "Sí" if lista.estaVacia() else "No")
    
    # Contar elementos
    print("\nCantidad de elementos en la lista:", lista.contar())
    
    # Imprimir elementos
    print("\nElementos de la lista:")
    lista.imprimir()
    
    # Crear rutas
    lista.establecerRuta("A", "B")
    lista.establecerRuta("B", "Y")
    lista.establecerRuta("Y", "X")
    lista.establecerRuta("X", "C")
    lista.establecerRuta("C", "D")
    
    # Mostrar ubicaciones y rutas
    print("\nLista de ubicaciones y rutas:")
    lista.mostrar()
    
    # Buscar una ubicación
    print("\nBuscando 'C':", lista.buscar("C").nombre if lista.buscar("C") else "No encontrado")
    
    # Buscar una ubicación usando el método ordenado
    print("\nBuscando 'X' usando búsqueda ordenada:", 
          lista.buscarOrdenado("X").nombre if lista.buscarOrdenado("X") else "No encontrado")
    
    # Buscar rutas
    print("\nRuta de A a D:", lista.buscarRuta("A", "D"))
    print("Ruta de A a X:", lista.buscarRuta("A", "X"))
    
    # Eliminar una ubicación y verificar rutas
    print("\nEliminando 'Y'...")
    lista.eliminar("Y")
    lista.mostrar()
    
    # Contar elementos después de eliminar
    print("\nCantidad de elementos después de eliminar:", lista.contar())
    
    # Buscar ruta tras eliminar un nodo
    print("\nRuta de A a D después de eliminar Y:", lista.buscarRuta("A", "D"))
    
    # Medir tiempo de ejecución
    inicio_tiempo = time.time()
    ruta = lista.buscarRuta("A", "C")
    fin_tiempo = time.time()
    print(f"\nTiempo de búsqueda: {fin_tiempo - inicio_tiempo:.6f} segundos")
