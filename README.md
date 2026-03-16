# Hundir la Flota

Juego de Hundir la Flota por consola desarrollado en Python como proyecto académico.

## Instalación

Requisitos previos: tener **Python 3.10+** instalado.

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd "Hundir la flota"

# 2. Crear y activar el entorno virtual
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Cómo ejecutarlo

```bash
python main.py
```

O usando el ejecutable generado (no requiere Python):

```bash
./dist/HundirLaFlota
```

## Arquitectura: MVC

El proyecto está organizado siguiendo el patrón **Modelo-Vista-Controlador**:

```
models/      → Barco, Tablero (datos y lógica del juego)
view/        → Pintado del tablero en consola
controller/  → Juego (coordina modelos y vista)
main.py      → Punto de entrada
```

## Paradigma: POO

Se usó **Programación Orientada a Objetos**. Las clases principales son:

- `Barco` — eslora, posición, golpes recibidos y estado (`Operativo / Tocado / Hundido`)
- `Tablero` — cuadrícula numpy, flota de barcos, gestión de ataques
- `Juego` — turno del jugador, turno de la máquina, lógica de victoria

## Dependencias

| Librería | Uso |
|---|---|
| `numpy` | Cuadrícula del tablero y coordenadas aleatorias |
| `colorama` | Colores en la consola |

## Modos de juego

- **Opción 1** — Jugar contra la máquina
- **Opción 2** — Demo automática (ambos jugadores son la máquina)
- **Opción 3** — Salir
