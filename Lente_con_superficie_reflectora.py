import numpy as np
import matplotlib.pyplot as plt

# Ejercicio 10-11: Lente con superficie reflectora 

n_aire = 1
n_vidrio = 1.5
Radio = 6 #cm
Espesor_lente = 2 #cm
Alto_objeto = 2 #cm

Dist_Objeto_Vertice = 15/22 #cm

# Funciones de matrices
def Transmition(n_t, n_i, R):
    P = (n_t - n_i) / R
    return np.array([
        [1, -P],
        [0, 1]
    ])
    
def Reflection(n_i, R):
    return np.array([
    [1, 2*(n_i/R)],
    [0, 1]
])
    
def Traslation(D, n):
    return np.array([
        [1, 0],
        [D/n, 1]
    ])
    
# Definicion de matrices del sistema 
    
R_a1 = Transmition(n_vidrio, n_aire, Radio)    

T_12 = Traslation(Espesor_lente, n_vidrio)

Re = Reflection(n_vidrio, -Radio)

T_21 = Traslation(Espesor_lente, n_vidrio)

R_a2 = Transmition(n_aire, n_vidrio, -Radio)
    
# Definicion matriz Lente con superficie reflectora   
    
M = R_a2 @ T_21 @ Re @ T_12 @ R_a1  

# Componentes de la matriz 
    
M11 = float(M[0,0])

M12 = float(M[0,1])

M22 = float(M[1,1])

# Distancias de los planos principales a los vertices de la matriz 
    
D = (n_aire/M12)*(1-M11)

D_p = (n_aire/M12)*(1-M22)

Poder_Sistema = -M12

# Distancia objeto e imagen a planos principales

s = Dist_Objeto_Vertice - D

s_p = (n_aire)/(Poder_Sistema-(n_aire/s))

# Magnificaciones

mag_lat = -(n_aire/n_aire)*(s_p/s)

mag_ang = -(s/s_p)

# Resultados

Posicion_imagen = s_p + D_p

Tamaño = Alto_objeto * mag_lat

    
print(M)

print(mag_lat)

print(mag_ang)

print(Tamaño)

print(Posicion_imagen)



