from collections import deque

class SolucionadorAmplitud:
    def __init__(self, mapaLaberinto, inicioRaton, metaQueso):
        self.mapaLaberinto = mapaLaberinto
        self.inicioRaton = inicioRaton
        self.metaQueso = metaQueso
        self.totalFilas = len(mapaLaberinto)
        self.totalColumnas = len(mapaLaberinto[0])

    def BuscarCaminoCorto(self):
        """
        Ejecuta la Búsqueda en Amplitud (BFS) para encontrar la ruta más corta.
        """
        colaDeNodos = deque([self.inicioRaton])
        nodosVisitados = {self.inicioRaton}
        registroDePadres = {}
        
        # Direcciones: Arriba, Abajo, Izquierda, Derecha
        movimientosPosibles = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        seEncontroMeta = False

        while colaDeNodos:
            nodoActual = colaDeNodos.popleft()

            # Test de Meta
            if nodoActual == self.metaQueso:
                seEncontroMeta = True
                break

            # Expandir vecinos
            for movimiento in movimientosPosibles:
                filaVecina = nodoActual[0] + movimiento[0]
                columnaVecina = nodoActual[1] + movimiento[1]
                nodoVecino = (filaVecina, columnaVecina)

                # Validar límites de la matriz 10x10
                if 0 <= filaVecina < self.totalFilas and 0 <= columnaVecina < self.totalColumnas:
                    # Validar que sea camino (0) y no se haya visitado antes
                    if self.mapaLaberinto[filaVecina][columnaVecina] == 0 and nodoVecino not in nodosVisitados:
                        nodosVisitados.add(nodoVecino)
                        registroDePadres[nodoVecino] = nodoActual
                        colaDeNodos.append(nodoVecino)

        if seEncontroMeta:
            return self.ReconstruirRutaFinal(registroDePadres)
        else:
            return []

    def ReconstruirRutaFinal(self, registroDePadres):
        """
        Traza el camino de regreso desde el queso hasta el ratón.
        """
        rutaCompleta = []
        nodoActual = self.metaQueso

        while nodoActual != self.inicioRaton:
            rutaCompleta.append(nodoActual)
            nodoActual = registroDePadres.get(nodoActual)

        rutaCompleta.append(self.inicioRaton)
        rutaCompleta.reverse() # Invertir para que empiece desde el inicio
        return rutaCompleta
