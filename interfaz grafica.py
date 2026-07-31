import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utilidades import crear_grafo
class InterfazGrafica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto de Grafos")
        self.geometry("1200x700")
        self.minsize(1000,600)
        self.grafo = crear_grafo()
        self.crear_menu()
        self.crear_widgets()
        self.cargar_combobox()
        self.actualizar_estado()
        self.canvas.bind("<Configure>",lambda event: self.dibujar_grafo())
    def crear_menu(self):
        barra = tk.Menu(self)
        menu_archivo = tk.Menu(barra, tearoff=0)
        menu_archivo.add_command(label="Actualizar",command=self.actualizar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir",command=self.destroy)
        barra.add_cascade(label="Archivo", menu=menu_archivo)
        menu_algoritmos = tk.Menu(barra, tearoff=0)
        menu_algoritmos.add_command(label="Bfs", command=self.ejecutar_bfs)
        menu_algoritmos.add_command(label="Dijkstra",command=self.ejecutar_dijkstra)
        barra.add_cascade(label="Algoritmos",menu=menu_algoritmos)
        menu_ayuda = tk.Menu(barra, tearoff=0)
        menu_ayuda.add_command(label="Acerca de...",command=lambda: messagebox.showinfo("Proyecto","Proyecto de Grafos\nEstructuras de Datos"))
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)
        self.config(menu=barra)
    def crear_widgets(self):
        panel = ttk.PanedWindow(self,orient=tk.HORIZONTAL)
        panel.pack(fill="both",expand=True,padx=10,pady=10)
        frame_matriz = ttk.LabelFrame(panel,text="Matriz de Adyacencia")
        panel.add(frame_matriz, weight=1)
        self.tabla = ttk.Treeview(frame_matriz,show="headings")
        scrollbar = ttk.Scrollbar(frame_matriz,orient="vertical",command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right",fill="y")
        frame_canvas = ttk.LabelFrame(panel,text="Grafo")
        panel.add(frame_canvas, weight=3)
        self.canvas = tk.Canvas(frame_canvas,bg="white")
        self.canvas.pack(fill="both",expand=True)
        inferior = ttk.Frame(self)
        inferior.pack(fill="x", padx=10, pady=5)
        ttk.Label(inferior,text="Origen:").grid(row=0,column=0,padx=5)
        self.cbo_origen = ttk.Combobox(inferior,state="readonly",width=18)
        self.cbo_origen.grid(row=0, column=1,padx=5)
        ttk.Label(inferior,text="Destino:").grid(row=0,column=2,padx=5)
        self.cbo_destino = ttk.Combobox(inferior,state="readonly",width=18)
        self.cbo_destino.grid(row=0, column=3, padx=5)
        ttk.Button(inferior, text="Bfs", command=self.ejecutar_bfs).grid(row=0,column=4,padx=8)
        ttk.Button(inferior, text="Dijkstra",command=self.ejecutar_dijkstra).grid(row=0,column=5,padx=8)
        ttk.Button(inferior, text="Actualizar", command=self.actualizar).grid(row=0,column=6,padx=8)
        ttk.Button(inferior, text="Salir", command=self.destroy).grid(row=0,column=7,padx=8)
        resultado = ttk.LabelFrame(self, text="Resultados")
        resultado.pack(fill="both", padx=10, pady=5)
        self.txt_resultado = tk.Text(resultado,height=8)
        self.txt_resultado.pack(fill="both",expand=True)
        self.estado = ttk.Label(self,anchor="w")
        self.estado.pack(fill="x",padx=5,pady=3)
    def cargar_combobox(self):
        ciudades = self.grafo.obtener_ciudades()
        self.cbo_origen["values"] = ciudades
        self.cbo_destino["values"] = ciudades
        if ciudades:
            self.cbo_origen.current(0)
            self.cbo_destino.current(len(ciudades)-1)
    def actualizar_estado(self):
        self.estado.config(
            text=(f"Ciudades: {self.grafo.numero_vertices()}   |   " f"Rutas: {self.grafo.numero_aristas()}   |   " f"Conexo: {'Sí' if self.grafo.es_conexo() else 'No'}"))
    def dibujar_grafo(self):
        self.canvas.delete("all")
        self.canvas.update_idletasks()
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()
        margen = 40
        coordenadas = self.grafo.obtener_coordenadas()
        xs = [x for x, y in coordenadas.values()]
        ys = [y for x, y in coordenadas.values()]
        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)
        ancho_grafo = xmax - xmin
        alto_grafo = ymax - ymin
        escala_x = (ancho - 2*margen) / ancho_grafo
        escala_y = (alto - 2*margen) / alto_grafo
        escala = min(escala_x, escala_y)
        offset_x = (ancho - ancho_grafo * escala) / 2
        offset_y = (alto - alto_grafo * escala) / 2
        coord = {}
        for nombre, (x, y) in coordenadas.items():
            nuevo_x = offset_x + (x - xmin) * escala
            nuevo_y = offset_y + (y - ymin) * escala
            coord[nombre] = (nuevo_x, nuevo_y)
        self.coord = coord
        for ruta in self.grafo.obtener_rutas():
            x1, y1 = coord[ruta.origen]
            x2, y2 = coord[ruta.destino]
            self.canvas.create_line(x1, y1, x2, y2, width=2, fill="black")
            xm = (x1+x2)/2
            ym = (y1+y2)/2
            self.canvas.create_text(xm, ym, text=str(ruta.distancia), fill="blue",font=("Arial",9,"bold"))
        radio = max(15, int(18*escala))
        for nombre, (x, y) in coord.items():
            self.canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill="lightyellow", outline="black", width=2)
            self.canvas.create_text(x, y, text=nombre, font=("Arial",9,"bold"))
    def mostrar_matriz(self):
        ciudades, matriz = self.grafo.matriz_adyacencia()
        self.tabla.delete(*self.tabla.get_children())
        columnas = ["Ciudad"] + ciudades
        self.tabla["columns"] = columnas
        for columna in columnas:
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, width=80, anchor="center")
        for i, ciudad in enumerate(ciudades):
            fila = [ciudad]
            for valor in matriz[i]:
                if valor == 0:
                    fila.append("-")
                else:
                    fila.append(valor)
            self.tabla.insert("", "end",values=fila)
    def actualizar(self):
        self.dibujar_grafo()
        self.mostrar_matriz()
        self.actualizar_estado()
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END,"Información actualizada correctamente.\n")
    def resaltar_ruta(self, ruta, color):
        if len(ruta) < 2:
            return
        self.dibujar_grafo()
        for i in range(len(ruta)-1):
            ciudad1 = ruta[i]
            ciudad2 = ruta[i+1]
            x1, y1 = self.coord[ciudad1]
            x2, y2 = self.coord[ciudad2]
            self.canvas.create_line(x1, y1, x2, y2,width=7,fill=color,capstyle=tk.ROUND)
        radio = 18
        for nombre, (x, y) in self.coord.items():
            if nombre in ruta:
                color_nodo = color
            else:
                color_nodo = "lightyellow"
            self.canvas.create_oval(x-radio, y-radio,x+radio,y+radio,fill=color_nodo,outline="black",width=2)
            self.canvas.create_text(x,y,text=nombre,font=("Arial",9,"bold"))
    def ejecutar_bfs(self):
        origen = self.cbo_origen.get()
        destino = self.cbo_destino.get()
        if not origen or not destino:
            messagebox.showwarning("Advertencia", "Seleccione una ciudad de origen y destino.")
            return
        ruta, paradas = self.grafo.ruta_bfs(origen, destino)
        self.actualizar()
        if not ruta:
            self.txt_resultado.delete("1.0", tk.END)
            self.txt_resultado.insert(tk.END, "No existe una ruta entre esas ciudades.")
            return
        self.resaltar_ruta(ruta,"#32CD32")
        self.resaltar_ruta(ruta,"blue")
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END,"========== Bfs ==========\n\n")
        self.txt_resultado.insert(tk.END,"Ruta encontrada:\n")
        self.txt_resultado.insert(tk.END," -> ".join(ruta))
        self.txt_resultado.insert(tk.END,f"\n\nNúmero de paradas: {paradas}")
    def ejecutar_dijkstra(self):
        origen = self.cbo_origen.get()
        destino = self.cbo_destino.get()
        if not origen or not destino:
            messagebox.showwarning("Advertencia","Seleccione una ciudad de origen y destino.")
            return
        ruta, distancia = self.grafo.ruta_mas_corta(origen, destino)
        self.actualizar()
        if not ruta:
            self.txt_resultado.delete("1.0", tk.END)
            self.txt_resultado.insert(tk.END,"No existe una ruta entre esas ciudades.")
            return
        self.resaltar_ruta(ruta,"#CC0000")
        self.resaltar_ruta(ruta,"red")
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END,"======= Dijkstra =======\n\n")
        self.txt_resultado.insert(tk.END,"Ruta mínima:\n")
        self.txt_resultado.insert(tk.END," -> ".join(ruta))
        self.txt_resultado.insert(tk.END,f"\n\nDistancia total: {distancia} km")
        ciudad, distancia_min = self.grafo.ciudad_mas_cercana(origen)
        self.txt_resultado.insert(tk.END,f"\n\nCiudad más cercana: {ciudad} ({distancia_min} km)")
        ciudad, distancia_max = self.grafo.ciudad_mas_lejana(origen)
        self.txt_resultado.insert(tk.END,f"\nCiudad más lejana: {ciudad} ({distancia_max} km)")
if __name__ == "__main__":
    app = InterfazGrafica()
    app.actualizar()
    app.mainloop()
