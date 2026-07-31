from collections import deque
import heapq
class Ciudad:
    def __init__(self, nombre, x=0, y=0):# Representa un vértice del grafo.
        self.nombre = nombre
        self.x = x
        self.y = y
    def __str__(self):
        return self.nombre
    def __repr__(self):
        return self.nombre
class Ruta:
    def __init__(self, origen, destino, distancia):#Representa una arista del grafo.
        self.origen = origen
        self.destino = destino
        self.distancia = distancia
    def __str__(self):
        return f"{self.origen} <--> {self.destino} ({self.distancia} km)"
    def __repr__(self):
        return self.__str__()
class Grafo:
    def __init__(self):
        self.ciudades = {} # Diccionario de ciudades
        self.adyacencia = {} # Lista de adyacencia
    def agregar_ciudad(self, nombre, x=0, y=0):#Agrega una ciudad al grafo. Complejidad: O(1)
        if nombre in self.ciudades:
            return False
        self.ciudades[nombre] = Ciudad(nombre, x, y)
        self.adyacencia[nombre] = []
        return True
    def eliminar_ciudad(self, nombre): #Elimina una ciudad. Complejidad: O(V+E)
        if nombre not in self.ciudades:
            return False
        del self.ciudades[nombre]
        del self.adyacencia[nombre]
        for ciudad in self.adyacencia:
            self.adyacencia[ciudad] = [(vecino, peso) for vecino, peso in self.adyacencia[ciudad] if vecino != nombre]
        return True
    def existe_ciudad(self, nombre):
        return nombre in self.ciudades
    def buscar_ciudad(self, nombre):
        return self.ciudades.get(nombre)
    def obtener_ciudades(self):
        return list(self.ciudades.keys())
    def numero_vertices(self):
        return len(self.ciudades)
    def agregar_ruta(self, origen, destino, distancia):#Agrega una ruta bidireccional.Complejidad: O(1)
        if origen not in self.ciudades:
            return False
        if destino not in self.ciudades:
            return False
        if self.existe_ruta(origen, destino):
            return False
        self.adyacencia[origen].append((destino, distancia))
        self.adyacencia[destino].append((origen, distancia))
        return True
    def eliminar_ruta(self, origen, destino): #Elimina una ruta. Complejidad: O(E)
        if origen not in self.adyacencia:
            return False
        if destino not in self.adyacencia:
            return False
        self.adyacencia[origen] = [(v, p) for v, p in self.adyacencia[origen] if v != destino]
        self.adyacencia[destino] = [(v, p) for v, p in self.adyacencia[destino] if v != origen]
        return True
    def existe_ruta(self, origen, destino):
        if origen not in self.adyacencia:
            return False
        for vecino, _ in self.adyacencia[origen]:
            if vecino == destino:
                return True
        return False
    def obtener_vecinos(self, ciudad):
        if ciudad not in self.adyacencia:
            return []
        return self.adyacencia[ciudad]
    def obtener_rutas(self): #Devuelve todas las rutas del grafo.
        rutas = []
        visitadas = set()
        for origen in self.adyacencia:
            for destino, peso in self.adyacencia[origen]:
                clave = tuple(sorted((origen, destino)))
                if clave not in visitadas:
                    rutas.append(Ruta(origen, destino, peso))
                    visitadas.add(clave)
        return rutas
    def numero_aristas(self):
        total = 0
        for vecinos in self.adyacencia.values():
            total += len(vecinos)
        return total // 2
    def mostrar_ciudades(self):
        print("\n========== CIUDADES ==========\n")
        for ciudad in self.ciudades.values():
            print(ciudad)
    def mostrar_rutas(self):
        print("\n========== RUTAS ==========\n")
        for ruta in self.obtener_rutas():
            print(ruta)
    def mostrar_lista_adyacencia(self):
        print("\n====== LISTA DE ADYACENCIA ======\n")
        for ciudad, vecinos in self.adyacencia.items():
            print(f"{ciudad} -> {vecinos}")
    def limpiar(self):
        self.ciudades.clear()
        self.adyacencia.clear()
    def grado(self, ciudad):#Devuelve el grado de una ciudad. Complejidad: O(1)
        if ciudad not in self.adyacencia:
            return 0
        return len(self.adyacencia[ciudad])
    def mostrar_grados(self): #Muestra el grado de todas las ciudades. Complejidad: O(V)
        print("\n========== GRADO DE LAS CIUDADES ==========\n")
        for ciudad in self.obtener_ciudades():
            print(f"{ciudad}: {self.grado(ciudad)}")
    def bfs(self, origen):# Busqueda de anchura Bfs. Retorna: recorrido, niveles y  padres. Complejidad O(V + E)
        if origen not in self.ciudades:
            return [], {}, {}
        visitados = set([origen])
        cola = deque([origen])
        recorrido = []
        niveles = {origen: 0}
        padres = {origen: None}
        while cola:
            actual = cola.popleft()
            recorrido.append(actual)
            for vecino, _ in self.adyacencia[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
                    niveles[vecino] = niveles[actual] + 1
                    padres[vecino] = actual
        return recorrido, niveles, padres

    def dfs(self, origen):#Busqueda en profundidad Dfs. Recorrido DFS iterativo. Complejidad: O(V + E)
        if origen not in self.ciudades:
            return []
        visitados = set()
        pila = [origen]
        recorrido = []
        while pila:
            actual = pila.pop()
            if actual not in visitados:
                visitados.add(actual)
                recorrido.append(actual)
                vecinos = self.adyacencia[actual]
                for vecino, _ in reversed(vecinos):
                    if vecino not in visitados:
                        pila.append(vecino)
        return recorrido
    def es_conexo(self): # Determina si el grafo es conexo. Complejidad O(V + E)
        if self.numero_vertices() == 0:
            return True
        inicio = next(iter(self.ciudades))
        recorrido, _, _ = self.bfs(inicio)
        return len(recorrido) == self.numero_vertices()
    def reconstruir_ruta(self, padres, destino): # Reconstruimos la ruta a partir del disccionario de padres. Complejidad O(V)
        ruta = []
        actual = destino
        while actual is not None:
            ruta.append(actual)
            actual = padres.get(actual)
        ruta.reverse()
        return ruta
    def informacion(self): # Mostramos la información en un resumen del grafo.
        print("\n========== INFORMACIÓN ==========\n")
        print("Número de ciudades :", self.numero_vertices())
        print("Número de rutas    :", self.numero_aristas())
        print("Grafo conexo       :", self.es_conexo())
    def ruta_bfs(self, origen, destino):# Buscamos la ruta mediante Bfs. Nos muestra la ruta y las paradas.
        recorrido, niveles, padres = self.bfs(origen)
        if destino not in padres:
            return [], -1
        ruta = self.reconstruir_ruta(padres, destino)
        return ruta, niveles[destino]
    def dijkstra(self, origen):#Algoritmo Djikstra que muestra la distancia minima desde el origen hacia las demás. Complejidad O((V + E) log V)
        if origen not in self.ciudades:
            return {}, {}
        distancias = {ciudad: float("inf") for ciudad in self.ciudades}
        padres = {ciudad: None for ciudad in self.ciudades}
        distancias[origen] = 0
        cola = [(0, origen)]
        while cola:
            distancia_actual, actual = heapq.heappop(cola)
            if distancia_actual > distancias[actual]:
                continue
            for vecino, peso in self.adyacencia[actual]:
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = actual
                    heapq.heappush(cola,(nueva_distancia, vecino))
        return distancias, padres
    def ruta_mas_corta(self, origen, destino):# Obtenemos la ruta minima
        distancias, padres = self.dijkstra(origen)
        if destino not in distancias:
            return [], float("inf")
        if distancias[destino] == float("inf"):
            return [], float("inf")
        ruta = self.reconstruir_ruta(padres,destino)
        return ruta, distancias[destino]
    def ciudad_mas_cercana(self, origen):#Obtenemos la ciudad que esta mas cerca
        distancias, _ = self.dijkstra(origen)
        menor = float("inf")
        ciudad = None
        for nombre, distancia in distancias.items():
            if nombre == origen:
                continue
            if distancia < menor:
                menor = distancia
                ciudad = nombre
        return ciudad, menor
    def ciudad_mas_lejana(self, origen):#Obtenemos la ciudad mas lejana
        distancias, _ = self.dijkstra(origen)
        mayor = -1
        ciudad = None
        for nombre, distancia in distancias.items():
            if nombre == origen:
                continue
            if distancia == float("inf"):
                continue
            if distancia > mayor:
                mayor = distancia
                ciudad = nombre
        return ciudad, mayor
    def comparar_algoritmos(self, origen, destino): # Comparamos Bfs y Dijkstra
        ruta_bfs, paradas = self.ruta_bfs(origen,destino)
        ruta_dijkstra, distancia = self.ruta_mas_corta(origen,destino)
        return {
            "ruta_bfs": ruta_bfs,
            "paradas": paradas,
            "ruta_dijkstra": ruta_dijkstra,
            "distancia": distancia
        }
    def mostrar_dijkstra(self, origen):#Mostramos el algoritmo Dijkstra
        distancias, _ = self.dijkstra(origen)
        print("\n========== DISTANCIAS ==========\n")
        for ciudad in sorted(distancias):
            distancia = distancias[ciudad]
            if distancia == float("inf"):
                print(f"{ciudad:15} No alcanzable")
            else:
                print(f"{ciudad:15} {distancia} km")

    def mostrar_comparacion(self, origen, destino):# Mostramos la comparación
        datos = self.comparar_algoritmos(origen, destino)
        print("\n========== COMPARACIÓN ==========\n")
        print("Bfs")
        print("Ruta:")
        print(" -> ".join(datos["ruta_bfs"]))
        print(f"Paradas: {datos['paradas']}")
        print()
        print("Dijkstra")
        print("Ruta:")
        print(" -> ".join(datos["ruta_dijkstra"]))
        print(f"Distancia: {datos['distancia']} km")
    def matriz_adyacencia(self):# Generamos la matriz de adyacencia. Tiene una complejidad de O(V²)
        ciudades = sorted(self.obtener_ciudades())
        indice = {ciudad: i for i, ciudad in enumerate(ciudades)}
        n = len(ciudades)
        matriz = [[0] * n for _ in range(n)]#Generamos la matriz Zero
        for origen in ciudades:
            fila = indice[origen]
            for destino, peso in self.adyacencia[origen]:
                columna = indice[destino]
                matriz[fila][columna] = peso
        return ciudades, matriz
    def obtener_coordenadas(self):# Nos permite devolver las coordenadas de las ciudades.
        coordenadas = {}
        for ciudad in self.ciudades.values():
            coordenadas[ciudad.nombre] = (ciudad.x, ciudad.y)
        return coordenadas
    def __str__(self):# Mostramos la matriz de adyacencia
        texto = "\n====== LISTA DE ADYACENCIA ======\n\n"
        for ciudad in self.obtener_ciudades():
            texto += f"{ciudad} -> "
            vecinos = []
            for vecino, peso in self.adyacencia[ciudad]:
                vecinos.append(f"{vecino}({peso})")
            texto += ", ".join(vecinos)
            texto += "\n"
        return texto
def crear_grafo():
    grafo = Grafo()
    ciudades = [
        ("Quito", 360, 60),
        ("Latacunga", 330, 140),
        ("Ambato", 360, 230),
        ("Riobamba", 340, 320),
        ("Guayaquil", 130, 450),
        ("Cuenca", 470, 470)
    ]
    for nombre, x, y in ciudades:
        grafo.agregar_ciudad(nombre, x, y)
    rutas = [
        ("Quito", "Latacunga", 95),
        ("Quito", "Ambato", 120),
        ("Latacunga", "Riobamba", 90),
        ("Ambato", "Riobamba", 50),
        ("Riobamba", "Cuenca", 110),
        ("Quito", "Guayaquil", 450),
        ("Guayaquil", "Cuenca", 210)
    ]
    for origen, destino, peso in rutas:
        grafo.agregar_ruta(origen, destino, peso)
    return grafo
