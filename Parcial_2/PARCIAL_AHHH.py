import numpy as np
import matplotlib.pyplot as plt

NFK5 = 1.4875

SF5 = 1.6727

NLAK9 = 1.6910

NLAK10 = 1.7200

F2 = 1.6200

SF4 = 1.7552

# Parámetros
Ref_idx = [NFK5, SF5, NLAK9, NLAK10, F2, SF4, NLAK10, NLAK9, NLAK9] # Indices de refracción
Radio = [5.4309, 2.3942, -3.8629, -5.5409, -16.0642, -6.5538, 4.3769, -4.1619, 9.8038, -3.8829, 5.4280, 35.4552, -3.2140, 3.2160, -36.2242, 2.0680, 1.6121]  # radios de curvatura
Distance = [0.7220, 1.2934, 0.7140, 0.0115, 1.6219, 0.0134, 1.6521, 0.4850, 2.1154, 0.1769, 0.0844, 0.3503, 0.0100, 0.6218, 0.0004, 0.5136]  # distancias
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
    
M_LG1 = Lente_Gruesa(n_aire, NFK5, n_aire, Radio[0], Radio[1], Distance[0])

T_23 = Traslation(Distance[1], n_aire)

M_LG2 = Lente_Gruesa(n_aire, SF5, n_aire, Radio[2], Radio[3], Distance[2])

T_45 = Traslation(Distance[3], n_aire)

M_LG3 = Lente_Gruesa(n_aire, NLAK9, n_aire, Radio[4], Radio[5], Distance[4])

T_67 = Traslation(Distance[5], n_aire)

M_LG4 = Lente_Gruesa(n_aire, NLAK10, F2, Radio[6], Radio[7], Distance[6])

T_89 = Traslation(Distance[7], F2)

Ra_9 = Transmition(n_aire, F2, Radio[8])

T_9_10 = Traslation(Distance[8], n_aire)

M_LG5 = Lente_Gruesa(n_aire, SF4, n_aire, Radio[9], Radio[10], Distance[9])

T_11_12 = Traslation(Distance[10], n_aire)

M_LG6 = Lente_Gruesa(n_aire, NLAK10, n_aire, Radio[11], Radio[12], Distance[11])

T_13_14 = Traslation(Distance[12], n_aire)

M_LG7 = Lente_Gruesa(n_aire, NLAK9, n_aire, Radio[13], Radio[14], Distance[13])

T_15_16 = Traslation(Distance[14], n_aire)

M_LG8 = Lente_Gruesa(n_aire, NLAK9, n_aire, Radio[15], Radio[16], Distance[15])

# Definicion matriz 

M = M_LG8 @ T_15_16 @ M_LG7 @ T_13_14 @ M_LG6 @ T_11_12 @ M_LG5 @ T_9_10 @ Ra_9 @ T_89 @ M_LG4 @ T_67 @ M_LG3 @ T_45 @ M_LG2 @ T_23 @ M_LG1

# # Componentes de la matriz 
    
M11 = float(M[0,0])
M12 = float(M[0,1])
M22 = float(M[1,1])

Poder_Sistema = -M12

Distancia_Focal_Sistema = 1/Poder_Sistema

Distancia_FocalP_Sistema = -Distancia_Focal_Sistema

D_p = Vertice_a_Plano(n_aire, M12, M22)

D = Plano_a_Vertice(M12, M11, n_aire)

s = Objeto_a_plano(Distancia_Objeto_V1, D)

sp = Plano_a_Imagen(Poder_Sistema, s)

m_x = mag_lat(n_aire, n_aire, s, sp)

Distancia_Imagen = D_p + sp

m_a = mag_ang(n_aire, n_aire, s, Poder_Sistema)

altura = 0

Tamaño = altura * m_x

print(Distancia_Imagen)

print(m_x)

print(m_a)



