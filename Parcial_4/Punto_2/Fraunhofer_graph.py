import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from masks import *  # Importa las funciones de generación de máscaras 

# Parámetros de la simulación
λ = 0.5 # um. Longitud de onda de la luz
D_prima = 1e6  # um. Distancia desde la abertura al plano

# Funcion que simula la difracción de Fraunhofer generada por una apertura dada.
# Aplica la transformada de Fourier bidimensional a la máscara y calcula la intensidad del patrón resultante.
def Fraunhofer_Diffraction(mask):
    
    # La difracción de Fraunhofer es proporcional a la transformada de Fourier de la función apertura:
    # I(u,v) ∝ |F{A(x,y)}|^2

    fft = np.fft.fft2(mask)            # Transformada de Fourier bidimensional de la máscara
    fft = np.fft.fftshift(fft)         # Centra las frecuencias (cambia el cero de frecuencia al centro)
    Intensity =  1/(λ**2 * D_prima**2) * np.abs(fft) ** 2  # Función de intensidad.

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
    plt.title('Mask')
    plt.imshow(mask, cmap='gray', extent=[-size//2, size//2, -size//2, size//2])
    plt.xlabel(r"$\tilde{x}$ [um]")
    plt.ylabel(r"$\tilde{y}$ [um]")
    plt.axis('on')

    # Calcular ejes físicos para la pantalla de difracción
    # Teniendo en cuenta que size es el número de píxeles y cada pixel = 1 um en la mascara
    dx = 1  # um
    L = size * dx  # tamaño físico de la máscara en um
    
    # Vector de frecuencias espaciales (ciclos/um)
    fx = np.fft.fftshift(np.fft.fftfreq(size, d=dx))
    fy = np.fft.fftshift(np.fft.fftfreq(size, d=dx))
    
    # Coordenadas físicas en la pantalla de observación (en um)
    X_screen = (λ * D_prima * fx) * 1000 # Convertir a mm
    Y_screen = (λ * D_prima * fy) * 1000 # Convertir a mm
    extent_screen = [X_screen.min(), X_screen.max(), Y_screen.min(), Y_screen.max()]

    # Porcentaje del espectro a mostrar (por ejemplo, 10%)
    crop = 0.2
    N = int(size * crop / 2)

    # Índices para recortar
    ix_start = size//2 - N
    ix_end   = size//2 + N

    # Índices para recortar en y (para los slits horizontal y vertical)
    iy_start = size//2 - N
    iy_end   = size//2 + N

    # Recorta intensidad y ejes
    Intensity_crop = Intensity[ix_start:ix_end, ix_start:ix_end]
    X_screen_crop = X_screen[ix_start:ix_end]
    Y_screen_crop = Y_screen[iy_start:iy_end] # multiplicar por 5 para slits
    extent_screen_crop = [X_screen_crop.min(), X_screen_crop.max(), Y_screen_crop.min(), Y_screen_crop.max()]

    # Mostrar el patrón de difracción (logaritmo para mejorar el contraste visual)
    plt.subplot(1, 2, 2)
    plt.title('Screen')
    plt.imshow(np.log10(Intensity_crop + 1e-5), cmap='inferno', extent=extent_screen_crop)
    plt.xlabel("$x'$ [mm]")
    plt.ylabel("$y'$ [mm]")
    plt.axis('on')

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
        radius_um = 50                      → para círculos
        vertical_slit_width_um = 1.0        → para rendijas verticales
        horizontal_slit_width_um = 1.0      → para rendijas horizontales
        width_um = 200, height_um = 100     → para rectángulos
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
        mask = circle(kwargs['radius_um'])

    elif shape == 'rectangle':
        mask = rectangle(kwargs['width_um'], kwargs['height_um'])

    elif shape == 'vertical_slit':
        mask = vertical_slit(kwargs['vertical_slit_width_um'])

    elif shape == 'horizontal_slit':
        mask = horizontal_slit(kwargs['horizontal_slit_width_um'])

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

#simulate_and_graph(shape = 'circle', radius_um = 50.0)

#simulate_and_graph(shape='rectangle', width_um = 200, height_um = 100)  # Ejemplo de uso con rectángulo

#simulate_and_graph(shape='vertical_slit', vertical_slit_width_um = 100)  # Ejemplo de uso con rendija vertical

#simulate_and_graph(shape='horizontal_slit', horizontal_slit_width_um = 100)  # Ejemplo de uso con rendija horizontal

#simulate_and_graph(shape='image', image_path='/home/manuel/Documents/GitHub/FIbras_Fotonica/Parcial_4/Images/PatronCircular.jpg')  # Ejemplo de uso con imagen

#simulate_and_graph(shape = 'cross_mask', L1 = 0, L2 = 0, h1 = 400, h2 = 400, t = 100, e = 100)  # Ejemplo de uso con cruz
