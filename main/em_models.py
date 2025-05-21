import numpy as np
from scipy.optimize import minimize, Bounds

def maxwell_garnett_eps(eps_m, eps_i, f, shape="sphere"):
    if shape == "sphere":
        return eps_m + 3*f*eps_m*(eps_i - eps_m)/(eps_i + 2*eps_m - f*(eps_i - eps_m))
    elif shape == "needle":
        return eps_m + f*(eps_i - eps_m)*(eps_i + 5*eps_m)/((3 - 2*f)*eps_i + (3 + 2*f)*eps_m)
    elif shape == "disc":
        return eps_m + f*(eps_i - eps_m)*(2*eps_i + eps_m)/((3 - f)*eps_i + f*eps_m)
    else:
        return None

def bruggeman_eps(eps_m, eps_i, f):
    def objective(x):
        eps_eff = x[0] - x[1]*1j
        left = (eps_i - eps_eff)/(eps_i - eps_m)
        right = (1 - f)*((eps_eff/eps_m)**(1/3))
        return abs(left - right)

    bounds = Bounds([0, 0], [np.inf, np.inf])
    x0 = [eps_m.real, abs(eps_m.imag)]
    result = minimize(objective, x0, bounds=bounds)
    if result.success:
        return result.x[0] - result.x[1]*1j
    else:
        return None

def coherent_potential_eps(eps_m, eps_i, f, shape="sphere"):
    nu_map = {"sphere": 3, "needle": 4, "disc": 2}
    nu = nu_map.get(shape, 3)

    def objective(x):
        eps_eff = x[0] - x[1]*1j
        left = (eps_eff - eps_m)/(eps_eff + 2*eps_m + nu*(eps_eff - eps_m))
        right = f*(eps_i - eps_eff)/(eps_i + 2*eps_m + nu*(eps_eff - eps_m))
        return abs(left - right)

    bounds = Bounds([0, 0], [np.inf, np.inf])
    x0 = [eps_m.real, abs(eps_m.imag)]
    result = minimize(objective, x0, bounds=bounds)
    if result.success:
        return result.x[0] - result.x[1]*1j
    else:
        return None

def mclachlan_eps(eps1, eps2, f, s=1.0, t=1.0, phi_c=0.5):
    def objective(x):
        eps_eff = x[0] - x[1]*1j
        a = (1 - phi_c)/phi_c
        term1 = f * (eps1**(1/s) - eps_eff**(1/s)) / (eps1**(1/s) + a * eps_eff**(1/s))
        term2 = (1 - f) * (eps2**(1/t) - eps_eff**(1/t)) / (eps2**(1/t) + a * eps_eff**(1/t))
        return abs(term1 + term2)

    bounds = Bounds([0, 0], [np.inf, np.inf])
    x0 = [(eps1.real + eps2.real)/2, abs((eps1.imag + eps2.imag)/2)]
    result = minimize(objective, x0, bounds=bounds)
    if result.success:
        return result.x[0] - result.x[1]*1j
    else:
        return None
