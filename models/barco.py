from colorama import Fore

class Barco:
    '''
    Clase Barco: Aquí se almacenan todos lo atributos y métodos del barco.

    Parámetros:
        eslora (int): Eslora del barco
        posicion (list) = Lista de tuplas de las coordenadas que ocupa el barco en el tablero
        golpes (list) = Lista de tuplas de las coordenadas de los golpes que tiene el barco
    '''

    def __init__(self, eslora):
        self.eslora = eslora
        self.posicion = []
        self.golpes = []

    
    @property
    def estado(self):
        if len(self.golpes) == 0:
            return "Operativo"
        elif len(self.golpes) == self.eslora:
            return "Hundido"
        else:
            return "Tocado"
            
    def recibir_ataque(self, coordenadas):
        if coordenadas in self.posicion:
            self.golpes.append(coordenadas)
            return ("GOLPEADO","Barco golpeado")
        return ("AGUA", "Disparo al agua")