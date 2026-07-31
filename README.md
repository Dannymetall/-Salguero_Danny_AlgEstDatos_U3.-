# -Salguero_Danny_AlgEstDatos_U3.-
Les presento una aplicación de Grafos y algunos de sus algoritmos
# Deber Unidad 3 – Grafos

## Autor
Danny Salguero

## Asignatura
Algoritmos y Estructuras de Datos

## Descripción

Este proyecto implementa una red de ciudades utilizando la estructura de datos Grafo mediante listas de adyacencia.

El sistema permite representar ciudades y carreteras, recorrer el grafo mediante BFS y DFS, encontrar rutas mínimas con el algoritmo de Dijkstra, generar la matriz de adyacencia y visualizar el grafo mediante una interfaz gráfica desarrollada con Tkinter.

---

## Archivos del proyecto

main.py
Programa principal que ejecuta todas las pruebas del sistema desde consola.

utilidades.py
Contiene todas las clases y algoritmos del proyecto:

- Ciudad
- Ruta
- Grafo
- BFS
- DFS
- Dijkstra
- Ruta más corta
- Matriz de adyacencia
- Comparación entre BFS y Dijkstra

interfaz grafica.py

Interfaz gráfica desarrollada con Tkinter que permite:

- Visualizar el grafo
- Mostrar la matriz de adyacencia
- Ejecutar BFS
- Ejecutar Dijkstra
- Resaltar las rutas encontradas

---

## Requerimientos implementados

### R1 – Modelado del grafo

Se representa la red mediante una lista de adyacencia implementada con un diccionario donde cada ciudad almacena sus vecinos y la distancia correspondiente.

También se muestran:

- ciudades
- rutas
- grados
- matriz de adyacencia
- información general del grafo

---

### R2 – Recorrido del grafo

Se implementa el algoritmo BFS que:

- recorre todas las ciudades alcanzables
- calcula el número de escalas
- determina si el grafo es conexo

Además se implementa DFS para comparar ambos recorridos.

---

### R3 – Ruta mínima

Se integra el algoritmo de Dijkstra para calcular:

- distancia mínima hacia cada ciudad
- ruta más corta
- ciudad más cercana
- ciudad más lejana
Se puede visualizar los resultados mediante la ejecución de main.py, pero también se puede visualizar al utilizar la GUI caso por caso

---

### R4 – Comparación

El programa compara:

- la ruta obtenida mediante BFS (menor número de escalas)
- la ruta obtenida mediante Dijkstra (menor distancia o costo)

Hay que tener en cuenta cuando y en qué contexto debemos utilizar cada algoritmo, por ejemplo si optimizamos el costo sería perfecto Dijkstra, por otra parte si pretendemos hacer la menor cantidad de paradas es decir necesitamos mas velocidad sin tener en cuenta el costo deberíamos usar BFS.

Se debe tener en cuenta que ambas pueden ser diferentes.

---

## Cómo ejecutar

### Ejecutar desde consola

python main.py

Se mostrarán:

- ciudades
- rutas
- lista de adyacencia
- grados
- BFS
- DFS
- Dijkstra
- ruta mínima
- comparación
- matriz de adyacencia

---

### Ejecutar la interfaz gráfica

python "interfaz grafica.py"

La aplicación permite visualizar el grafo y ejecutar los algoritmos de manera interactiva.

---

## Tecnologías utilizadas

- Python 3
- Tkinter
- collections.deque
- heapq

No se utilizan bibliotecas externas como NetworkX.
