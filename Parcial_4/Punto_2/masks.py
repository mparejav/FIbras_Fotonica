import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Variables globales 
size = 2048    # Número de píxeles de un lado de la ventana (cada pixel = 1 um)
physical_size_um = 2000  # Tamaño físico de la ventana en micras (um)

### Funciones para la creación de aberturas convencionales ###

'''
Todas las máscaras se generan con ventanas cuadradas de tamaño size x size.
Las figuras convencionales se grafican siguiendo geometrías simétricas centradas en la mitad de la imagen.
Las dimensiones se especifican directamente en micras (um).
'''

# Función que genera una abertura circular centrada.
def circle(radius_um):
    # Genera coordenadas físicas centradas en 0
    x = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    y = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    X, Y = np.meshgrid(x, y)
    mask = np.where(X**2 + Y**2 <= radius_um**2, 1, 0)
    return mask

# Función que genera una abertura rectangular centrada.
def rectangle(width_um, height_um):
    x = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    y = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    X, Y = np.meshgrid(x, y)
    mask = np.where(
        (np.abs(X) <= width_um // 2) & (np.abs(Y) <= height_um // 2),
        1, 0
    )
    return mask

# Función que genera una rendija vertical centrada.
def vertical_slit(width_um):
    x = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    y = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    X, Y = np.meshgrid(x, y)
    mask = np.where(np.abs(X) <= width_um // 2, 1, 0)
    return mask

# Función que genera una rendija horizontal centrada.
def horizontal_slit(width_um):
    x = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    y = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    X, Y = np.meshgrid(x, y)
    mask = np.where(np.abs(Y) <= width_um // 2, 1, 0)
    return mask

# Función que carga una imagen en escala de grises y la convierte en una máscara binaria.
# La imagen debe tener fondo negro (obstáculo) y figuras blancas (apertura).
def load_image(image_path):
    img = Image.open(image_path).convert('L')      # Convertir a escala de grises
    img = img.resize((size, size))                 # Redimensionar a la matriz de simulación
    img_array = np.array(img)
    # Normalizar: los valores >128 se consideran como apertura (1), los demás como obstáculo (0)
    mask = np.where(img_array > 128, 1, 0)
    return mask

# Función que genera una máscara en forma de cruz centrada, con espesores independientes en vertical y horizontal.
# La cruz se forma a partir de dos rectángulos: uno horizontal (con grosor 'e_um') y uno vertical (con grosor 't_um').
# Las dimensiones están definidas en micras (um).
def cross_mask(L1_um, L2_um, h1_um, h2_um, t_um, e_um):
    
    x = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    y = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    X, Y = np.meshgrid(x, y)
    mask = np.zeros((size, size))
    
    # Brazo horizontal
    cond_h = (np.abs(Y) <= e_um/2) & (X >= -L1_um - t_um/2) & (X <= L2_um + t_um/2)
    mask[cond_h] = 1

    # Brazo vertical
    cond_v = (np.abs(X) <= t_um/2) & (Y >= -h2_um - e_um/2) & (Y <= h1_um + e_um/2)
    mask[cond_v] = 1

    return mask

def Edge():
    x0_um = 0  # Posición del borde en micras
    x = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    y = np.linspace(-physical_size_um/2, physical_size_um/2, size)
    X, Y = np.meshgrid(x, y)
    mask = np.where(X >= x0_um, 1, 0)
    return mask

# Función que grafica solo la máscara
def plot_mask(mask, title='Abertura'):
    plt.figure(figsize=(6, 6))
    plt.imshow(mask, cmap='gray', extent=[-size//2, size//2, -size//2, size//2])
    plt.title(title)
    plt.xlabel('x [um]')
    plt.ylabel('y [um]')
    plt.axis('on')
    plt.show()