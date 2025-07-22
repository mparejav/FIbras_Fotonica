import numpy as np
import matplotlib.pyplot as plt

''' PARCIAL 4.
    Este programa grafica el patrón de difracción bidimensional de una abertura en forma de cruz basado
    en la solución analítica del campo.
    Se va a trabajar con la difracción de Fraunhofer, que es una aproximación válida para distancias grandes 
    entre la abertura y el plano de observación. Para ello se debe cumplir la condición de Fraunhofer:
    D_prima >> n*(max_length**2)/(λ), donde D_prima es la distancia entre el plano de abertura y el plano de visualización.
'''

# Parametros del sistema 
n = 1                       # Indice de refracción del medio. Aire por defecto.
window_size = 1500                 # Tamaño de la malla cuadrada (número de puntos en cada eje).
λ_0 = 0.5 #um               # Longitud de onda de la fuente de luz
λ = λ_0/n #um               # Lambda efectiva
k_0 = 2 * np.pi / λ #um^-1  # Número de onda en el medio

# Dimensiones de la abertura
e = 200  #um              # Ancho de la abertura horizontal
t = 200  #um              # Ancho de las aberturas verticales
L1 = 1000  #um            # Longitud de la abertura horizontal
L2 = 1000  #um            # Longitud de las aberturas verticales
h1 = 800  #um             # Altura de la abertura vertical superior
h2 = 800 #um              # Altura de la abertura vertical inferior

# Longitudes totales de la abertura
L = L1 + L2 + t # Longitud total horizontal
H = e + h1 + h2 # Altura total vertical

# Encuentra el tamaño mínimo característico de la cruz (en um)
P = np.array([L1, L2, h1, h2, t, e])
min_dim = np.min(P)

'''
Se determina la máxima longitud de la abertura para calcular la distancia mínima requerida
que cumpla la condición de Fraunhofer.
Esta condición en simulaciones de este tipo no es tan crítica.
'''

# Encuentra la longitud máxima de la abertura (en um)
max_dim = np.max(P)

# Condicion de Fraunhofer
D_prima = float(input(f"D_prima > {(n * max_dim**2)/(2*λ)} [um]:  "))   

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

''' 
Rango de coordenadas angulares en el plano de la pantalla.
Cada punto de la malla representa un ángulo θ en el plano primado.
El rango angular se define dinámicamente basado en la longitud de onda y el tamaño mínimo de la abertura.
Esto asegura que el rango angular sea adecuado para la resolución de la malla.
'''
# Factor de escala angular
# Este factor se utiliza para ajustar el rango angular de acuerdo con el tamaño de la malla.
# Se ajusta a sensaciones en función de que tan abierto o cerrado se quiera el rango angular.
angular_scale_factor = 10 # Factor de escala para el rango angular

# Rango angular dinámico (radianes)
range_of_theta = (λ * angular_scale_factor) / min_dim  # λ en um, min_dim en um

# Se despliega el rango de coordenadas angulares (rad) en el tamaño de la malla
theta_x = np.linspace(-range_of_theta, range_of_theta, window_size)
theta_y = np.linspace(-range_of_theta, range_of_theta, window_size)
axisX, axisY = np.meshgrid(theta_x, theta_y)

# Se definen las frecuencias espaciales en el plano de la pantalla
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

# Definicion de las transformadas de Fourier (desarrollo de la solucion analitica)
FT_1 = L * e * sinc_β_x0 * sinc_β_y0 * np.exp(-1j * (2 * np.pi / λ) * (x_0 * np.sin(axisX) + y_0 * np.sin(axisY)))
FT_2 = t * h1 * sinc_β_x1 * sinc_β_y1 * np.exp(-1j * (2 * np.pi / λ) * (x_1 * np.sin(axisX) + y_1 * np.sin(axisY)))
FT_3 = t * h2 * sinc_β_x2 * sinc_β_y2 * np.exp(-1j * (2 * np.pi / λ) * (x_2 * np.sin(axisX) + y_2 * np.sin(axisY)))   

# Funcion de intensidad en la pantalla
Intensity_Function = 1/(λ**2 * D_prima**2) * np.abs(FT_1 + FT_2 + FT_3)**2

# Intensidad normalizada
Intensity_Function = Intensity_Function / np.max(Intensity_Function)

# Grafica de la mascara
fig, ax = plt.subplots(1, 2, figsize = (12, 6))

ax[0].set_xlim(-window_size, window_size)
ax[0].set_ylim(-window_size, window_size)
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
ax[0].set_xlabel(r"$\tilde{x}$ [um]")
ax[0].set_ylabel(r"$\tilde{y}$ [um]")

# Grafica del patrón de difracción
'''
Se define el rango de coordenadas espaciales en el plano de la pantalla. Se pasa de coordenadas angulares a coordenadas espaciales,
usando aproximación de ángulos pequeños para la tangente.
Esto permite visualizar el patrón de difracción en términos de posiciones físicas en la pantalla. 
'''
extent = [theta_x.min()*D_prima, theta_x.max()*D_prima, theta_y.min()*D_prima, theta_y.max()*D_prima]

# Definir grafica que contiene patron de difraccion
# Se toma el logaritmo de la función de intensidad para mejorar la visualización.
patron = ax[1].imshow(np.log(Intensity_Function + 1e-6), extent=extent, cmap="inferno") 
ax[1].set_title("Screen")
ax[1].set_xlabel("x' [um]")
ax[1].set_ylabel("y' [um]")
plt.colorbar(patron, ax=ax[1], label="Log Normalized Intensity")

# Se muestran los gráficos
plt.tight_layout()
plt.show()















