import numpy as np
import matplotlib.pyplot as plt

# Constantes del problema
n_core = 1.5
n_clad = 1.0
wavelength = 1e-6  # metros
fiber_height = 1e-6  # metros
increment = 0.01  # incremento en radianes

def func_TE(theta, m):
    term1 = (4 * np.pi * n_core * fiber_height * np.cos(theta)) / wavelength
    sqrt_arg = (n_core**2 / n_clad**2) * (np.sin(theta)**2) - 1
    if sqrt_arg <= 0:
        return None
    term2 = 4 * np.arctan((n_clad / (n_core * np.cos(theta))) * np.sqrt(sqrt_arg))
    return term1 - term2 - 2 * m * np.pi

def func_TM(theta, m):
    term1 = (4 * np.pi * n_core * fiber_height * np.cos(theta)) / wavelength
    sqrt_arg = (n_core**2 / n_clad**2) * (np.sin(theta)**2) - 1
    if sqrt_arg <= 0:
        return None
    term2 = 4 * np.arctan((n_core / (n_clad * np.cos(theta))) * np.sqrt(sqrt_arg))
    return term1 - term2 - 2 * m * np.pi

def bisection_search(func, m, theta_min, theta_max, tol=1e-4):
    a, b = theta_min, theta_max
    fa = func(a, m)
    fb = func(b, m)
    if fa is None or fb is None:
        return None
    if fa * fb > 0:
        return None

    while (b - a) > tol:
        c = (a + b) / 2
        fc = func(c, m)
        if fc is None:
            return None
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return (a + b) / 2


def search_modes(func, label):
    results = []
    m = 0
    theta_c = np.arcsin(n_clad / n_core)
    while True:
        found = False
        theta_left = theta_c
        theta_right = theta_left + increment
        while theta_right < np.pi / 2:
            root = bisection_search(func, m, theta_left, theta_right)
            if root is not None:
                neff = n_core * np.sin(root)
                results.append((m, root, neff))
                theta_left = root + increment
                theta_right = theta_left + increment
                found = True
            else:
                theta_left += increment
                theta_right += increment
        if not found:
            break
        m += 1

    print(f"\nResultados para {label}:")
    for m, theta, neff in results:
        print(f"m = {m}, theta (deg) = {np.degrees(theta):.4f}, neff = {neff:.4f}")

# Ejecutar búsqueda para TE y TM
search_modes(func_TE, "TE")
search_modes(func_TM, "TM")
