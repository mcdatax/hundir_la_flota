import numpy as np
import random
from models.barco import Barco
from colorama import Fore

class Tablero():
    '''
    Clase Tablero: El tablero que albergará las coordenadas totales válidas

    Parámetros:
        columnas (int): Filas totales del tablero
        posicion (int) = Columnas totales del tablero
        cuadricula (numpy array) = Cuadricula del tablero
        cuadricula_temp (numpy array) = 
        flota (lista) = Lista con los objetos Barcos
    '''


    def __init__(self, filas=10, columnas=10):
        self.filas = filas
        self.columnas = columnas
        self.cuadricula = np.full((filas,columnas),"_")
        # self.cuadricula_temp = []
        self.flota = []
    
    def _actualiza_cuadricula(self, coordenadas, caracter):
        self.cuadricula[coordenadas] = caracter

    def _generar_posicion(self, barco):
        '''
        Genramos de forma aleatoria las posiciones de los barcos en el tablero
        '''

        pieza_original = (random.randint(0,self.filas -1),random.randint(0, self.columnas -1)) # Al usar el random de python, se debe restar 1 porque no es inclusive y si no se hace se sale del rango
        barco.posicion.append(pieza_original) # Ya tenemos una posición inicial aleatoria para poder luego validar si podemos colocar un barco
        orientacion = random.choice(["N","S","O","E"])
        fila = pieza_original[0]
        columna = pieza_original[1]
        for i in range(barco.eslora -1):
            if orientacion == "N":
                fila -= 1
            elif orientacion  == "S":
                fila += 1
            elif orientacion == "E":
                columna += 1
            else:
                columna -= 1
            barco.posicion.append((fila,columna))

    def _validar_y_colocar(self, barco):
        '''
        Validamos si la posición de un barco es válida parea la cuadrícula que se tiene
        '''
        tablero_temp = self.cuadricula.copy() # hago una copia de mi cuadrícula para no romper mi original
        
        for posicion in barco.posicion: # Recorremos cada tupla de coordenadas del barco
            fila = posicion[0] # La posición 0 de la tupla contiene la fila
            columna = posicion[1] # La posición 1 de la tupla contiene la columna
            if fila < 0 or fila >= self.filas: # Si la fila es negativa ó la fila es mayor al tamaño máximo de la variable filas de la instancia, entonces NO es válida.
                return False
            if columna < 0 or columna >= self.columnas: # Si la columna es negativa ó la columna es mayor al tamaño máximo de la variable columnas de la instancia, entonces NO es válida.
                return False
            if self.cuadricula[posicion] == "█": # si la tupla posicion (coordenada) tiene de valor █, es porque allí hay un trozo de barco, entonces NO es válida.
                return False
            tablero_temp[posicion] = "█" # Si pasa todas las validaciones anteriores, la posición es válida y asigna el █ en esa posición de la cuadrícula

        # Ahora si estamos seguros y modificamos nuestra cuadrícula    
        self.cuadricula = tablero_temp
        # self.cuadricula_inicial = np.where(self.cuadricula == "O", "█", "~")

        return True


    def colocar_barcos(self): 
        '''
        Creará una lista con los barcos recién creados, en este caso, sólo se conoce el eslora de cada uno y siempre son 6 barcos.        
        '''
        barcos = [Barco(eslora) for eslora in [2, 2, 2, 3, 3, 4]]
        for barco in barcos:
            # Por cada barco que encuentra, intentará generar una posición, luego validar la posición y si todo sale bien agrega el barco a la flota.
            # En de que validar_y_colocar barco no sea exitoso, volverá al inicio del While y limpiará barco.posicion (reinicio) para que no haya "residuos" de lo que intentó con las coordenadas anteriores. 
            # Recordemos que en _generar_posicion se hizo una asignación de barco.posicion.append((fila,columna))
            # Intentará tantas veces como sea necesario hasta colocar cada barco.
            while True:
                barco.posicion = []
                self._generar_posicion(barco)
                if self._validar_y_colocar(barco):
                    self.flota.append(barco)
                    break

    def gestionar_ataque(self, coordenadas):
        '''
        Simplemente gestionamos el ataque con el barco y actualizamos la cuadrícula según el resultado del ataque que nos diga el barco
        '''
        
        if self.cuadricula[coordenadas] in ("X", "|"):
            return "TIEMPO_PERDIDO"
        else:
            for barco in self.flota:
                resultado = barco.recibir_ataque(coordenadas)
                if resultado[0] == "GOLPEADO":
                    self._actualiza_cuadricula(coordenadas, "X")
                    return "GOLPEADO"
            self._actualiza_cuadricula(coordenadas, "|")
            return "AGUA"

    def imprimir_tablero(self,*, oculto = False):
        if oculto:
            # Crear vista temporal: ocultar barcos pero mostrar disparos
            cuadricula_oculta = np.where(self.cuadricula == "█", "_", self.cuadricula)
            print(Fore.BLUE + f' {cuadricula_oculta}')
            return None
        print(Fore.BLUE + f' {self.cuadricula}')


    def imprimir_tablero_oculto(self):
        # Crear vista temporal: ocultar barcos pero mostrar disparos
        cuadricula_oculta = np.where(self.cuadricula == "█", "_", self.cuadricula)
        print(Fore.BLUE + f' {cuadricula_oculta}')

    def flotas_hundidas(self):
        # En la siguiente línea recorremos lkos barcos de la flota y, si todos en su estado son "Hundido" es porque la flota fue hundida. 
        # La built-in function "all" es la que hace que sea True si la condición comentada en la línea anterior se cumple en su totalidad.
        return all(barco.estado == "Hundido" for barco in self.flota) # Si todos los barcos están hundidos, el all retornará True
    

