import numpy as np
import matplotlib.pyplot as plt

# Parámetros
Ref_idx = [1.6116, 1.6053, 1.5123, 1.6116] # Indices de refracción
Radio = [1.628, 27.57, 3.457, 1.582, np.inf, 1.920, 2.394]  # radios de curvatura
Distance = [0.357, 0.189, 0.081, 0.325, 0.217, 0.396]  # distancias

n_aire = 1
n_p = 1

# Funciones de matrices
def Traslation(D, n):
    return np.array([
        [1, 0],
        [D/n, 1]
    ])

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
    
def Lente_Gruesa(n_i, n_L, n_t, R_i, R_t, D):
    
    Refraction_v1 = Transmition(n_L, n_i, R_i)
    
    Traslation_v12 = Traslation(D, n_L)
    
    Refraction_v2 = Transmition(n_t, n_L, R_t)
    
    M = Refraction_v2 @ Traslation_v12 @ Refraction_v1
    
    return M

# Definicion de matrices del sistema 
    
M_12 = Lente_Gruesa(n_aire, Ref_idx[0], n_aire, Radio[0], Radio[1], Distance[0])

T_23 = Traslation(Distance[1], n_aire)

M_34 = Lente_Gruesa(n_aire, Ref_idx[1], n_aire, Radio[2], Radio[3], Distance[2])

T_45 = Traslation(Distance[3], n_aire)

M_56 = Lente_Gruesa(n_aire, Ref_idx[2], Ref_idx[3], Radio[4], Radio[5], Distance[4])

T_67 = Traslation(Distance[5], Ref_idx[3])

Ra_7 = Transmition(n_aire, Ref_idx[3], Radio[6])

# Definicion matriz Lente Tessar
    
M = Ra_7 @ T_67 @ M_56 @ T_45 @ M_34 @ T_23 @ M_12 

# Componentes de la matriz 
    
M11 = float(M[0,0])

M12 = float(M[0,1])

M22 = float(M[1,1])

# Distancias de los planos principales a los vertices de la matriz 
    
D = (n_aire/M12)*(1-M11)

D_p = (n_aire/M12)*(1-M22)

Poder_Sistema = -M12

# Distancia objeto e imagen a planos principales (NO NOS IMPORTA EN ESTE EJERCICIO)

#s = Dist_Objeto_Vertice - D

#s_p = (n_aire)/(Poder_Sistema-(n_aire/s))

# Magnificaciones

#mag_lat = -(n_aire/n_aire)*(s_p/s)

# mag_ang = -(s/s_p)

#Posicion_imagen = s_p + D_p

#Tamaño = Alto_objeto * mag_lat

foco_sistema = 1/Poder_Sistema

Lf = foco_sistema + D

Lf_p = foco_sistema + D_p

print(D)

print(D_p)

print(Lf)

print(Lf_p)

print(foco_sistema)

print(M)