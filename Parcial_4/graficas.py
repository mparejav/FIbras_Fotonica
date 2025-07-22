import numpy as np
import matplotlib.pyplot as plt

def intensidad(campo, ventanaX, ventanaY, min=0, max=1):
    ''' Grafica un patron de intensidad del campo ingresado    
    ENTRADAS:
    - campo: campo optico al que se le quiere representar su intensidad
    - ventana: longitud de la ventana que se desea graficar, se grafica en una ventana cuadrada

    RETORNA: Nada, solo despliega una ventana emergente con el grafico de la intensidad del campo optico que se quiere representar '''

    ''' Definir los parametros para poder realizar la grafica '''
    limites_eje = np.array([-ventanaX/2, ventanaX/2, -ventanaY/2, ventanaY/2]) #definimos los valores de los ejes del campo que vamos a representar
    campo_Intensidad = (np.abs(campo))**2 #calculamos la intensidad del campo que se ponga en la entrada

    ''' GRAFICAR '''
    plt.imshow(campo_Intensidad, extent = limites_eje, origin='lower', cmap='gray', vmin= min*np.max(campo_Intensidad), vmax=max*np.max(campo_Intensidad)) #generamos la grafica
    plt.colorbar(label="Intensidad") #agregamos la barra de color para representar la intensidad
    plt.xlabel("X (m)") #ponemos etiquetas en los ejes
    plt.ylabel("Y (m)") #ponemos etiquetas en los ejes
    plt.title("Mapa de Intensidad") #agregamos un titulo en el grafico
    plt.show() #mostramos el grafico

def intensidad_Logaritmica(campo, ventanaX, ventanaY, vmin = 0, vmax = 1):
    ''' Grafica un patron de intensidad del campo ingresado en escala logaritmica 
    ENTRADAS:
    - campo: campo optico al que se le quiere representar su intensidad
    - ventana: longitud de la ventana que se desea graficar, se grafica en una ventana cuadrada

    RETORNA: Nada, solo despliega una ventana emergente con el grafico de la intensidad del campo optico que se quiere representar '''

    ''' Definir los parametros para poder realizar la grafica '''
    limites_eje = np.array([-ventanaX/2, ventanaX/2, -ventanaY/2, ventanaY/2]) #definimos los valores de los ejes del campo que vamos a representar
    campo_Intensidad = (np.abs(campo))**2 #calculamos la intensidad del campo que se ponga en la entrada
    intensidad_Logaritmica = np.log(1 + campo_Intensidad)

    ''' GRAFICAR '''
    plt.imshow(intensidad_Logaritmica, extent = limites_eje, origin='lower', cmap='gray', vmin=vmin*np.max(intensidad_Logaritmica), vmax=vmax*np.max(intensidad_Logaritmica)) #generamos la grafica
    plt.colorbar(label="Intensidad") #agregamos la barra de color para representar la intensidad
    plt.xlabel("X (m)") #ponemos etiquetas en los ejes
    plt.ylabel("Y (m)") #ponemos etiquetas en los ejes
    plt.title("Mapa de Intensidad en escala logaritmica") #agregamos un titulo en el grafico
    plt.show() #mostramos el grafico

def fase(campo, ventana_X, ventana_Y):
    ''' Grafica un mapa de fase del campo ingresado    
    ENTRADAS:
    - campo: campo optico al que se le quiere representar su distribucion de fase
    - ventana: longitud de la ventana que se desea graficar, se grafica en una ventana cuadrada

    RETORNA: Nada, solo despliega una ventana emergente con el grafico de la distribucion de fase del campo optico que se quiere representar '''

    ''' Definir los parametros para poder realizar la grafica '''
    limites_eje = np.array([-ventana_X/2, ventana_X/2, -ventana_Y/2, ventana_Y/2])
    campo_Fase = np.angle(campo) #calculamos la intensidad del campo que se ponga en la entrada

    ''' GRAFICAR '''
    plt.imshow(campo_Fase, extent = limites_eje, origin='lower', cmap='viridis') #generamos la grafica
    plt.colorbar(label="Fase") #agregamos la barra de color para representar la distribucion de fase
    plt.xlabel("X (m)") #ponemos etiquetas en los ejes
    plt.ylabel("Y (m)") #ponemos etiquetas en los ejes
    plt.title("Mapa de fase") #agregamos un titulo en el grafico
    plt.show() #mostramos el grafico

def intensidad_EjeX(campo, ventana):
    """
    Grafica la intensidad en función de la posición en el eje X, utilizando una ventana de tamaño específico.
    ENTRADAS:
        campo == Array NumPy 2D que contiene los datos de intensidad.
        ventana == Float que representa el tamaño de la ventana en las unidades deseadas.
    RETORNA:
        Gráfico Intensidad vs posición en el eje X
    """
    campo = np.abs(campo)**2                                #Para obtener la intensidad    
    fila_central = campo.shape[0] // 2                      # Seleccionar la fila central para graficar
    intensidades_X = campo[fila_central, :]                 # Obtener los valores de intensidad de la fila central
    num_puntos_a_graficar = int(intensidades_X.shape[0])    # Calcular el número de puntos a graficar
    # Crear una lista de posiciones en el eje x
    # Asumimos que el centro de la ventana coincide con el centro de la fila
    posiciones_X = np.linspace(-ventana/2, ventana/2, num_puntos_a_graficar)
    # Graficas
    plt.plot(posiciones_X, intensidades_X[:num_puntos_a_graficar])
    plt.xlabel('Posición (m)')
    plt.ylabel('Intensidad')
    plt.title('Intensidad vs. Posición')
    plt.show()
        
def graficar_abertura(Nx, Ny, x_0, y_0, x_1, y_1, x_2, y_2, L, e, t, h_1, h_2, mostrar=True):
    '''Grafica la abertura espacial en el plano de la rendija. 
       Devuelve la matriz de la abertura A(x,y)
    '''
    # Coordenadas del plano de abertura
    x_ap = np.linspace(-100e-6, 100e-6, Nx)
    y_ap = np.linspace(-100e-6, 100e-6, Ny)
    X_ap, Y_ap = np.meshgrid(x_ap, y_ap)

    A = np.zeros((Ny, Nx))

    # Abertura horizontal
    mask1 = (np.abs(X_ap - x_0) <= L/2) & (np.abs(Y_ap - y_0) <= e/2)
    A[mask1] = 1

    # Abertura vertical superior
    mask2 = (np.abs(X_ap - x_1) <= t/2) & (np.abs(Y_ap - y_1) <= h_1/2)
    A[mask2] = 1

    # Abertura vertical inferior
    mask3 = (np.abs(X_ap - x_2) <= t/2) & (np.abs(Y_ap - y_2) <= h_2/2)
    A[mask3] = 1

    if mostrar:
        plt.figure(figsize=(6, 5))
        plt.imshow(A, extent=[x_ap[0]*1e6, x_ap[-1]*1e6, y_ap[0]*1e6, y_ap[-1]*1e6], cmap='gray', origin='lower')
        plt.xlabel("x (µm)")
        plt.ylabel("y (µm)")
        plt.title("Abertura en el plano físico")
        plt.colorbar(label="Transparencia")
        plt.tight_layout()
        plt.show()

    return A

