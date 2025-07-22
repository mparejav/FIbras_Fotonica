import numpy as np
import matplotlib.pyplot as plt

# Parámetros
Ref_idx = [1.812, 1.695, 1.812]   # n_1, n_2, n_3
Radio = [11.5, -127, -23.5, 10.2, 30.0, -15.0]  # radios de curvatura
Distance = [200, 5.00, 1.25, 1.55, 2.50, 5.00]  # distancias

n = 1
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

# Construcción de la matriz total
T_01 = Traslation(Distance[0], 1)

R_1 = Transmition(Ref_idx[0], 1, Radio[0])

T_12 = Traslation(Distance[1], Ref_idx[0])

R_2 = Transmition(1, Ref_idx[0], Radio[1])

T_23 = Traslation(Distance[2], 1)

R_3 = Transmition(Ref_idx[1], 1, Radio[2])

T_34 = Traslation(Distance[3], Ref_idx[1])

R_4 = Transmition(1, Ref_idx[1], Radio[3])

T_45 = Traslation(Distance[4], 1)

R_5 = Transmition(Ref_idx[2], 1, Radio[4])

T_56 = Traslation(Distance[5], Ref_idx[2])

R_6 = Transmition(1, Ref_idx[2], Radio[5])

M_16 = R_6 @ T_56 @ R_5 @ T_45 @ R_4 @ T_34 @ R_3 @ T_23 @ R_2 @ T_12 @ R_1

print(M_16)

M11 = float(M_16[0,0])

M12 = float(M_16[0,1])

M22 = float(M_16[1,1])

D = (n/M12)*(1-M11)

D_p = (n_p/M12)*(1-M22)

Poder_Sistema = -M12

print(D)

print(D_p)

s = Distance[0]-D

s_p = (n_p)/(Poder_Sistema-(n/s))

mag_lat = -(n/n_p)*(s_p/s)

mag_ang = -(s/s_p)

print(s)

print(s_p)

print (mag_ang)

print(mag_lat)

