# Raton y Laberinto (IA)

Prototipo en Python + Tkinter para comparar dos estrategias de busqueda en un laberinto 15x15:
- Busqueda en Amplitud (BFS)
- Busqueda Voraz (Greedy Best-First) con heuristica Manhattan

El agente (raton) parte de `(0, 0)` y debe llegar a la meta (queso) en la esquina inferior derecha.

## Requisitos
- Python 3.10+
- Dependencias de `requirements.txt`

## Instalacion
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecucion
Desde la raiz del proyecto:
```powershell
python .\RatonEnLaberinto\InterfazCarrera.py
```

## Uso basico
1. Se carga el laberinto actual en ambos paneles.
2. Presiona **Iniciar Busqueda** para ejecutar BFS y Voraz sobre el mismo mapa.
3. Presiona **Siguiente Laberinto** para cambiar de escenario.

## Estructura
- `RatonEnLaberinto/InterfazCarrera.py`: interfaz y animacion comparativa.
- `RatonEnLaberinto/LogicaAmplitud.py`: algoritmo BFS y metricas.
- `RatonEnLaberinto/LogicaVoraz.py`: algoritmo Voraz (Manhattan) y metricas.
- `RatonEnLaberinto/BusquedaBase.py`: validaciones, constantes comunes y resultado de busqueda.
- `RatonEnLaberinto/BibliotecaLaberintos.py`: 5 laberintos fijos de 15x15.
- `imagenes/`: recursos visuales (raton y queso).
