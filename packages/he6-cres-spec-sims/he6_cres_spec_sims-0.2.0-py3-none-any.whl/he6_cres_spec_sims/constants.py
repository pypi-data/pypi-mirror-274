'''Constants used throughout spec sims'''
import math

##### Math constants #####
PI = math.pi
RAD_TO_DEG = 180 / math.pi
P11_PRIME = 1.84118  # First zero of J1 prime (bessel function)

##### Physics constants. #####

ME = 5.10998950e5  # Electron rest mass (eV).
M = 9.1093837015e-31  # Electron rest mass (kg).
Q = 1.602176634e-19  # Electron charge (Coulombs).
C = 299792458  # Speed of light in vacuum (m/s)
J_TO_EV = 6.241509074e18  # Joule-ev conversion
EPS_0 = 8.8541878128 * 10**-12  # Vacuum Permittivity (F/m)
mu0 = 4 * math.pi * 1e-7
p11prime = 1.84118