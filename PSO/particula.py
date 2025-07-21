from random import uniform
from collections.abc import Callable

class Particle:
    """
    Particle:
        Representa una partícula individual en el algoritmo PSO.
        Atributos:
            posicion: Lista con las coordenadas actuales de la partícula
            limites: Tupla con los límites del espacio de búsqueda
            funcion: Función objetivo a optimizar
            velocidad: Velocidad actual de la partícula
            mejor_pos_local: Mejor posición encontrada por esta partícula
            mejor_val_local: Mejor valor encontrado por esta partícula
        
        Métodos:
            mover(): Actualiza la posición de la partícula según su velocidad
            buscar_mejor_local(): Actualiza el mejor local si la posición actual es mejor
            cambiar_velocidad(): Ajusta la velocidad según factores cognitivos y sociales
        """
    def __init__(self, limites: tuple, posicion: list, funcion: Callable):
        self.posicion = posicion
        self.limites = limites
        self.funcion = funcion
        distribucion_velocidad = uniform(-abs(limites[0] - limites[1]), abs(limites[0] - limites[1]))
        self.velocidad = [distribucion_velocidad, distribucion_velocidad]
        self.mejor_pos_local = posicion.copy()
        self.mejor_val_local = funcion(*self.posicion)

    def mover(self):
        for i in range(len(self.posicion)):
            self.posicion[i] = self.posicion[i] + self.velocidad[i]
            if self.posicion[i] < self.limites[0]:
                self.posicion[i] = self.limites[0]
            elif self.posicion[i] > self.limites[1]:
                self.posicion[i] = self.limites[1]
                
    def buscar_mejor_local(self):
        mejor_val_local_posible = self.funcion(*self.posicion) 
        if mejor_val_local_posible < self.mejor_val_local:
            self.mejor_val_local = mejor_val_local_posible
            self.mejor_pos_local = self.posicion.copy()
        return self.mejor_pos_local, self.mejor_val_local
    
    def cambiar_velocidad(self, coeficiente_inercia:float ,parametro_cognitivo: float, parametro_social:float, mejor_pos_global:list):
        nueva_velocidad = []
        for i in range(len(self.velocidad)):
            r1 = uniform(0, 1)
            r2 = uniform(0, 1)
            cognitivo = parametro_cognitivo * r1 * (self.mejor_pos_local[i] - self.posicion[i])
            social = parametro_social * r2 * (mejor_pos_global[i] - self.posicion[i])
            nueva_velocidad.append(coeficiente_inercia * self.velocidad[i] + cognitivo + social)
        self.velocidad = nueva_velocidad