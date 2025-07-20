from random import uniform
from numpy import linspace, meshgrid, log10

from collections.abc import Callable
from matplotlib import pyplot


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
    
    def buscar_mejor_global(self):
        for particula in self.enjambre:
            if particula.buscar_mejor_local()[1] < self.mejor_val_global:
                self.mejor_val_global = particula.buscar_mejor_local()[1]
                self.mejor_pos_global = particula.buscar_mejor_local()[0].copy()

    def mostrar_enjambre2d(self, funcion, num_iteraciones:int, num_graficas:int, escala_log=True):
        # Crear la malla para la función de fondo (solo una vez)
        x = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
        y = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
        X, Y = meshgrid(x, y)
        Z = funcion(X, Y)   
        
        # Decidir qué escala usar
        if escala_log:
            Z_plot = log10(Z)
            label_escala = "Escala logarítmica"
            vmin, vmax = 0, 6
        else:
            Z_plot = Z
            label_escala = "Escala normal"
            vmin, vmax = Z.min(), Z.max()
        
        # Crear la figura y configurar el fondo
        fig, ax = pyplot.subplots(figsize=(10, 8))
        pyplot.ion()  # Activar modo interactivo después de crear la figura
        
        for i in range(num_iteraciones + 1):
            self.buscar_mejor_global()
            
            if i in [(num_iteraciones//num_graficas)*j for j in range(num_graficas + 1)] or num_graficas >= num_iteraciones:
                # Limpiar el axes
                ax.clear()
                
                # Redibujar el fondo
                im = ax.imshow(Z_plot, extent=[self.enjambre[0].limites[0], self.enjambre[0].limites[1], 
                                self.enjambre[0].limites[0], self.enjambre[0].limites[1]], 
                            origin='lower', cmap='viridis', vmin=vmin, vmax=vmax)
                ax.contour(X, Y, Z_plot, levels=15, colors='white', alpha=0.7, linewidths=1)
                
                # Graficar las partículas en sus nuevas posiciones
                for particula in self.enjambre:
                    ax.plot(*particula.posicion, "ro", markersize=8)
                
                ax.set_title(f"Iteracion {i}")
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                
                # Actualizar la pantalla
                fig.canvas.draw()
                fig.canvas.flush_events()
                pyplot.pause(0.1)  # Pausa para ver el movimiento
                
            self.cambiar_velocidades()
        
        # Agregar colorbar al final
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label(label_escala)
        pyplot.ioff()  # Desactivar modo interactivo
        pyplot.show(block=True)  # Mostrar y esperar a que se cierre

    def mostrar_enjambre3d(self, funcion, num_iteraciones:int, num_graficas:int, escala_log=True):
        # Crear la malla para la función de fondo (solo una vez)
        x = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
        y = linspace(self.enjambre[0].limites[0], self.enjambre[0].limites[1], 100)
        X, Y = meshgrid(x, y)
        Z = funcion(X, Y)   
        
        # Decidir qué escala usar
        if escala_log :
            Z_plot = log10(Z)
            titulo_base = "Goldstein-Price 3D (Log)"
        else:
            Z_plot = Z
            titulo_base = "Goldstein-Price 3D"

        # Crear figura y subplot 3D
        fig = pyplot.figure(figsize=(12, 10))
        pyplot.ion()  # Activar modo interactivo después de crear la figura
        
        for i in range(num_iteraciones + 1):
            self.buscar_mejor_global()
            
            if i in [(num_iteraciones//num_graficas)*j for j in range(num_graficas + 1)] or num_graficas >= num_iteraciones:
                # Limpiar la figura anterior
                fig.clear()
                ax = fig.add_subplot(111, projection='3d')
                
                # Graficar la superficie
                suprf = ax.plot_surface(X, Y, Z_plot, cmap="viridis", alpha=0.7)
                
                # Agregar las partículas
                for particula in self.enjambre:
                    parte_x, parte_y = particula.posicion
                    if escala_log and funcion(parte_x, parte_y) > 0:
                        parte_z = log10(funcion(parte_x, parte_y))
                    else:
                        parte_z = funcion(parte_x, parte_y)
                    ax.scatter([parte_x], [parte_y], [parte_z], color='red', s=100)
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('log10(Z)' if escala_log else 'Z')
                ax.set_title(f'{titulo_base} - Iteración {i}')
                
                # Agregar colorbar solo en la última iteración para evitar problemas
                if i == num_iteraciones:
                    fig.colorbar(suprf, ax=ax, shrink=0.5)
                
                # Actualizar la pantalla
                fig.canvas.draw()
                fig.canvas.flush_events()
                pyplot.pause(0.2)  # Pausa para ver el movimiento
                
            self.cambiar_velocidades()
        
        pyplot.ioff()  # Desactivar modo interactivo
        pyplot.show(block=True)  # Mostrar y esperar a que se cierre

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
    
    # Mostrar en escala logarítmica
    prueba.mostrar_enjambre2d(goldstein_price, 150, 50, escala_log=True)
    
    limites_prueba = (-2, 2)
    enjambre = crear_enjambre(20, limites_prueba, goldstein_price)
    prueba = Swarm(enjambre)
    prueba.mostrar_enjambre3d(goldstein_price, 200, 50, escala_log=True)
    print(f"Optimizacion: {prueba.mejor_val_global:.3f},\nPosicion:", end=" ")
    print([f"{i:.3f}" for i in prueba.mejor_pos_global])