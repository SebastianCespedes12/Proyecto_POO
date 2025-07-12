from random import uniform
from collections.abc import Callable
from matplotlib import pyplot
from numpy import linspace, meshgrid, log10


class Particle:
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

class Swarm:
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
    
    def buscar_mejor_global(self, funcion):
        for particula in self.enjambre:
            if particula.buscar_mejor_local(funcion)[1] < self.mejor_val_global:
                self.mejor_val_global = particula.buscar_mejor_local(funcion)[1]
                self.mejor_pos_global = particula.buscar_mejor_local(funcion)[0].copy()

    def mostrar_enjambre2d(self, funcion, num_iteraciones:int, num_graficas:int):
        for i in range(num_iteraciones + 1):
            self.buscar_mejor_global(funcion)
            if i in [(num_iteraciones//num_graficas)*i for i in range(num_graficas + 1)]:
                # Crear la malla para la función de fondo
                x = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
                y = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
                X, Y = meshgrid(x, y)
                Z = funcion(X, Y)   
                #Escala logaritmica
                Z_log = log10(Z)
                    
                # Crear la figura 
                im = pyplot.imshow(Z_log, extent=[self.enjambre[0].limites[0], self.enjambre[0].limites[1], 
                                self.enjambre[0].limites[0], self.enjambre[0].limites[1]], 
                            origin='lower', cmap='viridis', vmin=0, vmax=6)
                
                # Agregar líneas de contorno
                Q = pyplot.contour(X, Y, Z_log, levels=15, colors='white', alpha=0.7, linewidths=1)
                
                #Colorbar con etiquetas logarítmicas
                cbar = pyplot.colorbar(im)
                cbar.set_label("Escala logaritmica")

                # Graficar las partículas encima
                for particula in self.enjambre:
                    pyplot.plot(*particula.posicion, "ro", markersize=8)
                    pyplot.title(f"Iteracion {i}")
                    
                pyplot.xlabel('x')
                pyplot.ylabel('y')
                pyplot.show()
            self.cambiar_velocidades()

    def mostrar_enjambre3d(self, funcion, num_iteraciones:int, num_graficas:int):
        for i in range(num_iteraciones + 1):
            self.buscar_mejor_global(funcion)
            if i in [(num_iteraciones//num_graficas)*i for i in range(num_graficas + 1)]:
                x = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
                y = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
                X, Y = meshgrid(x, y)
                Z = funcion(X, Y)   
                Z_log = log10(Z)

                # Crear figura y subplot 3D
                fig = pyplot.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, projection='3d')
                
                # Graficar la superficie
                suprf = ax.plot_surface(X, Y, Z_log, cmap="viridis", alpha=0.8)
                
                # Agregar las partículas
                for particula in self.enjambre:
                    parte_x, parte_y = particula.posicion
                    parte_z = log10(funcion(parte_x, parte_y))
                    ax.scatter([parte_x], [parte_y], [parte_z], color='red', s=80)
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('log10(Z)')
                ax.set_title(f'Goldstein-Price 3D - Iteración {i}')
                fig.colorbar(suprf, ax=ax, shrink=0.5)
                pyplot.show()
            self.cambiar_velocidades()

def goldstein_price(x, y):
    term1 = 1 + (x + y + 1)**2 * (19 - 14*x + 3*x**2 - 14*y + 6*x*y + 3*y**2)
    term2 = 30 + (2*x - 3*y)**2 * (18 - 32*x + 12*x**2 + 48*y - 36*x*y + 27*y**2)
    return term1 * term2

def crear_enjambre(num_particulas: int, limites: tuple, funcion: Callable):
        return [Particle(limites, [uniform(limites[0], limites[1]), uniform(limites[0], limites[1])], funcion) for i in range(num_particulas+1)]

   
if __name__ == "__main__":

    limites_prueba = (-2, 2)
    enjambre = crear_enjambre(20, limites_prueba, goldstein_price)
    prueba = Swarm(enjambre)
    prueba.mostrar_enjambre2d(goldstein_price, 200, 4)
    print(f"Optimizacion: {prueba.mejor_val_global:.3f},\nPosicion:", end=" ")
    print([f"{i:.3f}" for i in prueba.mejor_pos_global])
