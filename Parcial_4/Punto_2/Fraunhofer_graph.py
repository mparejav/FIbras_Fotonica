import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from masks import *  # Importa las funciones de generación de máscaras 

# Funcion que simula la difracción de Fraunhofer generada por una apertura dada.
# Aplica la transformada de Fourier bidimensional a la máscara y calcula la intensidad del patrón resultante.
def Fraunhofer_Diffraction(mask):
    
    # La difracción de Fraunhofer es proporcional a la transformada de Fourier de la función apertura:
    # I(u,v) ∝ |F{A(x,y)}|^2

    fft = np.fft.fft2(mask)            # Transformada de Fourier bidimensional de la máscara
    fft = np.fft.fftshift(fft)         # Centra las frecuencias (cambia el cero de frecuencia al centro)
    Intensity = np.abs(fft) ** 2       # Calcula la intensidad: |FFT|^2

    '''
    Esta operación modela lo que se observa en el plano focal de una lente al iluminar la abertura con una onda plana. 
    El resultado representa el patrón de intensidad en ese plano.
    '''
    return Intensity

# Funcion que grafica una mascara de apertura y su correspondiente patron de difracción de Fraunhofer.
# La intensidad se muestra en escala logaritmica para resaltar los detalles del patrón.
def graph(mask, Intensity):

    # Crear figura con dos paneles: apertura y patrón
    plt.figure(figsize=(10, 5))

    # Mostrar la abertura (máscara binaria)
    plt.subplot(1, 2, 1)
    plt.title('Abertura')
    plt.imshow(mask, cmap='gray')   # Escala de grises: blanco = luz pasa, negro = bloquea

    # Mostrar el patrón de difracción (logaritmo para mejorar el contraste visual)
    plt.subplot(1, 2, 2)
    plt.title('Difracción de Fraunhofer')
    plt.imshow(np.log(Intensity + 1), cmap='inferno')  # +1 para evitar log(0)

    plt.show()

# Funcion que simula y grafica la difracción de Fraunhofer para diferentes tipos de abertura.
# Permite seleccionar la geometría y pasar parámetros mediante argumentos nombrados.

def simulate_and_graph(shape='circle', **kwargs):
    '''
    Parámetros:
    - shape : str
        Tipo de abertura. Puede ser:
        'circle', 'rectangle', 'vertical_slit', 'horizontal_slit', 'image'

    - **kwargs : keyword arguments : diccionario
        Argumentos específicos para cada tipo de figura. Ejemplos:
        radius_mm = 1.0                     → para círculos
        vertical_slit_width_mm = 1.0        → para rendijas verticales
        horizontal_slit_width_mm = 1.0      → para rendijas horizontales
        width_mm = 1.5, height_mm = 2.0     → para rectángulos
        image_path = 'ruta.jpg'             → para cargar imagen

    El uso de **kwargs permite que esta función acepte distintos argumentos
    dependiendo del tipo de figura, sin necesidad de definir cada posible combinación de entrada.

    Ejemplo de uso:
    simulate_and_graph(shape='circle', radius_mm=0.5)
    simulate_and_graph(shape='rectangle', width_mm=1, height_mm=2)
    simulate_and_graph(shape='image', image_path='mascara.jpg')
    '''

    # Selección de figura
    if shape == 'circle':
        mask = circle(kwargs['radius_mm'])

    elif shape == 'rectangle':
        mask = rectangle(kwargs['width_mm'], kwargs['height_mm'])

    elif shape == 'vertical_slit':
        mask = vertical_slit(kwargs['vertical_slit_width_mm'])

    elif shape == 'horizontal_slit':
        mask = horizontal_slit(kwargs['horizontal_slit_width_mm'])

    elif shape == 'image':
        mask = load_image(kwargs['image_path'])
        
    elif shape == 'cross_mask':
        # Extraer parámetros específicos para la cruz
        L1 = kwargs['L1']
        L2 = kwargs['L2']
        h1 = kwargs['h1']
        h2 = kwargs['h2']
        t = kwargs['t']
        e = kwargs['e']
        mask = cross_mask(L1, L2, h1, h2, t, e)

    else:
        raise ValueError(f"Tipo de figura no reconocida: {shape}")

    # Mostrar la apertura y su patrón de difracción
    graph(mask, Intensity = Fraunhofer_Diffraction(mask))

    
#simulate_and_graph(shape = 'circle', radius_mm = 1.0)  

#simulate_and_graph(shape='rectangle', width_mm=2.0, height_mm=1.0)  # Ejemplo de uso con rectángulo

#simulate_and_graph(shape='vertical_slit', vertical_slit_width_mm=0.5)  # Ejemplo de uso con rendija vertical

#simulate_and_graph(shape='horizontal_slit', horizontal_slit_width_mm=0.5)  # Ejemplo de uso con rendija horizontal

#simulate_and_graph(shape='image', image_path='/home/manuel/Documents/GitHub/FIbras_Fotonica/Parcial_4/Images/CirculoCuadrado.png')  # Ejemplo de uso con imagen

#simulate_and_graph(shape = 'cross_mask', L1 = 4.0, L2 = 4.0, h1 = 2, h2 = 2, t = 0.5, e = 0.5)  # Ejemplo de uso con cruz


