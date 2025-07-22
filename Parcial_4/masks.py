import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Variables globales 

size = 2048    # Numero de pixeles de un lado de la ventana que grafica la mascara. Como la ventana es cuadrada, este valor al cuadrado da el numero de pixeles de la imagen.
physical_size = 10 #mm  # Tamaño fisico de la mascara 

### Funciones miscelanea ###

# Funcion para convertir dimensiones fisicas a pixeles.
def mm_to_pixels(dimention_in_mm):
    
    convertion_factor = size / physical_size    #pixeles por mm
    
    return dimention_in_mm * convertion_factor  # Retorna el numero de pixeles de determinada magnitud


### Funciones para la creación de aberturas convencionales ###

'''
Todas las mascaras se generan con ventanas cuadradas de tamaño M X M. 
Las figuras convencionales se graficaran siguiendo geometrias simetricas centradas en la mitad de la imagen.
'''

# Funcion que genera una abertura circular centrada. 
def circle(radius_mm):
    x, y = np.ogrid[:size, :size]   # genera malla de puntos
    center = size // 2               # centra el circulo. Valor entero
    radius_px = int(mm_to_pixels(radius_mm))
    
    boolean_condition = (x - center)**2 + (y - center)**2 <= radius_px    # Ecuacion de una circunferencia para generar la mascara. Construye una matriz booleana en donde hay True dentro del círculo.
    mask  =  np.where(boolean_condition,1,0) # Genera una matriz condicional. (condicion, valor si TRUE, valor si FALSE)
    return mask
    
# Funcion que genera una abertura rectangular centrada. 
# Los lados se especifican en milimetros.
def rectangle(width_mm, height_mm):
    
    width_px  = int(mm_to_pixels(width_mm))   # Ancho en pixeles
    height_px = int(mm_to_pixels(height_mm))  # Alto en pixeles
    mask = np.zeros((size, size))             # Genera una matriz de ceros. Todo opaco.
    
    center = size // 2  # Coordenada central
    mask[center - height_px // 2 : center + height_px // 2,        # Se define la mascara directamente con indices. No hay necesidad de ecuación que genere condición booleana.
         center - width_px  // 2 : center + width_px  // 2] = 1
    
    return mask

# Funcion que genera una rendija vertical centrada. 
# El ancho se especifica en milimetros.
def vertical_slit(width_mm):
    
    width_px = int(mm_to_pixels(width_mm))    # Ancho de la rendija en pixeles
    mask = np.zeros((size, size))             # Genera una matriz de ceros. Todo opaco.

    center = size // 2                        # Coordenada central
    mask[:, center - width_px // 2 : center + width_px // 2] = 1
    
    return mask

# Funcion que genera una rendija horizontal centrada. 
# El ancho se especifica en milimetros.
def horizontal_slit(width_mm):
    
    width_px = int(mm_to_pixels(width_mm))    # Ancho de la rendija en pixeles
    mask = np.zeros((size, size))             # Genera una matriz de ceros. Todo opaco.

    center = size // 2                        # Coordenada central
    mask[center - width_px // 2 : center + width_px // 2:] = 1
    
    return mask

# Funcion que carga una imagen en escala de grises y la convierte en una mascara binaria.
# La imagen debe tener fondo negro (obstaculo) y figuras blancas (apertura).
def load_image(image_path):
    
    img = Image.open(image_path).convert('L')              # Convertir a escala de grises
    img = img.resize((size, size))                         # Redimensionar a la matriz de simulación
    img_array = np.array(img)
    
    # Normalizar: los valores >128 se consideran como apertura (1), los demás como obstáculo (0)
    mask = np.where(img_array > 128, 1, 0)                 
    return mask

# Funcion que genera una máscara en forma de cruz centrada, con espesores independientes en vertical y horizontal.
# La cruz se forma a partir de dos rectángulos: uno horizontal (con grosor 'e') y uno vertical (con grosor 't').
# Las dimensiones están definidas en milímetros y se convierten a píxeles internamente.

def cross_mask(L1, L2, h1, h2, t, e):
    '''
    Parámetros:
    - L1 : float → Longitud horizontal izquierda desde el centro (mm)
    - L2 : float → Longitud horizontal derecha desde el centro (mm)
    - h1 : float → Altura hacia arriba desde el centro (mm)
    - h2 : float → Altura hacia abajo desde el centro (mm)
    - t  : float → Espesor del brazo vertical (mm)
    - e  : float → Espesor del brazo horizontal (mm)
    '''

    # Conversión de dimensiones físicas a pixeles
    L1_px = int(mm_to_pixels(L1))
    L2_px = int(mm_to_pixels(L2))
    h1_px = int(mm_to_pixels(h1))
    h2_px = int(mm_to_pixels(h2))
    t_px  = int(mm_to_pixels(t))
    e_px  = int(mm_to_pixels(e))

    mask = np.zeros((size, size))
    center = size // 2

    # Brazo horizontal: largo total (L1 + t + L2), grosor e
    x_start = center - L1_px - t_px // 2
    x_end   = center + L2_px + t_px // 2
    y_start = center - e_px // 2
    y_end   = center + e_px // 2
    mask[y_start:y_end, x_start:x_end] = 1

    # Brazo vertical: largo total (h1 + h2 + e), grosor t
    x_start_v = center - t_px // 2
    x_end_v   = center + t_px // 2
    y_start_v = center - h2_px - e_px // 2
    y_end_v   = center + h1_px + e_px // 2
    mask[y_start_v:y_end_v, x_start_v:x_end_v] = 1

    return mask

# Función que grafica solo la máscara
def plot_mask(mask, title='Abertura'):
    plt.figure(figsize=(6, 6))
    plt.imshow(mask, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()