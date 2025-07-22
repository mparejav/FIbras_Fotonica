import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Se definen los símbolos para incógnitas y parámetros
x, y = sp.symbols('x y')
nD1, nD2, dn1, dn2, P_obj = sp.symbols('nD1 nD2 dn1 dn2 P_obj')

# Se plantea el sistema de ecuaciones igualadas a cero
#    eq1: potencia total del sistema
#    eq2: corrección cromática (deltaP = 0)
eq1 = (nD1 - 1)*2*x + (nD2 - 1)*(-x - y) - P_obj   # eq1 = 0
eq2 = dn1*2*x - dn2*(x + y)                       # eq2 = 0

# Se resuelve el sistema en (x,y)
sol = sp.solve((eq1, eq2), (x, y), dict=True)[0]

# Se recuperan las variables (en este caso los radios)
R1 = 1/sol[x]
R2 = 1/sol[y]

# 5) Se determinan los parámetros numéricos
params = {
    nD1: 1.51100,
    nD2: 1.62100,
    dn1: 1.50868 - 1.51673,
    dn2: 1.61611 - 1.63327,
    P_obj: 1/10  # potencia objetivo en 1/cm
}

R1_val = float(R1.subs(params))
R2_val = float(R2.subs(params))
print(f"R1 = {R1_val:.3f} cm, R2 = {R2_val:.3f} cm")

# Determinación de los focos para colores distintos
# Vidrio Crown: [Rojo, Amarillo, Azul, Violeta]
Crown_Ref_idx = [1.50868, 1.51100, 1.51673, 1.52121]
# Vidrio Flint: [Rojo, Amarillo, Azul, Violeta]
Flint_Ref_idx = [1.61611, 1.62100, 1.63327, 1.64369]

# Para el rojo
data = []
P_Sistema_Rojo = (Crown_Ref_idx[0]-1)*(2/R1_val) + (Flint_Ref_idx[0]-1)*((-1/R1_val)-(1/R2_val))
Foco_Rojo = 1/P_Sistema_Rojo
data.append(("Rojo", Foco_Rojo))

# Para el amarillo
P_Sistema_Amarillo = (Crown_Ref_idx[1]-1)*(2/R1_val) + (Flint_Ref_idx[1]-1)*((-1/R1_val)-(1/R2_val))
Foco_Amarillo = 1/P_Sistema_Amarillo
data.append(("Amarillo", Foco_Amarillo))

# Para el azul
P_Sistema_Azul = (Crown_Ref_idx[2]-1)*(2/R1_val) + (Flint_Ref_idx[2]-1)*((-1/R1_val)-(1/R2_val))
Foco_Azul = 1/P_Sistema_Azul
data.append(("Azul", Foco_Azul))

# Para el violeta
P_Sistema_Violeta = (Crown_Ref_idx[3]-1)*(2/R1_val) + (Flint_Ref_idx[3]-1)*((-1/R1_val)-(1/R2_val))
Foco_Violeta = 1/P_Sistema_Violeta
data.append(("Violeta", Foco_Violeta))

# Impresión de resultados
for color, foco in data:
    print(f"Foco para {color}: {foco:.3f} cm")
    
print(P_Sistema_Rojo)
print(P_Sistema_Amarillo)
print(P_Sistema_Azul)
print(P_Sistema_Violeta)
