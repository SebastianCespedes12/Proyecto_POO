
from random import uniform
from time import sleep

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import linspace, meshgrid, log10
from collections.abc import Callable

from PSO.funciones import nombres_funciones, get_funcion, get_limites
from PSO.enjambre import Swarm, crear_enjambre

class OptimizationGUI:
    """
        OptimizationGUI:
        Interfaz gráfica para visualizar y controlar el algoritmo PSO.
        Atributos:
            root: Ventana principal de Tkinter
            swarm: Objeto Swarm actual
            is_animating: Estado de la animación
            
        Métodos principales:
            __init__(): Inicializa la interfaz gráfica
            setup_ui(): Configura los elementos visuales de la GUI
            setup_pso_controls(): Crea los controles para configurar PSO
            animate_pso(): Maneja el inicio/detención de la animación
            mostrar_enjambre_2d(): Visualización 2D del proceso PSO
            mostrar_enjambre_3d(): Visualización 3D del proceso PSO
            termina_animacion(): Procesa los resultados finales
            mostrar_grafica_final(): Muestra el resultado final de la optimización por medio de la grafica seleccionada
    """
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica y los parámetros del algoritmo PSO.
       
        Args:            root: Ventana principal de Tkinter
        Initializes:
        - root: Ventana principal de Tkinter
        - Variables de estado para el enjambre y la animación
        - Variables de GUI para los parámetros del PSO y los widgets
        """
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
        """
        Inicializa la interfaz gráfica 
        Crea los siguientes elementos:
        - Frame principal
        - Panel de controles para PSO
        - Frame para resultados
        - Frame para el gráfico PSO
        Configura los widgets necesarios para interactuar con el algoritmo PSO
        """
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
        """
        Configura los controles de la interfaz para el algoritmo PSO.
        Crea los widgets:
        - Selector de función
        - Parámetros PSO (número de partículas, iteraciones, coeficientes)
        - Tipo de visualización (2D/3D)
        - Checkbox para escala logarítmica
        - Botón para iniciar/detener la animación
        """
        # fila 0: Función 
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
        """
        Maneja el inicio/detención de la animación del algoritmo PSO.
        Si la animación está activa, la detiene y actualiza el botón.
        Si no está activa, inicia la animación con los parámetros actuales.
        Extrae los parámetros de la interfaz y crea el enjambre.
        """
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
        
        # Usar los métodos de visualización adaptados
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
        if escala_log:
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
def crear_root():
    """
    Crea la ventana principal de Tkinter y retorna el objeto root.
    
    Returns:
        tk.Tk: Ventana principal de la aplicación
    """
    root = tk.Tk()
    root.title('PSO Animado - Prototipo')
    root.geometry('1000x800')
    return root