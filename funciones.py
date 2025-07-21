from numpy import exp, cos, pi

def costo_produccion(x,y):
    """
    Calcula el costo total de producción de un producto en función de la cantidad de materia prima (x)
    y las horas de trabajo (y).

    El costo incluye:
    - Costo de materia prima: 5 * x
    - Costo de mano de obra: 10 * y
    - Penalización cuadrática por desviarse de los valores ideales (x=10, y=5):
      (x-10)**2 + (y-5)**2, se usa el cuadrado para "penalizar más fuerte" en el algoritmo
      y que este se enfoque en buscar valores que se desvén poco

    El objetivo de la optimización es encontrar los valores de x e y que minimizan el costo total,
    favoreciendo soluciones cercanas a 10 unidades de materia prima y 5 horas de trabajo.

    Parámetros:
        x (float): cantidad de materia prima
        y (float): horas de trabajo

    Retorna:
        float: costo total de producción
    """    
    return 5*x +10*y + (x-10)**2 + (y-8)**2 

def rastrigin(x, y, A=10):
    """
    Calcula el valor de la función de Rastrigin en dos dimensiones.

    Es una función de prueba clásica en optimización, caracterizada por su gran cantidad de mínimos locales.

    Parámetros:
        x (float): variable x
        y (float): variable y
        A (float): parámetro de la función (por defecto 10)

    Retorna:
        float: valor de la función Rastrigin
    """
    return A * 2 + (x**2 - A * cos(2 * pi * x)) + (y**2 - A * cos(2 * pi * y))

def goldstein_price(x, y):
    """
    Calcula el valor de la función Goldstein-Price.

    Es una función de prueba utilizada en optimización global, con un mínimo global bien definido.

    Parámetros:
        x (float): variable x
        y (float): variable y

    Retorna:
        float: valor de la función Goldstein-Price
    """
    term1 = 1 + (x + y + 1)**2 * (19 - 14*x + 3*x**2 - 14*y + 6*x*y + 3*y**2)
    term2 = 30 + (2*x - 3*y)**2 * (18 - 32*x + 12*x**2 + 48*y - 36*x*y + 27*y**2)
    return term1 * term2

def beale(x, y):
    """
    Calcula el valor de la función de Beale.

    Es una función de prueba para algoritmos de optimización, con un mínimo global en (3, 0.5).

    Parámetros:
        x (float): variable x
        y (float): variable y

    Retorna:
        float: valor de la función Beale
    """

    return (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2

def booth(x, y):
    """
    Calcula el valor de la función de Booth.

    Es una función de prueba para optimización, con un mínimo global en (1, 3).

    Parámetros:
        x (float): variable x
        y (float): variable y

    Retorna:
        float: valor de la función Booth
    """
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2

dic_funciones = {
    "Goldstein-Price": [goldstein_price, (-2,2)],
    "Rastrigin": [rastrigin, (-5.12, 5.12)],
    "Beale": [beale, (-4.5, 4.5)],
    "Rosenbrock": [booth, (-10, 10)],
    "Costo-Produccion" : [costo_produccion,(0,16)]
}
def nombres_funciones():
    return list(dic_funciones.keys())

def get_funcion(name):
    return dic_funciones.get(name)[0]

def get_limites(name):
    return dic_funciones.get(name)[1]
