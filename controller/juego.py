from models.barco import *
from models.tablero import *
from colorama import Fore
import os
import numpy as np
import time
import random
from view.view import *


class Juego():
    
    def __init__(self, filas, columnas):
        '''
        Inicializamos las variables del juego, es decir, solo asignamos el número de filas y columnas para luego crear los tableros.
        '''
        self.filas = filas
        self.columnas = columnas
        self._reiniciar_juego()

    def _reiniciar_juego(self):
        '''Creamos los tableros nuevos y colocamos los barcos. 
        Si la llamamos al inicio de cada partida, garantizamos que se reinicie el juego.'''
        self.tablero_jugador = Tablero(self.filas, self.columnas)
        self.tablero_maquina = Tablero(self.filas, self.columnas)
        self.tablero_jugador.colocar_barcos()
        self.tablero_maquina.colocar_barcos()

        

    def _es_coordenada_valida(self, coordenada, tablero):
        """
        Valida que la coordenada sea del formato fila.columna
        y que esté dentro del rango del tablero dado.

        """
        # Verificar que la coordenada no esté vacía
        if not coordenada or coordenada.strip() == "":
            return (False, None)
        
        coordenada = coordenada.strip()  # Eliminar los espacios al inicio y al final
        
        # Verificar que tenga un punto
        if '.' not in coordenada:
            return (False, None)
        
        # Hacer split por el punto
        partes = coordenada.split('.')
        
        # Verificar que solo haya 2 partes para que no sea válido si insertan varios puntos
        if len(partes) != 2:
            return (False, None)
        
        fila, columna = partes
        
        # Verificar que la fila y columna sean digitos
        if not fila.isdigit() or not columna.isdigit():
            return (False, None)
        
        # Convertir a enteros
        fila_int = int(fila)
        columna_int = int(columna)
        
        # Verificar que las coordenadas estén dentro del tablero
        if not (0 <= fila_int < tablero.filas and 0 <= columna_int < tablero.columnas):
            return (False, None)
        
        # Si pasa todas las validaciones, retornar True y las coordenadas
        return (True, (fila_int, columna_int))


    def _turno_maquina(self):
        '''
        Ataque de la máquina: Se generan las coordenadas de manera aleatoria para fila y columna desde la 0 hasta la cantidad de las filas y columnas, con esto garantizamos que nunca se salga del tablero.
        Se ejecuta el ataque al tablero del jugador.
        Según el resultado del ataque, vuelve a generar una coordenada y a atacar o sencillamente se sale de la función.
        Según el resultado, se muestran los tableros actualizados con el mensaje correspondiente.
        Cada vez que se golpea un barco, se verifica si la flota del oponente fue hindida en su totalidad para dar fin al juego.
        '''
        mensaje = [Fore.RED + "Turno de la máquina..."]

        while True:
            ataque = (np.random.randint(0, self.tablero_jugador.filas), np.random.randint(0, self.tablero_jugador.columnas))
            resultado = self.tablero_jugador.gestionar_ataque(ataque) # Este es el ataque de la máquina se ataca al tablero del jugador

            if resultado == "TIEMPO_PERDIDO":
                continue # Si la máquina ya disparó ahí, no pierde el turno, simplemente vuelve a disparar hasta que acierte o falle en una casilla nueva. Por eso el continue, esto le dará un poco de ventaja a la máquina.
                # break  # Ya disparó ahí, intenta otra casilla
            if resultado == "GOLPEADO":
                if self.tablero_jugador.flotas_hundidas():
                    return "MAQUINA_GANA"
                mensaje.append(Fore.RED + f"La máquina disparó a {ataque}...\nTe ha Tocado un barco, la máquina vuelve disparar")
                # Mostramos ambos tableros actualizados con el ataque
                mostrar_tableros(self.tablero_jugador, self.tablero_maquina, mensaje)
                time.sleep(1)
                continue

            if resultado == "AGUA":
                mensaje.append(Fore.CYAN + f"Agua en {ataque}. Ahora es el turno del jugador")
                # Mostramos ambos tableros actualizados con el ataque
                mostrar_tableros(self.tablero_jugador, self.tablero_maquina, mensaje)
                time.sleep(1)
                return None
                

    def _turno_jugador(self ,*, demo = False):
        '''
        Ataque del jugador: Se le pide al jugador las coordenadas fila y columna en formato fila.columna.
        Luego esas coordenadas deben pasar ciertas validaciones (es_valida) para garantizar que sean aptas para usar la función "gestionar_ataque".
        Se ejecuta el ataque al tablero de la máquina.
        Según el resultado del ataque, el jugador podrá volver a tirar o no.
        Según el resultado, también se muestran los tableros actualizados con el mensaje correspondiente.
        Cada vez que se golpea un barco, se verifica si la flota del oponente fue hindida en su totalidad para dar fin al juego.
        '''

        mensaje = []
        while True:
            mostrar_tableros(self.tablero_jugador, self.tablero_maquina, mensaje)

            if not demo:
                coordenadas_ataque = input("Elige la coordenada a atacar, ej: 0.1 (o pulsa la letra 'q' para salir): ")
                
                if coordenadas_ataque.lower() == "q": # Si la letra es "q" se sale.
                    return "SALIR"
                es_valida, coordenadas = self._es_coordenada_valida(coordenadas_ataque, self.tablero_maquina) # Validamos la coordenada y la guardamos en una variable

                if not es_valida: # Si no es válida la coordenada, ejecutamos nuevamente todo lo anterior hasta que se digite una correcta
                    mensaje = [Fore.RED + f"Coordenada inválida. El formato admitido es fila.columna (0-{self.tablero_maquina.filas-1}), ejemplo: 1.2"]
                    continue
            else:
                # coordenadas = (np.random.randint(0, tablero_maquina.filas), np.random.randint(0, tablero_maquina.columnas))  
                coordenadas = (np.random.randint(0, self.tablero_maquina.filas), np.random.randint(0, self.tablero_maquina.columnas))  

            
            # En este punto ya sabemos que la coordenada es válida
            # Ejcutamos el ataque
            resultado = self.tablero_maquina.gestionar_ataque(coordenadas)

            if resultado == "TIEMPO_PERDIDO":
                mensaje = [Fore.YELLOW + f"Ya disparaste a {coordenadas}. Tiempo perdido!!!"]
                mostrar_tableros(self.tablero_jugador, self.tablero_maquina, mensaje)
                time.sleep(1)
                return None

            if resultado == "GOLPEADO":
                if self.tablero_maquina.flotas_hundidas():
                    return "JUGADOR_GANA"
                mensaje = [Fore.GREEN + f"Tocado en {coordenadas}. Puedes volver a disparar"]
                continue

            if resultado == "AGUA":
                mensaje = [Fore.CYAN + f"Agua en {coordenadas}. Ahora es el turno de la máquina"]
                mostrar_tableros(self.tablero_jugador, self.tablero_maquina, mensaje)
                time.sleep(1)
                return None


    def jugar(self):
        '''
        Se ejecuta mientrar que ninguna flota se haya hundido o si el usuario no ha ingresado "q"
        El primer bucle corresponde al menú inicial en donde se muestra si se quiere jugar o salir.
        Si se elige la opción 1 comienza el juego.
        Si se elige la opción 2 se sale del programa.
        '''
        # Bucle principal que mantiene el menú activo
        while True:
            mostrar_menu()
            opcion = input("Selecciona una opción (1-3): ")

            if opcion == "1":
                self._reiniciar_juego() # Al reiniciar el juego, se crean nuevos tableros y se colocan los barcos, así garantizamos que cada partida sea nueva.
                while True:
                    # Código del turno del jugador
                    resultado_jugador = self._turno_jugador(demo=False)
                    if resultado_jugador == "SALIR":
                        break
                    if resultado_jugador == "JUGADOR_GANA":
                        mostrar_tableros(self.tablero_jugador, self.tablero_maquina,
                            [Fore.GREEN + "Ganaste. Hundiste la flota del enemigo."])
                        input("Presiona Enter para volver al menú...")
                        limpiar_pantalla()
                        break

                    # Código del turno de la máquina
                    resultado_maquina = self._turno_maquina()
                    if resultado_maquina == "MAQUINA_GANA":
                        mostrar_tableros(self.tablero_jugador, self.tablero_maquina,
                            [Fore.RED + "Has perdido :( La máquina hundió tu flota."])
                        input("Presiona Enter para volver al menú principal...")
                        limpiar_pantalla()
                        break


            if opcion == "2":
                self._reiniciar_juego() # Al reiniciar el juego, se crean nuevos tableros y se colocan los barcos, así garantizamos que cada partida sea nueva.
                while True:
                    # Código del turno del jugador
                    resultado_jugador = self._turno_jugador(demo=True)
                    if resultado_jugador == "SALIR":
                        break
                    if resultado_jugador == "JUGADOR_GANA":
                        mostrar_tableros(self.tablero_jugador, self.tablero_maquina,
                            [Fore.GREEN + "Ganaste. Hundiste la flota del enemigo."])
                        input("Presiona Enter para volver al menú...")
                        limpiar_pantalla()
                        break

                    # Código del turno de la máquina
                    resultado_maquina = self._turno_maquina()
                    if resultado_maquina == "MAQUINA_GANA":
                        mostrar_tableros(self.tablero_jugador, self.tablero_maquina,
                            [Fore.RED + "Has perdido :( La máquina hundió tu flota."])
                        input("Presiona Enter para volver al menú principal...")
                        limpiar_pantalla()
                        break


                pass
            if opcion == "3":
                break