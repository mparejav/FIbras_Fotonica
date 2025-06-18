import numpy as np
import matplotlib.pyplot as plt

# Parámetros
Ref_idx = [1.812, 1.695, 1.812] # Indices de refracción
Radio = [11.5, -127, -23.5, 10.2, 30.0, -15.0]  # radios de curvatura
Distance = [5, 1.25, 1.55, 2.50, 5]  # distancias
Focos = []

n_aire = 1

Distancia_Objeto_V1 = 200

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

def Foco_Lente_Delgada (n_L, R_i, R_t):
    
    Foco = 1/((n_L - 1)*((1/R_i)-(1/R_t)))
    
    return Foco

def Lente_Delgada(n_L, R_i, R_t):       # Para cuando me dan radios y indice de la lente
    
    Foco = 1/((n_L - 1)*((1/R_i)-(1/R_t)))
    
    return np.array ([
        [1, -1/Foco],
        [0, 1]
    ])
    
def Lente_Delgada_F(F):                   # Para cuando me dan solo el foco de la lente delgada

    return np.array ([
        [1, -1/F],
        [0, 1]
    ])


def Objeto_a_plano(Dist_Obj_Vert1, Dist_Vert1_PlanoH): # Distancia del objeto al plano principal H
    
    s = Dist_Obj_Vert1 - Dist_Vert1_PlanoH #D
    
    return s

def Plano_a_Vertice(M12, M11, n): # Distancia del plano principal H al vertice inicial del sistema optico o lente
    
    D = (n/M12)*(1-M11)
    
    return D


def Vertice_a_Plano(n, M12, M22):# Distancia del vertice final al plano principal H'
    
    D_p = (n/M12)*(1-M22)
    
    return D_p

def Plano_a_Imagen(Poder_Sistema, s):   # Distancia de la imagen al plano principal H'
    
    s_p = (n_aire)/(Poder_Sistema-(n_aire/s))
    
    return s_p


    
def mag_lat(n,np, s, sp):
    
    m_x = -(n/np)*(sp/s)
    
    return m_x
    
def mag_ang(n, np, s, Poder):
    
    m_a = (n/np)*(1-(s/n)*Poder)
    
    return m_a


#Posicion_imagen = s_p + D_p

#Tamaño = Alto_objeto * mag_lat

#foco_sistema = 1/Poder_Sistema

#Lf = foco_sistema + D

#Lf_p = foco_sistema + D_p



# Definicion de matrices del sistema 

M_L1 = Lente_Gruesa(n_aire, Ref_idx[0], n_aire, Radio[0], Radio[1], Distance[0])

T_12 = Traslation(Distance[1], n_aire)

M_L2 = Lente_Gruesa(n_aire, Ref_idx[1], n_aire, Radio[2], Radio[3], Distance[2])

T_45 = Traslation(Distance[3], n_aire)

M_L3 = Lente_Gruesa(n_aire, Ref_idx[2], n_aire, Radio[4], Radio[5], Distance[4])

# Definicion matriz 

M = M_L3 @ T_45 @ M_L2 @ T_12 @ M_L1

# # Componentes de la matriz 
    
M11 = float(M[0,0])
M12 = float(M[0,1])
M22 = float(M[1,1])

Poder_Sistema = -M12

D_p = Vertice_a_Plano(n_aire, M12, M22)

D = Plano_a_Vertice(M12, M11, n_aire)

s = Objeto_a_plano(Distancia_Objeto_V1, D)

sp = Plano_a_Imagen(Poder_Sistema, s)

m_x = mag_lat(n_aire, n_aire, s, sp)

Distancia_Imagen = D_p + sp

print(sp)

print(Distancia_Imagen)

print(m_x)

print(M)

print(s)

