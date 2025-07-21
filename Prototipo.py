import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from time import sleep

from random import uniform
from numpy import linspace, meshgrid, log10

from collections.abc import Callable
from matplotlib import pyplot
from funciones import dic_funciones, nombres_funciones, get_funcion, get_limites


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

class OptimizationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('PSO Animado - Prototipo')
        self.root.geometry('1000x800')
        
        # Variables de estado
        self.swarm = None
        self.is_animating = False
        
        # Variables de GUI - PSO
        self.pso_function_var = tk.StringVar(value="Goldstein-Price")
        self.num_particles_var = tk.IntVar(value=20)
        self.num_iterations_var = tk.IntVar(value=100)
        self.inertia_var = tk.DoubleVar(value=0.7)
        self.cognitive_var = tk.DoubleVar(value=2.0)
        self.social_var = tk.DoubleVar(value=2.0)
        self.viz_type_var = tk.StringVar(value="2D")
        self.escala_log_var = tk.BooleanVar(value=True)
        
        # Variables de GUI - Widgets
        self.pso_function_combo = None
        self.escala_log_check = None
        self.viz_type_combo = None
        self.animate_button = None
        self.results_text = None
        self.pso_figure = None
        self.pso_canvas = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack()

        # Panel de controles PSO
        pso_control_frame = ttk.LabelFrame(main_frame, text="Configuración PSO")
        pso_control_frame.pack()

        self.setup_pso_controls(pso_control_frame)

        # Frame para resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados")
        results_frame.pack()

        self.results_text = tk.Text(results_frame, height=4, width=50)
        self.results_text.pack()

        # Frame para el gráfico PSO
        pso_plot_frame = ttk.Frame(main_frame)
        pso_plot_frame.pack()

        # Canvas para matplotlib PSO
        self.pso_figure = Figure(figsize=(10, 6), dpi=100)
        self.pso_canvas = FigureCanvasTkAgg(self.pso_figure, pso_plot_frame)
        self.pso_canvas.get_tk_widget().pack()
        
    def setup_pso_controls(self, parent):
        # fila 0: Función y límites
        ttk.Label(parent, text="Función:").grid(row=0, column=0)
        self.pso_function_combo = ttk.Combobox(parent, textvariable=self.pso_function_var, values=nombres_funciones(), state="readonly")
        self.pso_function_combo.grid(row=0, column=1)

        # Fila 1: Parámetros PSO
        ttk.Label(parent, text="Partículas:").grid(row=1, column=0)
        ttk.Spinbox(parent, from_=5, to=100, textvariable=self.num_particles_var, width=8).grid(row=1, column=1)

        ttk.Label(parent, text="Iteraciones:").grid(row=1, column=2)
        ttk.Spinbox(parent, from_=10, to=500, textvariable=self.num_iterations_var, width=8).grid(row=1, column=3)

        # Fila 2: Parámetros PSO avanzados
        ttk.Label(parent, text="Inercia:").grid(row=2, column=0)
        ttk.Spinbox(parent, from_=0.1, to=2.0, increment=0.1, textvariable=self.inertia_var, width=8).grid(row=2, column=1)

        ttk.Label(parent, text="Cognitivo:").grid(row=2, column=2)
        ttk.Spinbox(parent, from_=0.5, to=5.0, increment=0.1, textvariable=self.cognitive_var, width=8).grid(row=2, column=3)

        ttk.Label(parent, text="Social:").grid(row=2, column=4)
        ttk.Spinbox(parent, from_=0.5, to=5.0, increment=0.1, textvariable=self.social_var, width=8).grid(row=2, column=5)

        # Fila 3: Tipo de visualización
        ttk.Label(parent, text="Visualización:").grid(row=3, column=0)
        self.viz_type_combo = ttk.Combobox(parent, textvariable=self.viz_type_var, values=["2D", "3D"], state="readonly")
        self.viz_type_combo.grid(row=3, column=1)

        # Checkbox para escala logarítmica
        self.escala_log_check = ttk.Checkbutton(parent, text="Escala logarítmica", variable=self.escala_log_var)
        self.escala_log_check.grid(row=3, column=2)

        # Row 4: Botón de animación
        self.animate_button = ttk.Button(parent, text="Iniciar Animación PSO", command=self.animate_pso)
        self.animate_button.grid(row=4, column=0)
  
    
    def animate_pso(self):
        if self.is_animating:
            self.is_animating = False
            self.animate_button.config(text="Iniciar Animación PSO")
            return
            
        self.is_animating = True
        self.animate_button.config(text="Detener Animación")
        

        # Obtener parámetros PSO
        function_name = self.pso_function_var.get()
        funcion = get_funcion(function_name)
        num_particles = self.num_particles_var.get()
        num_iterations = self.num_iterations_var.get()
        limites = get_limites(function_name)
        viz_type = self.viz_type_var.get()
        use_escala_log = self.escala_log_var.get()

        inertia = self.inertia_var.get()
        cognitivo = self.cognitive_var.get()
        social = self.social_var.get()
        
        # Crear enjambre usando la función existente
        enjambre = crear_enjambre(num_particles, limites, funcion)
        self.swarm = Swarm(enjambre, inertia, cognitivo, social)
        
        # Usar los métodos existentes de Swarm adaptados para GUI
        if viz_type == "2D":
            self.mostrar_enjambre_2d(funcion, num_iterations, use_escala_log)
        else:
            self.mostrar_enjambre_3d(funcion, num_iterations, use_escala_log)
    
    def mostrar_enjambre_2d(self, funcion, num_iteraciones, escala_log=True):
        # Crear la malla para la función de fondo (solo una vez)
        x = linspace(self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1], 100)
        y = linspace(self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1], 100)
        X, Y = meshgrid(x, y)
        Z = funcion(X, Y)   
        
        # Decidir qué escala usar
        if escala_log and (Z > 0).all():
            Z_plot = log10(Z)
            label_escala = "Escala logarítmica"
            vmin, vmax = 0, 6
        else:
            Z_plot = Z
            label_escala = "Escala normal"
            vmin, vmax = Z.min(), Z.max()
        
        # Animación adaptada para GUI
        for i in range(num_iteraciones + 1):
            if not self.is_animating:
                break
                
            self.swarm.buscar_mejor_global()
            
            if i % 3 == 0:  # Actualizar cada 3 iteraciones para GUI
                # Limpiar figura
                self.pso_figure.clear()
                ax = self.pso_figure.add_subplot(111)
                
                # Redibujar el fondo
                im = ax.imshow(Z_plot, extent=[self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1], 
                                self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1]], 
                            origin='lower', cmap='viridis', vmin=vmin, vmax=vmax)
                ax.contour(X, Y, Z_plot, levels=15, colors='white', alpha=0.7, linewidths=1)
                
                # Graficar las partículas en sus nuevas posiciones
                for particula in self.swarm.enjambre:
                    ax.plot(*particula.posicion, "ro", markersize=6)
                
                
                ax.set_title(f"Iteración {i} - Mejor: {self.swarm.mejor_val_global:.6f}")
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                
                # Actualizar la pantalla GUI
                self.pso_canvas.draw()
                self.root.update()
                sleep(0.05)
                
            self.swarm.cambiar_velocidades()
        
        # Finalizar animación
        self.termina_animacion(funcion, Z_plot, X, Y, escala_log, "2D", label_escala)
    
    def mostrar_enjambre_3d(self, funcion, num_iteraciones, escala_log=True):
        # Crear la malla para la función de fondo 
        x = linspace(self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1], 100)
        y = linspace(self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1], 100)
        X, Y = meshgrid(x, y)
        Z = funcion(X, Y)   
        
        # Decidir qué escala usar
        if escala_log and (Z > 0).all():
            Z_plot = log10(Z)
            titulo_base = "Escala logarítmica"
        else:
            Z_plot = Z
            titulo_base = "Escala normal"
        
        # Animación 3D adaptada para GUI
        for i in range(num_iteraciones + 1):
            if not self.is_animating:
                break
                
            self.swarm.buscar_mejor_global()
            
            if i % 5 == 0:  # Actualizar cada 5 iteraciones para 3D
                # Limpiar la figura anterior
                self.pso_figure.clear()
                ax = self.pso_figure.add_subplot(111, projection='3d')
                
                # Graficar la superficie
                suprf = ax.plot_surface(X, Y, Z_plot, cmap="viridis", alpha=0.7)
                
                # Agregar las partículas
                for particula in self.swarm.enjambre:
                    parte_x, parte_y = particula.posicion
                    if escala_log and funcion(parte_x, parte_y) > 0:
                        parte_z = log10(funcion(parte_x, parte_y))
                    else:
                        parte_z = funcion(parte_x, parte_y)
                    ax.scatter([parte_x], [parte_y], [parte_z], color='red', s=80)
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('log10(Z)' if escala_log else 'Z')
                ax.set_title(f'{titulo_base} - Iteración {i}\nMejor: {self.swarm.mejor_val_global:.6f}')
                
                # Actualizar la pantalla GUI
                self.pso_canvas.draw()
                self.root.update()
                sleep(0.1)
                
            self.swarm.cambiar_velocidades()
        
        # Finalizar animación 3D
        self.termina_animacion(funcion, Z_plot, X, Y, escala_log, "3D", titulo_base)
    
    def termina_animacion(self, funcion, Z_plot, X, Y, escala_log, viz_type, label_escala):
        self.is_animating = False
        self.animate_button.config(text="Iniciar Animación PSO")
        
        function_name = self.pso_function_var.get()
        
        # Mostrar resultados finales
        if self.swarm.mejor_pos_global:
            resultado = f"Función: {function_name}\n"
            resultado += f"Mejor valor: {self.swarm.mejor_val_global:.6f}\n"
            resultado += f"Mejor posición: [{self.swarm.mejor_pos_global[0]:.6f}, {self.swarm.mejor_pos_global[1]:.6f}]\n"
            resultado += f"Visualización: {viz_type}"
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, resultado)
            
            # Gráfico final adaptado
            self.mostrar_grafica_final(funcion, Z_plot, X, Y, escala_log, viz_type, label_escala)
    
    def mostrar_grafica_final(self, funcion, Z_plot, X, Y, escala_log, viz_type, label_escala):
        self.pso_figure.clear()
        
        if viz_type == "2D":
            ax = self.pso_figure.add_subplot(111)
            
            # Redibujar el fondo final
            im = ax.imshow(Z_plot, extent=[self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1], 
                            self.swarm.enjambre[0].limites[0], self.swarm.enjambre[0].limites[1]], 
                        origin='lower', cmap='viridis')
            ax.contour(X, Y, Z_plot, levels=15, colors='white', alpha=0.7, linewidths=1)
            
            # Partículas finales
            for particula in self.swarm.enjambre:
                ax.plot(*particula.posicion, "ro", markersize=4, alpha=0.6)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('RESULTADO FINAL')
            ax.legend()
            
            # Colorbar al final como en el método original
            cbar = self.pso_figure.colorbar(im, ax=ax)
            cbar.set_label(label_escala)
            
        else:  # 3D
            ax = self.pso_figure.add_subplot(111, projection='3d')
            
            # Superficie final
            suprf = ax.plot_surface(X, Y, Z_plot, cmap="viridis", alpha=0.7)
            
            # Partículas finales
            for particula in self.swarm.enjambre:
                parte_x, parte_y = particula.posicion
                if escala_log and funcion(parte_x, parte_y) > 0:
                    parte_z = log10(funcion(parte_x, parte_y))
                else:
                    parte_z = funcion(parte_x, parte_y)
                ax.scatter([parte_x], [parte_y], [parte_z], color='red', s=60, alpha=0.7)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('log10(Z)' if escala_log else 'Z')
            ax.set_title('RESULTADO FINAL')
            
            # Colorbar al final
            self.pso_figure.colorbar(suprf, ax=ax, shrink=0.5)
        
        self.pso_figure.tight_layout()
        self.pso_canvas.draw()

 


def crear_enjambre(num_particulas: int, limites: tuple, funcion: Callable):
        return [Particle(limites, [uniform(limites[0], limites[1]), uniform(limites[0], limites[1])], funcion) for i in range(num_particulas+1)]

if __name__ == "__main__":
        # Modo GUI
        root = tk.Tk()
        app = OptimizationGUI(root)
        root.mainloop()

    #     Modo consola original
    #     limites_prueba = (-2, 2)
    #     enjambre = crear_enjambre(20, limites_prueba, goldstein_price)
    #     prueba = Swarm(enjambre)
        
