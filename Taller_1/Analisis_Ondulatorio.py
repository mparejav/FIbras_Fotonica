import math
from typing import Callable, List

# --- Utilidades numéricas --------------------------------------------------

def bounded_tan(phi: float, eps: float = 1e-6, max_val: float = 1e3) -> float:
    """Versión acotada de tan(phi).

    - Si |tan(phi)| < eps  ⇒ devuelve ±eps para evitar divisiones por cero.
    - Si |tan(phi)| > max_val ⇒ satura al valor máximo permitido para evitar
      desbordamientos que arruinen la detección de cambio de signo.
    """
    t = math.tan(phi)
    if abs(t) < eps:
        t = math.copysign(eps, t)
    elif abs(t) > max_val:
        t = math.copysign(max_val, t)
    return t

# --- Método de bisección ----------------------------------------------------

def bisection_method(
    func: Callable[[float], float],
    start: float,
    end: float,
    increment: float = 0.001,
    tol: float = 1e-7,
) -> List[float]:
    """Encuentra todas las raíces de *func* en [start, end] mediante barrido + bisección.

    Estrategia:
    1. Muestrea el intervalo con paso *increment* y localiza cambios de signo.
    2. En cada sub‑intervalo con signo opuesto refina la raíz con bisección
       hasta que el tamaño de intervalo sea < *tol*.
    3. Devuelve las raíces ordenadas y sin duplicados (según *tol*).
    """
    roots: List[float] = []
    left, right = start, start + increment

    f_left = func(left)
    # Añadir raíz exacta en el borde izquierdo
    if abs(f_left) < tol:
        roots.append(left)

    while right <= end:
        f_right = func(right)

        # Detectar cambio de signo
        if f_left * f_right < 0:
            a, b = left, right
            while (b - a) / 2 > tol:
                mid = (a + b) / 2
                f_mid = func(mid)
                if f_left * f_mid <= 0:
                    b, f_right = mid, f_mid
                else:
                    a, f_left = mid, f_mid
            root = (a + b) / 2
            if all(abs(root - r) > tol for r in roots):
                roots.append(root)
            # Reiniciar para continuar la búsqueda tras la raíz encontrada
            left, right = root + increment, root + 2 * increment
            f_left = func(left) if left <= end else 0.0
            continue

        # Desplazar ventana
        left, f_left = right, f_right
        right += increment

    return sorted(roots)

# --- Parámetros de la guía --------------------------------------------------

n_core = 1.5
n_clad = 1.0
wavelength = 1e-6  # [m]
height = 1e-6      # [m]

k0 = 2 * math.pi / wavelength
V = (k0 * height / 2) * math.sqrt(n_core**2 - n_clad**2)

# Para los modos TM el primer cruce puede ocurrir un poco después de V.
# Amplía el rango a 1.5·V para asegurarte de capturar todas las raíces.
phi_max = 1.5 * V

# --- Funciones de dispersión -----------------------------------------------

def E_TE_even(phi: float) -> float:
    return phi**2 + (phi * bounded_tan(phi))**2 - V**2


def E_TE_odd(phi: float) -> float:
    t = bounded_tan(phi)
    return phi**2 + (phi / t)**2 - V**2


def E_TM_even(phi: float) -> float:
    ratio2 = (n_clad / n_core)**2
    return phi**2 + (ratio2 * phi * bounded_tan(phi))**2 - V**2


def E_TM_odd(phi: float) -> float:
    ratio2 = (n_clad / n_core)**2
    t = bounded_tan(phi)
    return phi**2 + (ratio2 * phi / t)**2 - V**2

# --- Cálculo de θ y n_eff ---------------------------------------------------

def theta_neff(phi_roots: List[float], alpha_roots: List[float]):
    betas = []
    for phi, alpha in zip(phi_roots, alpha_roots):
        kappa = 2 * phi / height
        gamma = 2 * alpha / height
        beta_k = math.sqrt(max((n_core * k0)**2 - kappa**2, 0.0))
        beta_g = math.sqrt(max(gamma**2 + (n_clad * k0)**2, 0.0))
        betas.append((beta_k + beta_g) / 2)

    thetas = [math.asin(b / (n_core * k0)) for b in betas]
    thetas_deg = [math.degrees(t) for t in thetas]
    n_eff = [n_core * math.sin(t) for t in thetas]
    return thetas_deg, n_eff

# --- Ejecución principal ----------------------------------------------------

if __name__ == "__main__":
    modes = [
        ("TE pares", E_TE_even, lambda phi: phi * bounded_tan(phi)),
        ("TE impares", E_TE_odd, lambda phi: -phi / bounded_tan(phi)),
        ("TM pares", E_TM_even, lambda phi: (n_clad / n_core)**2 * phi * bounded_tan(phi)),
        ("TM impares", E_TM_odd, lambda phi: -(n_clad / n_core)**2 * phi / bounded_tan(phi)),
    ]

    for name, func_E, alpha_fn in modes:
        phi_roots = bisection_method(func_E, 0.0, phi_max)
        alpha_roots = [alpha_fn(phi) for phi in phi_roots]
        thetas_deg, n_eff = theta_neff(phi_roots, alpha_roots)
        print(f"{name}: φ_roots = {[round(p,4) for p in phi_roots]}")
        print(f"  Thetas (deg): {thetas_deg}")
        print(f"  n_eff: {n_eff}\n")

# --- Pruebas unitarias mínimas ---------------------------------------------

def _test_bounded_tan():
    assert abs(bounded_tan(0)) >= 1e-6
    assert abs(bounded_tan(math.pi / 2 - 1e-6)) <= 1e3
    assert abs(bounded_tan(math.pi / 2 + 1e-6)) <= 1e3


def _test_bisection_linear():
    root = bisection_method(lambda x: x - 2, 0, 4, increment=0.1)
    assert any(abs(r - 2) < 1e-6 for r in root)

# Ejecutar pruebas cuando se llama python file.py -m pytest, por ejemplo
if __name__ == "__pytest__":
    _test_bounded_tan()
    _test_bisection_linear()
