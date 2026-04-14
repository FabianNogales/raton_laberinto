from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageTk

    PIL_DISPONIBLE = True
except ModuleNotFoundError:
    Image = None
    ImageTk = None
    PIL_DISPONIBLE = False

from BibliotecaLaberintos import BibliotecaLaberintos
from BusquedaBase import ErrorEscenario, Posicion, ResultadoBusqueda, validar_escenario
from LogicaAmplitud import SolucionadorAmplitud
from LogicaVoraz import SolucionadorVoraz


class InterfazCarrera:
    def __init__(self, ventanaRaiz: tk.Tk):
        self.ventanaRaiz = ventanaRaiz
        self.ventanaRaiz.title("Comparativa de Busquedas IA - Raton y Queso")
        self.ventanaRaiz.config(bg="#1A332B")

        self.tamanoCelda = 32
        self.rutaImagenes = Path(__file__).resolve().parent.parent / "imagenes"

        self.imgRaton = None
        self.imgQueso = None
        self._cargar_imagenes()

        self.gestorMapas = BibliotecaLaberintos()
        self.totalLaberintos = len(self.gestorMapas.coleccionDeMapas)
        self.indiceLaberintoActual = 1

        self.mapaLaberinto = []
        self.totalFilas = 0
        self.totalColumnas = 0
        self.inicioRaton: Posicion = (0, 0)
        self.metaQueso: Posicion = (0, 0)

        self.resultadoAmplitud: Optional[ResultadoBusqueda] = None
        self.resultadoVoraz: Optional[ResultadoBusqueda] = None
        self.expansionAmplitudAnim: list[Posicion] = []
        self.expansionVorazAnim: list[Posicion] = []
        self.rutaAmplitudAnim: list[Posicion] = []
        self.rutaVorazAnim: list[Posicion] = []
        self.idxA = 0
        self.idxV = 0

        self._cargar_laberinto_actual()
        self.ConstruirInterfaz()

    def _cargar_imagenes(self) -> None:
        if not PIL_DISPONIBLE:
            return

        try:
            ruta_raton = self.rutaImagenes / "raton.png"
            ruta_queso = self.rutaImagenes / "queso.png"

            img_original_raton = Image.open(ruta_raton).convert("RGBA")
            img_redimensionada_raton = img_original_raton.resize(
                (self.tamanoCelda, self.tamanoCelda), Image.Resampling.LANCZOS
            )
            self.imgRaton = ImageTk.PhotoImage(img_redimensionada_raton)

            img_original_queso = Image.open(ruta_queso).convert("RGBA")
            img_redimensionada_queso = img_original_queso.resize(
                (self.tamanoCelda, self.tamanoCelda), Image.Resampling.LANCZOS
            )
            self.imgQueso = ImageTk.PhotoImage(img_redimensionada_queso)
        except Exception:
            self.imgRaton = None
            self.imgQueso = None

    def _cargar_laberinto_actual(self) -> None:
        self.mapaLaberinto = self.gestorMapas.ObtenerMapaPorNumero(self.indiceLaberintoActual)
        self.totalFilas = len(self.mapaLaberinto)
        self.totalColumnas = len(self.mapaLaberinto[0]) if self.totalFilas > 0 else 0
        self.inicioRaton = (0, 0)
        self.metaQueso = (self.totalFilas - 1, self.totalColumnas - 1)

    def ConstruirInterfaz(self) -> None:
        lblTitulo = tk.Label(
            self.ventanaRaiz,
            text="PROYECTO IA: Carrera Raton y Queso",
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#1A332B",
        )
        lblTitulo.pack(pady=10)

        self.lblLaberintoActual = tk.Label(
            self.ventanaRaiz,
            text=self._texto_laberinto_actual(),
            font=("Arial", 12, "bold"),
            fg="#F3D79C",
            bg="#1A332B",
        )
        self.lblLaberintoActual.pack(pady=(0, 8))

        framePrincipal = tk.Frame(self.ventanaRaiz, bg="#1A332B")
        framePrincipal.pack(padx=20, pady=10)

        frameAmplitud = tk.Frame(framePrincipal, bg="#1A332B", highlightbackground="#CBA471", highlightthickness=2)
        frameAmplitud.grid(row=0, column=0, padx=10)
        tk.Label(frameAmplitud, text="Amplitud (BFS)", font=("Arial", 13, "bold"), fg="#00FFAA", bg="#1A332B").pack(pady=5)

        frameCuerpoIzq = tk.Frame(frameAmplitud, bg="#1A332B")
        frameCuerpoIzq.pack()
        self.lblStatsAmplitud = tk.Label(
            frameCuerpoIzq,
            text=self._texto_stats_inicial(),
            font=("Arial", 11),
            fg="white",
            bg="#1A332B",
            justify="left",
        )
        self.lblStatsAmplitud.pack(side="left", padx=10)
        self.canvasAmplitud = tk.Canvas(
            frameCuerpoIzq,
            width=self.totalColumnas * self.tamanoCelda,
            height=self.totalFilas * self.tamanoCelda,
            bg="white",
            highlightthickness=0,
        )
        self.canvasAmplitud.pack(side="right", padx=10, pady=10)

        frameVoraz = tk.Frame(framePrincipal, bg="#1A332B", highlightbackground="#CBA471", highlightthickness=2)
        frameVoraz.grid(row=0, column=1, padx=10)
        tk.Label(frameVoraz, text="Busqueda Voraz", font=("Arial", 13, "bold"), fg="#00FFAA", bg="#1A332B").pack(pady=5)

        frameCuerpoDer = tk.Frame(frameVoraz, bg="#1A332B")
        frameCuerpoDer.pack()
        self.canvasVoraz = tk.Canvas(
            frameCuerpoDer,
            width=self.totalColumnas * self.tamanoCelda,
            height=self.totalFilas * self.tamanoCelda,
            bg="white",
            highlightthickness=0,
        )
        self.canvasVoraz.pack(side="left", padx=10, pady=10)
        self.lblStatsVoraz = tk.Label(
            frameCuerpoDer,
            text=self._texto_stats_inicial(),
            font=("Arial", 11),
            fg="white",
            bg="#1A332B",
            justify="left",
        )
        self.lblStatsVoraz.pack(side="right", padx=10)

        frameBotones = tk.Frame(self.ventanaRaiz, bg="#1A332B")
        frameBotones.pack(pady=10)

        self.btnIniciar = tk.Button(
            frameBotones,
            text="Iniciar Busqueda",
            font=("Arial", 13, "bold"),
            fg="#1A332B",
            bg="#00FFAA",
            command=self.IniciarCarrera,
        )
        self.btnIniciar.grid(row=0, column=0, padx=8)

        self.btnSiguiente = tk.Button(
            frameBotones,
            text="Siguiente Laberinto",
            font=("Arial", 13, "bold"),
            fg="#1A332B",
            bg="#F3D79C",
            command=self.CargarSiguienteLaberinto,
        )
        self.btnSiguiente.grid(row=0, column=1, padx=8)

        self.lblEstado = tk.Label(
            self.ventanaRaiz,
            text="Listo para ejecutar.",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#1A332B",
        )
        self.lblEstado.pack(pady=(0, 10))

        self.DibujarLaberintoInicial(self.canvasAmplitud)
        self.DibujarLaberintoInicial(self.canvasVoraz)

    def _texto_laberinto_actual(self) -> str:
        return f"Laberinto actual: {self.indiceLaberintoActual} de {self.totalLaberintos}"

    def _texto_stats_inicial(self) -> str:
        return (
            "Estadisticas\n\n"
            "Tiempo: 0.00000 s\n"
            "Nodos generados: 0\n"
            "Nodos expandidos: 0\n"
            "Longitud ruta: 0\n"
            "Costo total: 0\n"
            "Solucion: No ejecutado"
        )

    def _texto_stats(
        self,
        resultado: ResultadoBusqueda,
        nodos_expandidos_mostrados: Optional[int] = None,
    ) -> str:
        expandidos = resultado.nodos_expandidos
        if nodos_expandidos_mostrados is not None:
            expandidos = min(nodos_expandidos_mostrados, resultado.nodos_expandidos)

        solucion = "Si" if resultado.encontro_solucion else "No"
        return (
            "Estadisticas\n\n"
            f"Tiempo: {resultado.tiempo_segundos:.5f} s\n"
            f"Nodos generados: {resultado.nodos_generados}\n"
            f"Nodos expandidos: {expandidos}\n"
            f"Longitud ruta: {resultado.longitud_ruta}\n"
            f"Costo total: {resultado.costo_total}\n"
            f"Solucion: {solucion}"
        )

    def _filtrar_para_animacion(self, nodos: list[Posicion]) -> list[Posicion]:
        return [nodo for nodo in nodos if nodo not in (self.inicioRaton, self.metaQueso)]

    def _mensaje_estado(self) -> str:
        if self.resultadoAmplitud is None or self.resultadoVoraz is None:
            return "Listo para ejecutar."

        estado_bfs = "con solucion" if self.resultadoAmplitud.encontro_solucion else "sin solucion"
        estado_voraz = "con solucion" if self.resultadoVoraz.encontro_solucion else "sin solucion"
        return f"BFS: {estado_bfs} | Voraz: {estado_voraz}"

    def DibujarLaberintoInicial(self, canvas: tk.Canvas) -> None:
        canvas.delete("all")
        for f in range(self.totalFilas):
            for c in range(self.totalColumnas):
                color = "white"
                if self.mapaLaberinto[f][c] == 1:
                    color = "#2E4F43"
                canvas.create_rectangle(
                    c * self.tamanoCelda,
                    f * self.tamanoCelda,
                    (c + 1) * self.tamanoCelda,
                    (f + 1) * self.tamanoCelda,
                    fill=color,
                    outline="#D1D1D1",
                )

        self.DibujarIcono(canvas, self.inicioRaton, "raton")
        self.DibujarIcono(canvas, self.metaQueso, "queso")

    def DibujarIcono(self, canvas: tk.Canvas, nodo: Posicion, tipo_icono: str) -> None:
        f, c = nodo
        x0 = c * self.tamanoCelda
        y0 = f * self.tamanoCelda
        x1 = (c + 1) * self.tamanoCelda
        y1 = (f + 1) * self.tamanoCelda
        x_centro = x0 + (self.tamanoCelda // 2)
        y_centro = y0 + (self.tamanoCelda // 2)

        if tipo_icono == "raton" and self.imgRaton is not None:
            canvas.create_image(x_centro, y_centro, image=self.imgRaton)
            return

        if tipo_icono == "queso" and self.imgQueso is not None:
            canvas.create_image(x_centro, y_centro, image=self.imgQueso)
            return

        if tipo_icono == "raton":
            canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="#4F81BD", outline="#2F4E73")
            canvas.create_text(x_centro, y_centro, text="R", fill="white", font=("Arial", 10, "bold"))
        else:
            canvas.create_rectangle(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="#F2C94C", outline="#AA7C00")
            canvas.create_text(x_centro, y_centro, text="Q", fill="#3A2A00", font=("Arial", 10, "bold"))

    def DibujarCeldaExpansion(self, canvas: tk.Canvas, nodo: Posicion, color: str) -> None:
        f, c = nodo
        canvas.create_rectangle(
            c * self.tamanoCelda,
            f * self.tamanoCelda,
            (c + 1) * self.tamanoCelda,
            (f + 1) * self.tamanoCelda,
            fill=color,
            outline="#D1D1D1",
        )
        if nodo == self.inicioRaton:
            self.DibujarIcono(canvas, self.inicioRaton, "raton")
        if nodo == self.metaQueso:
            self.DibujarIcono(canvas, self.metaQueso, "queso")

    def _validar_escenario_actual(self) -> tuple[bool, str]:
        try:
            validar_escenario(self.mapaLaberinto, self.inicioRaton, self.metaQueso)
            return True, ""
        except ErrorEscenario as error:
            return False, str(error)

    def CargarSiguienteLaberinto(self) -> None:
        self.indiceLaberintoActual += 1
        if self.indiceLaberintoActual > self.totalLaberintos:
            self.indiceLaberintoActual = 1

        self._cargar_laberinto_actual()
        self.lblLaberintoActual.config(text=self._texto_laberinto_actual())

        self.resultadoAmplitud = None
        self.resultadoVoraz = None
        self.lblStatsAmplitud.config(text=self._texto_stats_inicial())
        self.lblStatsVoraz.config(text=self._texto_stats_inicial())
        self.lblEstado.config(text="Laberinto cargado. Presione 'Iniciar Busqueda'.", fg="white")

        self.DibujarLaberintoInicial(self.canvasAmplitud)
        self.DibujarLaberintoInicial(self.canvasVoraz)

    def IniciarCarrera(self) -> None:
        self.btnIniciar.config(state=tk.DISABLED)
        self.btnSiguiente.config(state=tk.DISABLED)

        es_valido, mensaje = self._validar_escenario_actual()
        if not es_valido:
            self.lblEstado.config(text=f"Error de escenario: {mensaje}", fg="#FF9B9B")
            self.btnIniciar.config(state=tk.NORMAL)
            self.btnSiguiente.config(state=tk.NORMAL)
            return

        self.DibujarLaberintoInicial(self.canvasAmplitud)
        self.DibujarLaberintoInicial(self.canvasVoraz)

        self.resultadoAmplitud = SolucionadorAmplitud(
            self.mapaLaberinto, self.inicioRaton, self.metaQueso
        ).Resolver()
        self.resultadoVoraz = SolucionadorVoraz(
            self.mapaLaberinto, self.inicioRaton, self.metaQueso
        ).Resolver()

        self.expansionAmplitudAnim = self._filtrar_para_animacion(self.resultadoAmplitud.historial_expansion)
        self.expansionVorazAnim = self._filtrar_para_animacion(self.resultadoVoraz.historial_expansion)
        self.rutaAmplitudAnim = self._filtrar_para_animacion(self.resultadoAmplitud.camino)
        self.rutaVorazAnim = self._filtrar_para_animacion(self.resultadoVoraz.camino)

        self.lblStatsAmplitud.config(text=self._texto_stats(self.resultadoAmplitud, 0))
        self.lblStatsVoraz.config(text=self._texto_stats(self.resultadoVoraz, 0))

        self.idxA = 0
        self.idxV = 0
        self.lblEstado.config(text="Ejecutando animacion...", fg="white")
        self.Animar()

    def Animar(self) -> None:
        continuar = False

        if self.resultadoAmplitud is not None:
            if self.idxA < len(self.expansionAmplitudAnim):
                self.DibujarCeldaExpansion(self.canvasAmplitud, self.expansionAmplitudAnim[self.idxA], "#ADD8E6")
                self.idxA += 1
                continuar = True
            elif self.idxA == len(self.expansionAmplitudAnim):
                for nodo in self.rutaAmplitudAnim:
                    self.DibujarCeldaExpansion(self.canvasAmplitud, nodo, "#32CD32")
                self.idxA += 1

            self.lblStatsAmplitud.config(text=self._texto_stats(self.resultadoAmplitud, self.idxA))

        if self.resultadoVoraz is not None:
            if self.idxV < len(self.expansionVorazAnim):
                self.DibujarCeldaExpansion(self.canvasVoraz, self.expansionVorazAnim[self.idxV], "#ADD8E6")
                self.idxV += 1
                continuar = True
            elif self.idxV == len(self.expansionVorazAnim):
                for nodo in self.rutaVorazAnim:
                    self.DibujarCeldaExpansion(self.canvasVoraz, nodo, "#32CD32")
                self.idxV += 1

            self.lblStatsVoraz.config(text=self._texto_stats(self.resultadoVoraz, self.idxV))

        if continuar:
            self.ventanaRaiz.after(50, self.Animar)
            return

        if self.resultadoAmplitud is not None:
            self.lblStatsAmplitud.config(text=self._texto_stats(self.resultadoAmplitud))
        if self.resultadoVoraz is not None:
            self.lblStatsVoraz.config(text=self._texto_stats(self.resultadoVoraz))

        self.lblEstado.config(text=self._mensaje_estado(), fg="#F3D79C")
        self.btnIniciar.config(state=tk.NORMAL)
        self.btnSiguiente.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCarrera(root)
    root.mainloop()
