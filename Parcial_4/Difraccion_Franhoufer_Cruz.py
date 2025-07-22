import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from masks import *  # Importa las funciones de generación de máscaras 
from Fraunhofer_graph import *

''' PARCIAL 4.
    Este programa grafica el patrón de difracción bidimensional de una abertura en forma de cruz basado
    en la solución analítica. 
    Se toma la difracción de campo lejano en función de la condición de Fraunhofer:
    D_prima >> n*(max_length**2)/(λ).
'''

# Parametros del sistema 
R_p = 1e6 #um              # Distancia del plano de abertura al plano de visualización 
n = 1                      # Indice de refracción del medio. Aire por defecto.
size = 2048    # Numero de pixeles de un lado de la ventana que grafica la mascara. Como la ventana es cuadrada, este valor al cuadrado da el numero de pixeles de la imagen.

# Dimensiones de la abertura
λ_0 = 0.5 #um              # Longitud de onda de la fuente de luz
e = 200  #um              # Ancho de la abertura horizontal
t = 200  #um              # Ancho de las aberturas verticales
L1 = 1000  #um              # Longitud de la abertura horizontal
L2 = 1000  #um              # Longitud de las aberturas verticales
h1 = 800  #um              # Altura de la abertura vertical superior
h2 = 800 #um              # Altura de la abertura vertical inferior

λ = λ_0/n #um              # Lambda efectiva
k_0 = 2 * np.pi / λ #um^-1   # Número de onda en el medio

L = L1 + L2 + t # Longitud total horizontal
H = e + h1 + h2 # Altura total vertical

max_length = max(L, H)  # Longitud máxima de la abertura

# Condicion de Fraunhofer
D_prima = float(input(f"D_prima > {max_length**2/(2*λ)} [um]:  "))   

# Posiciones de los centros de los rectángulos 
# Rectangulo 1 (horizontal):
x_0 = (L2-L1)/2
y_0 = 0 
# Rectangulo 2 (vertical por encima del eje x):
x_1 = 0
y_1 = (e/2+h1/2)
# Rectangulo 3 (vertical por debajo del eje x):
x_2 = 0
y_2 = (-e/2-h2/2)

# Encuentra el tamaño mínimo característico de la cruz (en um)
P = np.array([L1, L2, h1, h2, t, e])
min_dim = np.min(P)

# Rango angular dinámico (radianes)
range_of_theta = (λ * 500) / min_dim  # λ en um, min_dim en um

theta_x = np.linspace(-range_of_theta, range_of_theta, size)
theta_y = np.linspace(-range_of_theta, range_of_theta, size)
axisX, axisY = np.meshgrid(theta_x, theta_y)

# Betas
β_x0 = (2 * np.pi * L / λ) * np.sin(axisX)
β_y0 = (2 * np.pi * H / λ) * np.sin(axisY)
β_x1 = (2 * np.pi * t / λ) * np.sin(axisX)
β_y1 = (2 * np.pi * h1 / λ) * np.sin(axisY)
β_x2 = (2 * np.pi * t / λ) * np.sin(axisX)
β_y2 = (2 * np.pi * h2 / λ) * np.sin(axisY)

# Funciones de intensidad (Parten de la solución analitica)
sinc_β_x0 = np.sinc(β_x0 / (2 * np.pi))
sinc_β_y0 = np.sinc(β_y0 / (2 * np.pi))
sinc_β_x1 = np.sinc(β_x1 / (2 * np.pi))
sinc_β_y1 = np.sinc(β_y1 / (2 * np.pi))
sinc_β_x2 = np.sinc(β_x2 / (2 * np.pi))
sinc_β_y2 = np.sinc(β_y2 / (2 * np.pi))

# Definicion de las transformadas de Fourier
F1 = L * e * sinc_β_x0 * sinc_β_y0 * np.exp(-1j * (2 * np.pi / λ) * (x_0 * np.sin(axisX) + y_0 * np.sin(axisY)))
F2 = t * h1 * sinc_β_x1 * sinc_β_y1 * np.exp(-1j * (2 * np.pi / λ) * (x_1 * np.sin(axisX) + y_1 * np.sin(axisY)))
F3 = t * h2 * sinc_β_x2 * sinc_β_y2 * np.exp(-1j * (2 * np.pi / λ) * (x_2 * np.sin(axisX) + y_2 * np.sin(axisY)))   

# Funcion de intensidad en la pantalla
I = 1/(λ**2 * D_prima**2) * np.abs(F1 + F2 + F3)**2

# Intensidad normalizada
I /= np.max(I)

# Grafica de la mascara
fig, ax = plt.subplots(1, 2, figsize = (12, 6))

ax[0].set_xlim(-size, size)
ax[0].set_ylim(-size, size)
ax[0].set_facecolor("#000000")

# Rectángulo horizontal (centro en x_0, y_0)
rect1 = plt.Rectangle((x_0 - L/2, y_0 - e/2), L, e, color="white")

# Rectángulo vertical superior (centro en x_1, y_1)
rect2 = plt.Rectangle((x_1 - t/2, y_1 - h1/2), t, h1, color="white")

# Rectángulo vertical inferior (centro en x_2, y_2)
rect3 = plt.Rectangle((x_2 - t/2, y_2 - h2/2), t, h2, color="white")

ax[0].add_patch(rect1)
ax[0].add_patch(rect2)
ax[0].add_patch(rect3)
ax[0].set_title("Mask")
ax[0].set_xlabel("x [um]")
ax[0].set_ylabel("y [um]")

# Grafica del patrón de difracción
# Conversion radianes a coordenadas
extent = [theta_x.min()*D_prima, theta_x.max()*D_prima, theta_y.min()*D_prima, theta_y.max()*D_prima]

# Definir grafica que contiene patron de difraccion
patron = ax[1].imshow(np.log(I + 1e-6), extent=extent, cmap="inferno")
ax[1].set_title("Screen")
ax[1].set_xlabel("x' [um]")
ax[1].set_ylabel("y' [um]")
plt.colorbar(patron, ax=ax[1], label="Normalized Intensity")
#Mostrar graficos
plt.tight_layout()
plt.show()















