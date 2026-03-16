import os
from colorama import Fore


def limpiar_pantalla():
    # Windows → cls    |   Linux/Mac → clear
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n--- MENÚ DE JUEGO ---")
    print("1. Iniciar Juego. (Para salir puedes ingresar la letra \"q\"))")
    print("2. ¿Quieres ver un ejemplo de la dinámica del juego?")
    print("3. Salir")

def mostrar_tableros(tablero_jugador, tablero_maquina, mensaje=None):
    limpiar_pantalla()
    print(Fore.BLUE + "*"*23, "Mi Tablero", "*"*23)
    print()
    tablero_jugador.imprimir_tablero(oculto = False)
    print()
    print(Fore.YELLOW + "*"*20, "Tablero Enemigo", "*"*20)
    print()
    tablero_maquina.imprimir_tablero(oculto = True)
    # tablero_maquina.imprimir_tablero_oculto(True)
    print()
    # Imprimimos debajo del tablero los mensajes según los resultados del ataque
    if mensaje:
        print("-" * 50)
        for m in mensaje:
            print(m)
        print()