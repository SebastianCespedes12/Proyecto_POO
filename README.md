# Proyecto_POO
## Definición de alternativa
Alternativa 3
>Construir una aplicación que emule el algorimo PSO utilizando Python.
## Diagrama de clases
```mermaid
classDiagram
       class Swarm {
        - list~Particle~ enjambre
        - list mejor_pos_global
        - float mejor_global
        + __init__(enjambre)
        + buscar_mejor_global(funcion)
        + cambiar_velocidades(parametro_cognitivo, parametro_social)
        + mejor_global_encontrado()
    }
    class Particle {
        - list posicion
        - list velocidad
        - list limites
        - list mejor_pos_local
        - float mejor_local
        + __init__(posicion, funcion, limites)
        + mover()
        + buscar_mejor_local(funcion)
        + cambiar_velocidad(parametro_cognitivo, parametro_social, mejor_pos_global)
    }
    Swarm --* Particle
```

Utilizando las siguientes formulas:
[![Captura-de-pantalla-2025-06-13-170914.png](https://i.postimg.cc/4yBPmcxx/Captura-de-pantalla-2025-06-13-170914.png)](https://postimg.cc/T55gspbz)
Se definieron dos clases, 
