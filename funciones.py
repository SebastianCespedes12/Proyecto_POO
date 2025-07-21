from numpy import exp, cos, pi

def rastrigin(x, y, A=10):
    return A * 2 + (x**2 - A * cos(2 * pi * x)) + (y**2 - A * cos(2 * pi * y))

def goldstein_price(x, y):
    term1 = 1 + (x + y + 1)**2 * (19 - 14*x + 3*x**2 - 14*y + 6*x*y + 3*y**2)
    term2 = 30 + (2*x - 3*y)**2 * (18 - 32*x + 12*x**2 + 48*y - 36*x*y + 27*y**2)
    return term1 * term2

def beale(x, y):
    return (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2

def booth(x, y):
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2

dic_funciones = {
    "Goldstein-Price": [goldstein_price, (-2,2)],
    "Rastrigin": [rastrigin, (-5.12, 5.12)],
    "Beale": [beale, (-4.5, 4.5)],
    "Rosenbrock": [booth, (-10, 10)],
}
def nombres_funciones():
    return list(dic_funciones.keys())

def get_funcion(name):
    return dic_funciones.get(name)[0]

def get_limites(name):
    return dic_funciones.get(name)[1]
