from __future__ import annotations

import heapq
from time import perf_counter
from typing import Dict, Set

from BusquedaBase import (
    MOVIMIENTOS_CARDINALES,
    ErrorEscenario,
    Posicion,
    ResultadoBusqueda,
    reconstruir_ruta,
    validar_escenario,
)


class SolucionadorVoraz:
    def __init__(self, mapaLaberinto, inicioRaton: Posicion, metaQueso: Posicion):
        self.mapaLaberinto = mapaLaberinto
        self.inicioRaton = inicioRaton
        self.metaQueso = metaQueso

    def CalcularHeuristica(self, nodoActual: Posicion) -> int:
        """Distancia Manhattan al nodo meta."""
        distancia_fila = abs(nodoActual[0] - self.metaQueso[0])
        distancia_columna = abs(nodoActual[1] - self.metaQueso[1])
        return distancia_fila + distancia_columna

    def Resolver(self) -> ResultadoBusqueda:
        """Ejecuta Busqueda Voraz (Greedy Best-First Search)."""
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

        cola_de_prioridad: list[tuple[int, Posicion]] = []
        heuristica_inicial = self.CalcularHeuristica(self.inicioRaton)
        heapq.heappush(cola_de_prioridad, (heuristica_inicial, self.inicioRaton))

        nodos_visitados: Set[Posicion] = {self.inicioRaton}
        registro_de_padres: Dict[Posicion, Posicion] = {}
        historial_expansion: list[Posicion] = []

        nodos_generados = 1
        nodos_expandidos = 0
        encontro_meta = False

        total_filas = len(self.mapaLaberinto)
        total_columnas = len(self.mapaLaberinto[0])

        while cola_de_prioridad:
            _, nodo_actual = heapq.heappop(cola_de_prioridad)
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

                        heuristica_vecino = self.CalcularHeuristica(nodo_vecino)
                        heapq.heappush(cola_de_prioridad, (heuristica_vecino, nodo_vecino))
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

    def BuscarCaminoVoraz(self):
        """Compatibilidad con la version original: retorna solo la ruta final."""
        return self.Resolver().camino
