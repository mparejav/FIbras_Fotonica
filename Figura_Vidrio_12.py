import numpy as np
import matplotlib.pyplot as plt

# Ejercicio 12 : Figura hecha de vidrio

n_vidrio = 1.5
n_aire = 1

R1 = 2 #cm
R2 = 2*R1
Dist_centros = 0  # Distancia entre los centros de las SREs
H = 0.5*R1  # Distancia del objeto al vértice izq

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
    
# Definición de la matriz de la figura de vidrio

R_a1 = Transmition(n_vidrio, n_aire, R1)

T_12 = Traslation(R1+Dist_centros+R2, n_vidrio)

R_a2 = Transmition(n_aire, n_vidrio, -R2)

# Definición de la matriz

M = R_a2 @ T_12 @ R_a1

# Componentes de la matriz 
    
M11 = float(M[0,0])

M12 = float(M[0,1])

M22 = float(M[1,1])

# Distancias de los planos principales a los vertices de la matriz 
    
D = (n_aire/M12)*(1-M11)

D_p = (n_aire/M12)*(1-M22)

Poder_Sistema = -M12

# Distancia objeto e imagen a planos principales

s = H - D

s_p = (n_aire)/(Poder_Sistema-(n_aire/s))

# Resultados

Posicion_imagen = s_p + D_p

print(M)

print(D_p)

print(D)

print(Posicion_imagen)

