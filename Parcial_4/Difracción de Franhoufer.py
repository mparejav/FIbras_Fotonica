import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Funciones para generar las formas geométricas
def crear_circulo(tamaño, radio_en_pixeles):
    x, y = np.ogrid[:tamaño, :tamaño]
    centro = tamaño // 2
    mascara = (x - centro) ** 2 + (y - centro) ** 2 <= int(radio_en_pixeles) ** 2
    return np.where(mascara, 1, 0)

def crear_rectangulo(tamaño, ancho_en_pixeles, alto_en_pixeles):
    rectangulo = np.zeros((tamaño, tamaño))
    centro = tamaño // 2
    rectangulo[centro - int(alto_en_pixeles)//2:centro + int(alto_en_pixeles)//2,
               centro - int(ancho_en_pixeles)//2:centro + int(ancho_en_pixeles)//2] = 1
    return rectangulo

def crear_rendija(tamaño, ancho_en_pixeles):
    rendija = np.zeros((tamaño, tamaño))
    centro = tamaño // 2
    rendija[:, centro - int(ancho_en_pixeles)//2:centro + int(ancho_en_pixeles)//2] = 1
    return rendija

def cargar_imagen(imagen_path, tamaño):
    img = Image.open(imagen_path).convert('L')
    img = img.resize((tamaño, tamaño))
    img_array = np.array(img)
    # Normalizar la imagen para que los blancos sean 1 (apertura) y los negros sean 0 (obstáculo)
    return np.where(img_array > 128, 1, 0)

# Simulación de la difracción de Fraunhofer
def difraccion_fraunhofer(apertura):
    fft = np.fft.fftshift(np.fft.fft2(apertura))
    intensidad = np.abs(fft) ** 2
    return intensidad

# Función para convertir unidades físicas a píxeles
def convertir_a_pixeles(unidad_fisica, tamaño_fisico_total, tamaño_matriz):
    # Convertimos las unidades físicas (en mm) a píxeles
    factor_conversion = tamaño_matriz / tamaño_fisico_total  # píxeles por milímetro
    return unidad_fisica * factor_conversion

# Función principal para elegir la forma
def elegir_geometria():
    tamaño_matriz = 2048
    # Tamaño de la matriz (píxeles)
    tamaño_fisico_total = 10 #float(input("Introduce el tamaño físico del lado de la apertura en mm "))  # en mm

    print("Elige una forma geométrica:")
    print("1. Círculo")
    print("2. Rectángulo")
    print("3. Rendija")
    print("4. Cargar imagen .jpg")

    opcion = int(input("Introduce el número de la opción: "))

    if opcion == 1:
        radio_fisico = float(input("Introduce el radio del círculo (en mm): "))
        # Convertimos el radio físico a píxeles
        radio_en_pixeles = convertir_a_pixeles(radio_fisico, tamaño_fisico_total, tamaño_matriz)
        apertura = crear_circulo(tamaño_matriz, radio_en_pixeles)
    elif opcion == 2:
        ancho_fisico = float(input("Introduce el ancho del rectángulo (en mm): "))
        alto_fisico = float(input("Introduce el alto del rectángulo (en mm): "))
        # Convertimos las dimensiones físicas a píxeles
        ancho_en_pixeles = convertir_a_pixeles(ancho_fisico, tamaño_fisico_total, tamaño_matriz)
        alto_en_pixeles = convertir_a_pixeles(alto_fisico, tamaño_fisico_total, tamaño_matriz)
        apertura = crear_rectangulo(tamaño_matriz, ancho_en_pixeles, alto_en_pixeles)
    elif opcion == 3:
        ancho_fisico = float(input("Introduce el ancho de la rendija (en mm): "))
        # Convertimos el ancho físico a píxeles
        ancho_en_pixeles = convertir_a_pixeles(ancho_fisico, tamaño_fisico_total, tamaño_matriz)
        apertura = crear_rendija(tamaño_matriz, ancho_en_pixeles)
    elif opcion == 4:
        imagen_path = input("Introduce la ruta de la imagen .jpg: ")
        apertura = cargar_imagen(imagen_path, tamaño_matriz)
    else:
        print("Opción no válida")
        return

    # Calcular la difracción de Fraunhofer
    intensidad = difraccion_fraunhofer(apertura)

    # Mostrar resultados
    plt.figure(figsize=(10, 5))

    # Apertura
    plt.subplot(1, 2, 1)
    plt.title('Apertura')
    plt.imshow(apertura, cmap='gray')

    # Patrón de difracción
    plt.subplot(1, 2, 2)
    plt.title('Difracción de Fraunhofer')
    plt.imshow(np.log(intensidad + 1), cmap='inferno')

    plt.show()

# Ejecutar la función principal
elegir_geometria()