import tkinter as tk
import time
import os
from collections import deque
import heapq
from PIL import Image, ImageTk 
from BibliotecaLaberintos import BibliotecaLaberintos

class InterfazCarrera:
    def __init__(self, ventanaRaiz):
        self.ventanaRaiz = ventanaRaiz
        self.ventanaRaiz.title("Comparativa de Búsquedas IA - Ratón y Queso")
        self.ventanaRaiz.config(bg="#1A332B")
        
        self.tamanoCelda = 32 
        self.rutaImagenes = r"C:\Users\rodri\Documents\Importante\trabajo de ia\imagenes"
        
        # Carga y redimensionamiento de imágenes
        try:
            imgOriginalRaton = Image.open(os.path.join(self.rutaImagenes, "raton.png")).convert("RGBA")
            imgRedimensionadaRaton = imgOriginalRaton.resize((self.tamanoCelda, self.tamanoCelda), Image.Resampling.LANCZOS)
            self.imgRaton = ImageTk.PhotoImage(imgRedimensionadaRaton)

            imgOriginalQueso = Image.open(os.path.join(self.rutaImagenes, "queso.png")).convert("RGBA")
            imgRedimensionadaQueso = imgOriginalQueso.resize((self.tamanoCelda, self.tamanoCelda), Image.Resampling.LANCZOS)
            self.imgQueso = ImageTk.PhotoImage(imgRedimensionadaQueso)
            
        except Exception as e:
            print(f"Error al cargar/redimensionar las imágenes: {e}")
            self.imgRaton = None
            self.imgQueso = None

        # --- Gestión de Laberintos ---
        self.gestorMapas = BibliotecaLaberintos()
        
        # Iniciar siempre en el Laberinto 1
        self.indiceLaberintoActual = 1
        self.mapaLaberinto = self.gestorMapas.ObtenerMapaPorNumero(self.indiceLaberintoActual)
        
        self.totalFilas = len(self.mapaLaberinto)
        self.totalColumnas = len(self.mapaLaberinto[0])
        
        self.inicioRaton = (0, 0)
        self.metaQueso = (self.totalFilas - 1, self.totalColumnas - 1)
        
        self.ConstruirInterfaz()

    # --- Construcción de Interfaz Visual ---
    def ConstruirInterfaz(self):
        lblTitulo = tk.Label(self.ventanaRaiz, text="PROYECTO IA: Carrera Ratón y Queso", font=("Arial", 23, "bold"), fg="white", bg="#1A332B")
        lblTitulo.pack(pady=10)

        framePrincipal = tk.Frame(self.ventanaRaiz, bg="#1A332B")
        framePrincipal.pack(padx=20, pady=10)

        # Panel Izquierdo: Amplitud (BFS)
        frameAmplitud = tk.Frame(framePrincipal, bg="#1A332B", highlightbackground="#CBA471", highlightthickness=2)
        frameAmplitud.grid(row=0, column=0, padx=10)
        tk.Label(frameAmplitud, text="Amplitud (BFS)", font=("Arial", 13, "bold"), fg="#00FFaa", bg="#1A332B").pack(pady=5)
        
        frameCuerpoIzq = tk.Frame(frameAmplitud, bg="#1A332B")
        frameCuerpoIzq.pack()
        self.lblStatsAmplitud = tk.Label(frameCuerpoIzq, text="Estadísticas\n\nTiempo:\n0.000s\n\nNodos gen:\n0", font=("Arial", 11), fg="white", bg="#1A332B", justify="left")
        self.lblStatsAmplitud.pack(side="left", padx=10)
        self.canvasAmplitud = tk.Canvas(frameCuerpoIzq, width=self.totalColumnas * self.tamanoCelda, height=self.totalFilas * self.tamanoCelda, bg="white", highlightthickness=0)
        self.canvasAmplitud.pack(side="right", padx=10, pady=10)

        # Panel Derecho: Búsqueda Voraz
        frameVoraz = tk.Frame(framePrincipal, bg="#1A332B", highlightbackground="#CBA471", highlightthickness=2)
        frameVoraz.grid(row=0, column=1, padx=10)
        tk.Label(frameVoraz, text="Búsqueda Voraz", font=("Arial", 13, "bold"), fg="#00FFaa", bg="#1A332B").pack(pady=5)
        
        frameCuerpoDer = tk.Frame(frameVoraz, bg="#1A332B")
        frameCuerpoDer.pack()
        self.canvasVoraz = tk.Canvas(frameCuerpoDer, width=self.totalColumnas * self.tamanoCelda, height=self.totalFilas * self.tamanoCelda, bg="white", highlightthickness=0)
        self.canvasVoraz.pack(side="left", padx=10, pady=10)
        self.lblStatsVoraz = tk.Label(frameCuerpoDer, text="Estadísticas\n\nTiempo:\n0.000s\n\nNodos gen:\n0", font=("Arial", 11), fg="white", bg="#1A332B", justify="left")
        self.lblStatsVoraz.pack(side="right", padx=10)

        self.btnIniciar = tk.Button(self.ventanaRaiz, text="Siguiente Laberinto e Iniciar", font=("Arial", 15, "bold"), fg="#1A332B", bg="#00FFaa", command=self.IniciarCarrera)
        self.btnIniciar.pack(pady=20)

        self.DibujarLaberintoInicial(self.canvasAmplitud)
        self.DibujarLaberintoInicial(self.canvasVoraz)

    # --- Lógica de Dibujado en Canvas ---
    def DibujarLaberintoInicial(self, canvas):
        canvas.delete("all")
        for f in range(self.totalFilas):
            for c in range(self.totalColumnas):
                color = "white"
                if self.mapaLaberinto[f][c] == 1:
                    color = "#2E4F43"
                canvas.create_rectangle(c * self.tamanoCelda, f * self.tamanoCelda, (c + 1) * self.tamanoCelda, (f + 1) * self.tamanoCelda, fill=color, outline="#D1D1D1")
        
        self.DibujarIcono(canvas, self.inicioRaton, self.imgRaton)
        self.DibujarIcono(canvas, self.metaQueso, self.imgQueso)

    def DibujarIcono(self, canvas, nodo, imagen):
        f, c = nodo
        x = c * self.tamanoCelda + (self.tamanoCelda // 2)
        y = f * self.tamanoCelda + (self.tamanoCelda // 2)
        if imagen:
            canvas.create_image(x, y, image=imagen)
        else:
            color = "gray" if imagen == self.imgRaton else "yellow"
            canvas.create_rectangle(c * self.tamanoCelda, f * self.tamanoCelda, (c + 1) * self.tamanoCelda, (f + 1) * self.tamanoCelda, fill=color)

    def DibujarCeldaExpansion(self, canvas, nodo, color):
        f, c = nodo
        canvas.create_rectangle(c * self.tamanoCelda, f * self.tamanoCelda, (c + 1) * self.tamanoCelda, (f + 1) * self.tamanoCelda, fill=color, outline="#D1D1D1")
        if nodo == self.inicioRaton: self.DibujarIcono(canvas, self.inicioRaton, self.imgRaton)
        if nodo == self.metaQueso: self.DibujarIcono(canvas, self.metaQueso, self.imgQueso)

    # --- Lógica Búsqueda No Informada (Amplitud) ---
    def LogicaAmplitud(self):
        tInicio = time.perf_counter()
        cola = deque([self.inicioRaton]); visitados = {self.inicioRaton}; padres = {}; hist = []; gen = 1
        while cola:
            act = cola.popleft()
            if act == self.metaQueso: break
            for m in [(-1,0),(1,0),(0,-1),(0,1)]:
                v = (act[0]+m[0], act[1]+m[1])
                if 0<=v[0]<self.totalFilas and 0<=v[1]<self.totalColumnas:
                    if self.mapaLaberinto[v[0]][v[1]] == 0 and v not in visitados:
                        visitados.add(v); padres[v] = act; cola.append(v); gen += 1
                        if v != self.metaQueso: hist.append(v)
        tFin = time.perf_counter()
        return hist, self.ObtenerRuta(padres), tFin - tInicio, gen

    # --- Lógica Búsqueda Informada (Voraz) ---
    def LogicaVoraz(self):
        tInicio = time.perf_counter()
        colaP = []; heapq.heappush(colaP, (0, self.inicioRaton))
        visitados = {self.inicioRaton}; padres = {}; hist = []; gen = 1
        while colaP:
            _, act = heapq.heappop(colaP)
            if act == self.metaQueso: break
            for m in [(-1,0),(1,0),(0,-1),(0,1)]:
                v = (act[0]+m[0], act[1]+m[1])
                if 0<=v[0]<self.totalFilas and 0<=v[1]<self.totalColumnas:
                    if self.mapaLaberinto[v[0]][v[1]] == 0 and v not in visitados:
                        visitados.add(v); padres[v] = act
                        h = abs(v[0]-self.metaQueso[0]) + abs(v[1]-self.metaQueso[1])
                        heapq.heappush(colaP, (h, v)); gen += 1
                        if v != self.metaQueso: hist.append(v)
        tFin = time.perf_counter()
        return hist, self.ObtenerRuta(padres), tFin - tInicio, gen

    def ObtenerRuta(self, padres):
        r = []; act = self.metaQueso
        while act in padres and act != self.inicioRaton:
            r.append(act); act = padres[act]
        r.reverse()
        return r[:-1]

    # --- Controladores de Flujo y Animación ---
    def IniciarCarrera(self):
        self.btnIniciar.config(state=tk.DISABLED)
        
        # Avanzar al siguiente laberinto secuencialmente
        self.indiceLaberintoActual += 1
        if self.indiceLaberintoActual > 5:
            self.indiceLaberintoActual = 1
            
        self.mapaLaberinto = self.gestorMapas.ObtenerMapaPorNumero(self.indiceLaberintoActual)
        
        self.lblStatsAmplitud.config(text="Estadísticas\n\nTiempo:\n0.000s\n\nNodos gen:\n0")
        self.lblStatsVoraz.config(text="Estadísticas\n\nTiempo:\n0.000s\n\nNodos gen:\n0")

        self.DibujarLaberintoInicial(self.canvasAmplitud)
        self.DibujarLaberintoInicial(self.canvasVoraz)
        
        self.hA, self.rA, self.tA, self.gA = self.LogicaAmplitud()
        self.hV, self.rV, self.tV, self.gV = self.LogicaVoraz()
        
        self.idxA = 0
        self.idxV = 0
        self.Animar()

    def Animar(self):
        sig = False
        if self.idxA < len(self.hA):
            self.DibujarCeldaExpansion(self.canvasAmplitud, self.hA[self.idxA], "#ADD8E6")
            self.lblStatsAmplitud.config(text=f"Estadísticas\n\nTiempo:\n{self.tA:.5f}s\n\nNodos gen:\n{self.idxA + 1}")
            self.idxA += 1; sig = True
        elif self.idxA == len(self.hA):
            for n in self.rA: self.DibujarCeldaExpansion(self.canvasAmplitud, n, "#32CD32")
            self.lblStatsAmplitud.config(text=f"Estadísticas\n\nTiempo:\n{self.tA:.5f}s\n\nNodos gen:\n{self.gA}")
            self.idxA += 1

        if self.idxV < len(self.hV):
            self.DibujarCeldaExpansion(self.canvasVoraz, self.hV[self.idxV], "#ADD8E6")
            self.lblStatsVoraz.config(text=f"Estadísticas\n\nTiempo:\n{self.tV:.5f}s\n\nNodos gen:\n{self.idxV + 1}")
            self.idxV += 1; sig = True
        elif self.idxV == len(self.hV):
            for n in self.rV: self.DibujarCeldaExpansion(self.canvasVoraz, n, "#32CD32")
            self.lblStatsVoraz.config(text=f"Estadísticas\n\nTiempo:\n{self.tV:.5f}s\n\nNodos gen:\n{self.gV}")
            self.idxV += 1

        if sig: self.ventanaRaiz.after(50, self.Animar)
        else: self.btnIniciar.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCarrera(root)
    root.mainloop()