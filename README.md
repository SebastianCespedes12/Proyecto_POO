# Proyecto_POO
## Definición de alternativa
Alternativa 3
>Construir una aplicación que emule el algorimo PSO utilizando Python.
## Diagrama de clases
```mermaid
classDiagram
    class Swarm {
        - enjambre: list~Particle~
        - mejor_pos_global: list
        - mejor_val_global: float
        - coeficiente_inercia: float
        - parametro_cognitivo: float
        - parametro_social: float
        + cambiar_velocidades()
        + buscar_mejor_global(funcion)
        + mostrar_enjambre(funcion, num_iteraciones, num_graficas)
    }
    
    class Particle {
        - posicion: list
        - velocidad: list
        - limites: tuple
        - mejor_pos_local: list
        - mejor_val_local: float
        + mover()
        + buscar_mejor_local(funcion)
        + cambiar_velocidad(coeficiente_inercia, parametro_cognitivo, parametro_social, mejor_pos_global)
    }
    
    Swarm --* Particle
```

Utilizando las siguientes formulas:
[![Captura-de-pantalla-2025-06-13-170914.png](https://i.postimg.cc/4yBPmcxx/Captura-de-pantalla-2025-06-13-170914.png)](https://postimg.cc/T55gspbz)
Se definieron dos clases, 
