from random import uniform
from collections.abc import Callable

from PSO.particula import Particle


class Swarm:
    """
    Swarm:
        Representa el enjambre completo de partículas y coordina el algoritmo PSO.
        Atributos:
            enjambre: Lista de varios objetos denominados Particle
            mejor_pos_global: Mejor posición encontrada por todo el enjambre
            mejor_val_global: Mejor valor encontrado por todo el enjambre
            coeficiente_inercia: Factor de inercia para el cálculo de velocidad
            parametro_cognitivo: Factor cognitivo para el cálculo de velocidad
            parametro_social: Factor social para el cálculo de velocidad
        
        Métodos:
            cambiar_velocidades(): Actualiza velocidades de todas las partículas
            buscar_mejor_global(): Encuentra la mejor solución global del enjambre
    """
    def __init__(self, enjambre: list[Particle], coeficiente_inercia = 0.7, parametro_cognitivo =2, parametro_social = 2): 
        self.enjambre = enjambre
        self.mejor_pos_global = []
        self.mejor_val_global = float('inf')
        self.coeficiente_inercia = coeficiente_inercia
        self.parametro_cognitivo = parametro_cognitivo
        self.parametro_social = parametro_social

    def cambiar_velocidades(self):
        for particula in self.enjambre:
            particula.cambiar_velocidad(self.coeficiente_inercia, self.parametro_cognitivo, self.parametro_social, self.mejor_pos_global)
            particula.mover()
    
    def buscar_mejor_global(self):
        for particula in self.enjambre:
            if particula.buscar_mejor_local()[1] < self.mejor_val_global:
                self.mejor_val_global = particula.buscar_mejor_local()[1]
                self.mejor_pos_global = particula.buscar_mejor_local()[0].copy()

def crear_enjambre(num_particulas: int, limites: tuple, funcion: Callable):
        return [Particle(
                    limites, 
                    [uniform(limites[0], limites[1]), 
                     uniform(limites[0], limites[1])], funcion) 
                for i in range(num_particulas+1)]
"""
 crear_enjambre(num_particulas, limites, funcion):
        Crea un enjambre de partículas con posiciones aleatorias.
        Args:
            num_particulas: Número de partículas a crear
            limites: Tupla con los límites del espacio de búsqueda
            funcion: Función objetivo a optimizar
        Returns:
            Lista de objetos Particle inicializados aleatoriamente
"""