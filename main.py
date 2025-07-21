from PSO import OptimizationGUI, crear_root
 
if __name__ == "__main__":
    # Se inicializa la raíz de la GUI y se corre la aplicación
    root = crear_root()
    app = OptimizationGUI(root)
    root.mainloop()