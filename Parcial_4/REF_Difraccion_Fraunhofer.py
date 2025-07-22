import numpy as np
import matplotlib.pyplot as plt

""" PARCIAL 4.
    Este programa grafica el patron de difraccion de dos aberturas rectangulares basado
    en la solucion analitica. Además de que tomamos la difraccion como difraccion de cam-
    po lejano con su condicion: D_prima >> n*(x_moñito**2 + y_moñito**2)/(2*wavelength).

    NOTA: asumimos n: indice de refraccion, n = 1
"""

# Parametros del problema
wavelength = float(input("Wavelength [um]: "))
a = float(input("a [um]: "))
b = float(input("b [um]: "))
c = float(input("c [um]: "))
d = float(input("d [um]: "))
D = float(input("D [um]: "))

# Condicion de campo lejano para aberturas
cond1 = ((a**2 + b**2)/(2*wavelength))
cond2 = ((c**2 + d**2)/(2*wavelength))
D_prima = float(input(f"D_prima (distance mask-screen) D_prima > {cond1} [um] and D_prima > {cond2} [um]:  "))

# Poscion de centros de las aberturas
rect1_center_x = -D/2
rect1_center_y = 0
rect2_center_x = D/2
rect2_center_y = 0

# Rango de thetas (radianes)
P = np.array([[a,b],[c,d]])
range_of_theta = (wavelength*2000)/(np.min(P))
theta_x = np.linspace(-range_of_theta, range_of_theta, 1000)
theta_y = np.linspace(-range_of_theta, range_of_theta, 1000)
axisX, axisY = np.meshgrid(theta_x, theta_y)

# Betas
beta_x1 = (2*np.pi*a*np.sin(axisX))/(wavelength)
beta_y1 = (2*np.pi*b*np.sin(axisY))/(wavelength)

beta_x2 = (2*np.pi*c*np.sin(axisX))/(wavelength)
beta_y2 = (2*np.pi*d*np.sin(axisY))/(wavelength)

# Funcion de Intensidad (proviene de la solucion analitica)
sincBx1 = np.sinc(beta_x1/(2 * np.pi))
sincBy1 = np.sinc(beta_y1/(2 * np.pi))
sincBx2 = np.sinc(beta_x2/(2 * np.pi))
sincBy2 = np.sinc(beta_y2/(2 * np.pi))

# Resultados de transformadas de fourier. 
# F1: de tao_moñito1
# F1: de tao_moñito1
F1 = a * b * sincBx1 * sincBy1 * np.exp(-1j * (2 * np.pi / wavelength) * (rect1_center_x * np.sin(axisX)))
F2 = c * d * sincBx2 * sincBy2 * np.exp(-1j * (2 * np.pi / wavelength) * (rect2_center_x * np.sin(axisX)))

# I = Ifuente n**2 / (lambda**2 *D_prima**2) (F(Tao1_moñito)**2 + F(Tao2_moñito)**2 + F(Tao1_moñito)F(Tao2_moñito)* + F(Tao2_moñito)F(Tao1_moñito)*)
# donde * es conjugado
I = 1/(wavelength**2 * D_prima**2)*np.abs(F1 + F2)**2
# Intensidad normalizada
I /= np.max(I)

fig, ax = plt.subplots(1, 2, figsize = (12, 6))

ax[0].set_xlim(-2000, 2000)
ax[0].set_ylim(-2000, 2000)
ax[0].set_facecolor("#ffb8a9")

rect1 = plt.Rectangle((rect1_center_x - a/2, rect1_center_y - b/2), a, b, color = "white")
rect2 = plt.Rectangle((rect2_center_x - c/2, rect2_center_y - d/2), c, d, color = "white")
ax[0].add_patch(rect1)  #añadir a la grafica el rectanngulo 1
ax[0].add_patch(rect2)  #añadir a la grafica el rectanngulo 2
ax[0].set_title("Mask")
ax[0].set_xlabel("x [um]")
ax[0].set_ylabel("y [um]")

# GRAFICA PATRON DE DIFRACCION

# Conversion radianes a coordenadas
extent = [theta_x.min()*D_prima, theta_x.max()*D_prima, theta_y.min()*D_prima, theta_y.max()*D_prima]
# Definir grafica que contiene patron de difraccion
patron = ax[1].imshow(I, extent = [-1, 1, -1, 1], cmap = "plasma")
ax[1].set_title("Screen")
ax[1].set_xlabel("x' [um]")
ax[1].set_ylabel("y' [um]")
plt.colorbar(patron, ax=ax[1], label="Normalized Intensity")
#Mostrar graficos
plt.tight_layout()
plt.show()