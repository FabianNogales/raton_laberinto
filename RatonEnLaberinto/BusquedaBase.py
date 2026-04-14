from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

Posicion = Tuple[int, int]
MOVIMIENTOS_CARDINALES: Tuple[Posicion, ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


@dataclass(slots=True)
class ResultadoBusqueda:
    camino: List[Posicion]
    historial_expansion: List[Posicion]
    nodos_generados: int
    nodos_expandidos: int
    tiempo_segundos: float
    encontro_solucion: bool
    mensaje: str

    @property
    def longitud_ruta(self) -> int:
        return len(self.camino)

    @property
    def costo_total(self) -> int:
        if not self.encontro_solucion or not self.camino:
            return 0
        return len(self.camino) - 1


class ErrorEscenario(ValueError):
    """Se lanza cuando el mapa o las posiciones no son validas."""


def validar_escenario(
    mapa_laberinto: Sequence[Sequence[int]], inicio_raton: Posicion, meta_queso: Posicion
) -> None:
    if not mapa_laberinto or not mapa_laberinto[0]:
        raise ErrorEscenario("El mapa del laberinto esta vacio.")

    total_filas = len(mapa_laberinto)
    total_columnas = len(mapa_laberinto[0])

    if any(len(fila) != total_columnas for fila in mapa_laberinto):
        raise ErrorEscenario("El mapa del laberinto no es rectangular.")

    def _en_limites(posicion: Posicion) -> bool:
        fila, columna = posicion
        return 0 <= fila < total_filas and 0 <= columna < total_columnas

    if not _en_limites(inicio_raton):
        raise ErrorEscenario("La posicion inicial esta fuera de los limites del mapa.")

    if not _en_limites(meta_queso):
        raise ErrorEscenario("La posicion meta esta fuera de los limites del mapa.")

    if mapa_laberinto[inicio_raton[0]][inicio_raton[1]] != 0:
        raise ErrorEscenario("La posicion inicial esta sobre una pared.")

    if mapa_laberinto[meta_queso[0]][meta_queso[1]] != 0:
        raise ErrorEscenario("La posicion meta esta sobre una pared.")


def reconstruir_ruta(
    registro_de_padres: Dict[Posicion, Posicion], inicio_raton: Posicion, meta_queso: Posicion
) -> List[Posicion]:
    ruta_completa: List[Posicion] = []
    nodo_actual = meta_queso

    while True:
        ruta_completa.append(nodo_actual)
        if nodo_actual == inicio_raton:
            break
        nodo_actual = registro_de_padres[nodo_actual]

    ruta_completa.reverse()
    return ruta_completa
