from __future__ import annotations

from collections import deque
from time import perf_counter
from typing import Deque, Dict, Set

from BusquedaBase import (
    MOVIMIENTOS_CARDINALES,
    ErrorEscenario,
    Posicion,
    ResultadoBusqueda,
    reconstruir_ruta,
    validar_escenario,
)


class SolucionadorAmplitud:
    def __init__(self, mapaLaberinto, inicioRaton: Posicion, metaQueso: Posicion):
        self.mapaLaberinto = mapaLaberinto
        self.inicioRaton = inicioRaton
        self.metaQueso = metaQueso

    def Resolver(self) -> ResultadoBusqueda:
        """Ejecuta Busqueda en Amplitud (BFS) sobre un mapa en grilla."""
        inicio_tiempo = perf_counter()

        try:
            validar_escenario(self.mapaLaberinto, self.inicioRaton, self.metaQueso)
        except ErrorEscenario as error:
            tiempo_total = perf_counter() - inicio_tiempo
            return ResultadoBusqueda(
                camino=[],
                historial_expansion=[],
                nodos_generados=0,
                nodos_expandidos=0,
                tiempo_segundos=tiempo_total,
                encontro_solucion=False,
                mensaje=str(error),
            )

        cola_de_nodos: Deque[Posicion] = deque([self.inicioRaton])
        nodos_visitados: Set[Posicion] = {self.inicioRaton}
        registro_de_padres: Dict[Posicion, Posicion] = {}
        historial_expansion: list[Posicion] = []

        nodos_generados = 1
        nodos_expandidos = 0
        encontro_meta = False

        total_filas = len(self.mapaLaberinto)
        total_columnas = len(self.mapaLaberinto[0])

        while cola_de_nodos:
            nodo_actual = cola_de_nodos.popleft()
            historial_expansion.append(nodo_actual)
            nodos_expandidos += 1

            if nodo_actual == self.metaQueso:
                encontro_meta = True
                break

            for mov_fila, mov_columna in MOVIMIENTOS_CARDINALES:
                fila_vecina = nodo_actual[0] + mov_fila
                columna_vecina = nodo_actual[1] + mov_columna
                nodo_vecino = (fila_vecina, columna_vecina)

                if 0 <= fila_vecina < total_filas and 0 <= columna_vecina < total_columnas:
                    if (
                        self.mapaLaberinto[fila_vecina][columna_vecina] == 0
                        and nodo_vecino not in nodos_visitados
                    ):
                        nodos_visitados.add(nodo_vecino)
                        registro_de_padres[nodo_vecino] = nodo_actual
                        cola_de_nodos.append(nodo_vecino)
                        nodos_generados += 1

        tiempo_total = perf_counter() - inicio_tiempo

        if encontro_meta:
            camino = reconstruir_ruta(registro_de_padres, self.inicioRaton, self.metaQueso)
            mensaje = "Solucion encontrada."
        else:
            camino = []
            mensaje = "No existe ruta desde el inicio hasta la meta."

        return ResultadoBusqueda(
            camino=camino,
            historial_expansion=historial_expansion,
            nodos_generados=nodos_generados,
            nodos_expandidos=nodos_expandidos,
            tiempo_segundos=tiempo_total,
            encontro_solucion=encontro_meta,
            mensaje=mensaje,
        )

    def BuscarCaminoCorto(self):
        """Compatibilidad con la version original: retorna solo la ruta final."""
        return self.Resolver().camino
