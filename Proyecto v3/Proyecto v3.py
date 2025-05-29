"""Plataforma de Monterrey Tours Express - Versión con Red Densa"""
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

class GrafoTurismo:
    """Implementa un grafo con Macroplaza como punto de salida y límite de ubicaciones."""
    def __init__(self):
        self.nodos = set(["Macroplaza"]) # Macroplaza es el punto de partida
        self.distancias = defaultdict(dict) 
        self.posiciones = {
            "Macroplaza": (0.5, 0.5),
            "Parque Fundidora": (0.2, 0.7),
            "Museo del Acero": (0.3, 0.3),
            "Barrio Antiguo": (0.8, 0.6),
            "Catedral de Monterrey": (0.5, 0.8),
            "Cerro del Obispado": (0.8, 0.2),
            "Estadio BBVA": (0.2, 0.2),
            "Paseo Santa Lucía": (0.3, 0.7),
            "Museo de Historia Mexicana": (0.7, 0.75)
        }
    
    def agregar_ubicacion(self, nombre: str):
        if len(self.nodos) >= 6:  # Macroplaza + 5 ubicaciones
            return "Error: Máximo 5 ubicaciones permitidas"
        
        if nombre in self.nodos:
            return f"Error: '{nombre}' ya existe."
        
        self.nodos.add(nombre)
        return f"Ubicación '{nombre}' añadida."
    
    def eliminar_ubicacion(self, nombre: str):
        if nombre == "Macroplaza":
            return "No se puede eliminar Macroplaza"
        
        if nombre not in self.nodos:
            return f"Error: '{nombre}' no existe."
        
        self.nodos.remove(nombre)
        for origen in list(self.distancias.keys()):
            if nombre in self.distancias[origen]:
                del self.distancias[origen][nombre]
            if origen == nombre:
                del self.distancias[origen]
        
        return f"Ubicación '{nombre}' eliminada."
    
    def conectar_ubicaciones_densamente(self, distancias_predefinidas):
        """Conecta cada ubicación con Macroplaza y con al menos 2 nodos adicionales."""
        for nodo in self.nodos:
            if nodo != "Macroplaza":
                if "Macroplaza" not in self.distancias.get(nodo, {}):
                    self.distancias["Macroplaza"][nodo] = 2.0
                    self.distancias[nodo]["Macroplaza"] = 2.0
        
        for (origen, destino), distancia in distancias_predefinidas.items():
            if origen in self.nodos and destino in self.nodos:
                self.distancias[origen][destino] = distancia
                self.distancias[destino][origen] = distancia
        
        nodos_lista = list(self.nodos)
        for nodo in nodos_lista:
            if nodo == "Macroplaza":
                continue
                
            conexiones_actuales = [destino for destino in self.distancias.get(nodo, {}) 
                                 if destino != "Macroplaza"]
            
            if len(conexiones_actuales) < 2:
                candidatos = [n for n in nodos_lista 
                            if n != nodo and n != "Macroplaza" 
                            and n not in conexiones_actuales]
                
                # Calcular distancias basadas en posiciones
                if nodo in self.posiciones:
                    candidatos_con_distancia = []
                    for candidato in candidatos:
                        if candidato in self.posiciones:
                            dx = self.posiciones[nodo][0] - self.posiciones[candidato][0]
                            dy = self.posiciones[nodo][1] - self.posiciones[candidato][1]
                            distancia = np.sqrt(dx**2 + dy**2) * 3  # Escalar para km aproximados
                            candidatos_con_distancia.append((candidato, distancia))
                    
                    # Ordenar por distancia y tomar los más cercanos
                    candidatos_con_distancia.sort(key=lambda x: x[1])
                    
                    needed = min(2 - len(conexiones_actuales), len(candidatos_con_distancia))
                    for i in range(needed):
                        candidato, distancia = candidatos_con_distancia[i]
                        self.distancias[nodo][candidato] = round(distancia, 1)
                        self.distancias[candidato][nodo] = round(distancia, 1)
    
    def calcular_ruta_optima(self):
        if len(self.nodos) < 2:
            return None, "Se necesitan al menos 2 ubicaciones"
        
        destinos = [n for n in self.nodos if n != "Macroplaza"]
        
        # Algoritmo de aproximación TSP (Vecino más cercano)
        ruta = ["Macroplaza"]
        visitados = set(["Macroplaza"])
        distancia_total = 0
        
        while visitados != self.nodos:
            ultimo = ruta[-1]
            vecinos = [n for n in self.nodos 
                      if n not in visitados 
                      and n in self.distancias.get(ultimo, {})]
            
            if not vecinos:
                vecinos = [n for n in self.nodos 
                          if n not in visitados 
                          and "Macroplaza" in self.distancias.get(n, {})]
                if not vecinos:
                    break
                siguiente = min(vecinos, key=lambda n: self.distancias["Macroplaza"][n])
                distancia_total += self.distancias["Macroplaza"][siguiente]
            else:
                siguiente = min(vecinos, key=lambda n: self.distancias[ultimo][n])
                distancia_total += self.distancias[ultimo][siguiente]
            
            ruta.append(siguiente)
            visitados.add(siguiente)
        
        if ruta[-1] in self.distancias.get("Macroplaza", {}):
            distancia_total += self.distancias[ruta[-1]]["Macroplaza"]
            ruta.append("Macroplaza")
        
        return ruta, f"Distancia total: {distancia_total:.1f} km"
    
    def obtener_ubicaciones(self):
        return sorted(self.nodos)

