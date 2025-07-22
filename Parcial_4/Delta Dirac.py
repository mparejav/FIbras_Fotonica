import numpy as np
import matplotlib.pyplot as plt

def delta_dirac(x, sigma=0.01):
  return np.exp(-(x**2)/(2*sigma**2)) / (sigma * np.sqrt(2*np.pi))

def funcion_peine(x, periodo, amplitud=1, sigma=0.01):
  y = np.zeros_like(x)
  for n in range(-10, 10):
    y += amplitud * delta_dirac(x - n*periodo, sigma)
  return y

# Parámetros
periodo = 2
amplitud = 1
sigma = 0.02  # Reducimos sigma para funciones más estrechas

# Valores en el eje x
x = np.linspace(-10, 10, 1000)

# Calcular los valores de la función peine
y = funcion_peine(x, periodo, amplitud, sigma)

# Graficar la función
plt.plot(x, y)
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Función Peine con Deltas de Dirac más Estrechas')
plt.show()