class InterfazTurismo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.grafo = GrafoTurismo()
        self.title("Monterrey Tours Express - Rutas Turísticas Inteligentes")
        self.geometry("800x600")
        
        self.distancias_predefinidas = {
            # Conexiones con Macroplaza (distancias reales aproximadas)
            ("Macroplaza", "Parque Fundidora"): 1.8,
            ("Macroplaza", "Museo del Acero"): 2.1,
            ("Macroplaza", "Barrio Antiguo"): 0.8,
            ("Macroplaza", "Catedral de Monterrey"): 0.3,
            ("Macroplaza", "Cerro del Obispado"): 3.2,
            ("Macroplaza", "Estadio BBVA"): 6.8,
            ("Macroplaza", "Paseo Santa Lucía"): 0.5,
            ("Macroplaza", "Museo de Historia Mexicana"): 0.4,
            
            # Conexiones entre ubicaciones (distancias reales aproximadas)
            ("Parque Fundidora", "Museo del Acero"): 1.2,
            ("Parque Fundidora", "Paseo Santa Lucía"): 2.5,  
            ("Parque Fundidora", "Estadio BBVA"): 8.0,
            ("Museo del Acero", "Estadio BBVA"): 7.2,
            ("Museo del Acero", "Cerro del Obispado"): 4.1,
            ("Barrio Antiguo", "Cerro del Obispado"): 2.9,
            ("Barrio Antiguo", "Museo de Historia Mexicana"): 1.2,
            ("Catedral de Monterrey", "Museo de Historia Mexicana"): 0.6,
            ("Catedral de Monterrey", "Paseo Santa Lucía"): 0.7,
            ("Cerro del Obispado", "Estadio BBVA"): 5.4,
            ("Paseo Santa Lucía", "Museo de Historia Mexicana"): 0.8,
            ("Estadio BBVA", "Parque Fundidora"): 8.0
        }
        
        self._configurar_interfaz()
    
    def _configurar_interfaz(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(self.frame, text="Monterrey Tours Express", 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        
        ttk.Label(self.frame, text="Seleccione hasta 5 destinos turísticos (Macroplaza es punto de salida)", 
                 font=("Arial", 10)).grid(row=1, column=0, columnspan=3, pady=5)
        
        frame_disponibles = ttk.LabelFrame(self.frame, text="Ubicaciones Disponibles")
        frame_disponibles.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.lista_disponibles = tk.Listbox(frame_disponibles, width=25, height=10, selectmode=tk.SINGLE)
        self.lista_disponibles.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ubicaciones = [
            "Parque Fundidora", "Museo del Acero", "Barrio Antiguo",
            "Catedral de Monterrey", "Cerro del Obispado", "Estadio BBVA",
            "Paseo Santa Lucía", "Museo de Historia Mexicana"
        ]
        for ubi in ubicaciones:
            self.lista_disponibles.insert(tk.END, ubi)
        
        frame_botones = ttk.Frame(self.frame)
        frame_botones.grid(row=2, column=1, padx=10, pady=10, sticky="n")
        
        ttk.Button(frame_botones, text="Añadir Destino ➡", 
                  command=self._añadir_ubicacion, width=15).pack(pady=10, fill=tk.X)
        ttk.Button(frame_botones, text="Eliminar Destino ⬅", 
                  command=self._eliminar_ubicacion, width=15).pack(pady=10, fill=tk.X)
        ttk.Button(frame_botones, text="Mostrar Mapa", 
                  command=self._dibujar_mapa, width=15).pack(pady=20, fill=tk.X)
        ttk.Button(frame_botones, text="Calcular Ruta", 
                  command=self._calcular_ruta_optima, width=15).pack(pady=10, fill=tk.X)
        
        frame_seleccionadas = ttk.LabelFrame(self.frame, text="Destinos Seleccionados")
        frame_seleccionadas.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        
        self.lista_seleccionadas = tk.Listbox(frame_seleccionadas, width=25, height=10)
        self.lista_seleccionadas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.lista_seleccionadas.insert(tk.END, "Macroplaza (Punto de Salida)")
        
        frame_resultados = ttk.LabelFrame(self.frame, text="Ruta Óptima")
        frame_resultados.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.resultado = tk.Text(frame_resultados, height=4, width=80, font=("Arial", 10))
        self.resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.resultado.insert(tk.END, "Seleccione destinos y calcule la ruta óptima...")
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(2, weight=1)
    
    def _añadir_ubicacion(self):
        if self.lista_seleccionadas.size() >= 6: 
            messagebox.showwarning("Límite Alcanzado", "Máximo 5 destinos permitidos")
            return
        
        seleccion = self.lista_disponibles.curselection()
        if not seleccion:
            messagebox.showwarning("Nada Seleccionado", "Seleccione una ubicación de la lista izquierda")
            return
        
        nombre = self.lista_disponibles.get(seleccion[0])
        resultado = self.grafo.agregar_ubicacion(nombre)
        
        if "Error" not in resultado:
            self.lista_seleccionadas.insert(tk.END, nombre)
            self.lista_disponibles.delete(seleccion[0])
        
        messagebox.showinfo("Resultado", resultado)
    
    def _eliminar_ubicacion(self):
        seleccion = self.lista_seleccionadas.curselection()
        if not seleccion:
            messagebox.showwarning("Nada Seleccionado", "Seleccione una ubicación de la lista derecha")
            return
        
        nombre = self.lista_seleccionadas.get(seleccion[0])
        
        # No permitir eliminar Macroplaza
        if "Macroplaza" in nombre:
            messagebox.showinfo("Información", "Macroplaza no se puede eliminar")
            return
        
        resultado = self.grafo.eliminar_ubicacion(nombre)
        self.lista_disponibles.insert(tk.END, nombre)
        self.lista_seleccionadas.delete(seleccion[0])
        messagebox.showinfo("Resultado", resultado)
    
    def _dibujar_mapa(self):
        if len(self.grafo.nodos) < 2:
            messagebox.showwarning("Mapa Vacío", "Añada destinos primero")
            return
        
        self.grafo.conectar_ubicaciones_densamente(self.distancias_predefinidas)
        
        G = nx.Graph()
        
        for nodo in self.grafo.nodos:
            if nodo in self.grafo.posiciones:
                G.add_node(nodo, pos=self.grafo.posiciones[nodo])
        
        for origen in self.grafo.distancias:
            for destino, dist in self.grafo.distancias[origen].items():
                if origen in G.nodes() and destino in G.nodes():
                    G.add_edge(origen, destino, weight=dist)
        
        pos = nx.get_node_attributes(G, 'pos')
        plt.figure(figsize=(12, 10))
        
        nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=1, alpha=0.6)
        
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", edgecolors="black")
        
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
        
        if "Macroplaza" in pos:
            nx.draw_networkx_nodes(G, pos, nodelist=["Macroplaza"], node_size=2500, node_color="gold", edgecolors="black")
        
        edge_labels = {}
        for edge in G.edges():
            if G.has_edge(edge[0], edge[1]):
                weight = G[edge[0]][edge[1]]['weight']
                edge_labels[edge] = f"{weight:.1f}"
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7, alpha=0.8)
        
        plt.title("Red de Destinos Turísticos - Monterrey Tours Express", fontsize=14)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
    
    def _calcular_ruta_optima(self):

        self.grafo.conectar_ubicaciones_densamente(self.distancias_predefinidas)
        
        ruta, distancia = self.grafo.calcular_ruta_optima()
        self.resultado.delete(1.0, tk.END)
        
        if ruta:
            self.resultado.insert(tk.END, f"Ruta Óptima:\n{' → '.join(ruta)}\n\n{distancia}")
            self._dibujar_ruta_optima(ruta)
        else:
            self.resultado.insert(tk.END, "No se pudo calcular una ruta completa")
    
    def _dibujar_ruta_optima(self, ruta):
        G = nx.Graph()
        pos = {}
        
        for nodo in self.grafo.nodos:
            if nodo in self.grafo.posiciones:
                pos[nodo] = self.grafo.posiciones[nodo]
                G.add_node(nodo)
        
        for origen in self.grafo.distancias:
            for destino, dist in self.grafo.distancias[origen].items():
                if origen in pos and destino in pos:  # Solo si ambos nodos existen
                    G.add_edge(origen, destino, weight=dist)
        
        plt.figure(figsize=(12, 10))
        
        todas_aristas = list(G.edges())
        nx.draw_networkx_edges(G, pos, edgelist=todas_aristas, edge_color="black", width=1, alpha=0.4)
        
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", edgecolors="black")
        
        if "Macroplaza" in pos:
            nx.draw_networkx_nodes(G, pos, nodelist=["Macroplaza"], node_size=2500, node_color="gold", edgecolors="black")
        
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
        
        ruta_edges = []
        for i in range(1, len(ruta)):
            if G.has_edge(ruta[i-1], ruta[i]):
                ruta_edges.append((ruta[i-1], ruta[i]))
        
        nx.draw_networkx_edges(G, pos, edgelist=ruta_edges, width=4, edge_color="red", alpha=0.9)
        
        etiquetas_todas = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(
            G, 
            pos, 
            edge_labels={k: f"{v:.1f}" for k, v in etiquetas_todas.items()},
            font_color='gray',
            font_size=7,
            alpha=0.7
        )
        
        edge_labels_optimas = {}
        for edge in ruta_edges:
            if G.has_edge(edge[0], edge[1]):
                edge_data = G.get_edge_data(edge[0], edge[1])
                edge_labels_optimas[edge] = f"{edge_data['weight']:.1f} km"

        nx.draw_networkx_edge_labels(
            G, 
            pos, 
            edge_labels=edge_labels_optimas,
            font_color='red',
            font_size=10,
            font_weight='bold',
            bbox=dict(facecolor='white', edgecolor='red', alpha=0.9, boxstyle='round,pad=0.3')
        )
        
        plt.title("Ruta Turística Óptima - Monterrey Tours Express", fontsize=14)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

# Iniciar la aplicación
if __name__ == "__main__":
    app = InterfazTurismo()
    app.mainloop()