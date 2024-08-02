import matplotlib.pyplot as plt
import numpy as np

R = 8.314  # J/mol-K
x = 1
y = 4

# NASA Polynomial Constants
ch4_coeffs_l = [5.14987613E+00, -1.36709788E-02, 4.91800599E-05, -4.84743026E-08, 1.66693956E-11, -1.02466476E+04, -4.64130376E+00]
o2_coeffs_l = [3.78245636E+00, -2.99673416E-03, 9.84730201E-06, -9.68129509E-09, 3.24372837E-12, -1.06394356E+03, 3.65767573E+00]
n2_coeffs_l = [0.03298677E+02, 0.14082404E-02, -0.03963222E-04, 0.05641515E-07, -0.02444854E-10, -0.10208999E+04, 0.03950372E+02]

n2_coeffs_h = [0.02926640E+02, 0.14879768E-02, -0.05684760E-05, 0.10097038E-09, -0.06753351E-13, -0.09227977E+04, 0.05980528E+02]
co2_coeffs_h = [3.85746029E+00, 4.41437026E-03, -2.21481404E-06, 5.23490188E-10, -4.72084164E-14, -4.87591660E+04, 2.27163806E+00]
h2o_coeffs_h = [3.03399249E+00, 2.17691804E-03, -1.64072518E-07, -9.70419870E-11, 1.68200992E-14, -3.00042971E+04, 4.96677010E+00]
o2_coeffs_h =  [3.78245636E+00, -2.99673416E-03, 9.84730201E-06, -9.68129509E-09, 3.24372837E-12, -1.06394356E+03, 3.65767573E+00]
co_coeffs_h = [2.71518561E+00, 2.06252743E-03, -9.98825771E-07, 2.30053008E-10, -2.03647716E-14, -1.41518724E+04, 7.81868772E+00]

# Function to evaluate Enthalpy
def h(T, co_effs):
    a1, a2, a3, a4, a5, a6, _ = co_effs  # Ignoring the last coefficient
    return (a1 + a2*T/2 + a3*T*2/3 + a4*T*3/4 + a5*T*4/5 + a6/T)*R*T  # Corrected T*3

# Function that represents the root finding problem
def f(T, phi, a, b, c, d, e):
    # Products At Temperature T
    h_co2_p = h(T, co2_coeffs_h)
    h_h2o_p = h(T, h2o_coeffs_h)
    h_n2_p = h(T, n2_coeffs_h)
    h_o2_p = h(T, o2_coeffs_h)
    h_co_p = h(T, co_coeffs_h)
     
    H_products = a*h_co2_p + b*h_h2o_p + c*h_n2_p + d*h_o2_p + e*h_co_p
    n_products = a + b + c + d + e
    nRT_products = n_products * R * T

    # Reactants At Standard Temperature
    T_std = 298.15
    h_ch4_r = h(T_std, ch4_coeffs_l)
    h_o2_r = h(T_std, o2_coeffs_l)
    h_n2_r = h(T_std, n2_coeffs_l)

    H_reactants = h_ch4_r + g*h_o2_r + 3.76*g*h_n2_r
    n_reactants = 1 + g + 3.76*g
    nRT_reactants = n_reactants * R * T_std

    return (H_products - H_reactants) - (nRT_products - nRT_reactants)


def n_tot(phi, a, b):
    n_tot = a + b/2 + (a + b/4)*phi*(1-phi + 3.76)
    return n_tot
# Function to calculate the derivative using central difference
def fprime(T, phi, a, b, c, d, e):
    h = 1e-6  # Step size for numerical differentiation
    return (f(T + h, phi, a, b, c, d, e) - f(T - h, phi, a, b, c, d, e)) / (2 * h)

# Calculating the temperature and storing the values
T_py = []
X_co2 = []
X_co = []
X_h2o = []
X_h2 = []
X_o2 = []
X_n2 = []

n_tots= []
phi_min = 0.5
phi_max = 2
phi_diff = 0.05
phi_values = np.arange(phi_min, phi_max + phi_diff, phi_diff)

for phi_value in phi_values:
    if phi_value == 1:
        ar = x + y/4
        g = ar
        a = x
        b = y/2
        c = 3.76 * ar
        d = 0
        e = 0

    elif phi_value < 1:
        ar = x + y/4
        g = ar * (1/phi_value)
        a = x
        b = y/2
        c = 3.76 * ar * (1/phi_value)
        d = ar * ((1/phi_value)-1)
        e = 0

    elif phi_value > 1:
        ar = x + y/4
        g = ar * (1/phi_value)
        a = (2*ar/phi_value) - x - y/2
        b = y/2
        c = 3.76 * ar * (1/phi_value)
        d = 0
        e = 2*x + y/2 - (2*ar)/phi_value
        
    T_guess = 2100
    tol = 1e-6
    alpha = 0.2
    max_iter = 1000  # Maximum number of iterations
    ct = 0
    
    val1 = f(T_guess, phi_value, a, b, c, d, e)
    while abs(val1) > tol and ct < max_iter:
        val1 = f(T_guess, phi_value, a, b, c, d, e)
        T_guess -= alpha * (f(T_guess, phi_value, a, b, c, d, e) / fprime(T_guess, phi_value, a, b, c, d, e))
        ct += 1

    val_n_tot = n_tot(phi_value, a, b)
    
    X_co2.append(a/ val_n_tot)
    X_co.append(0)
    X_h2o.append((b/2)/ val_n_tot)
    X_h2.append(0)
    X_o2.append((((1 - phi_value)/ phi_value)*(a + b/4))/val_n_tot)
    X_n2.append((3.76* (a + b/4))*(phi_value * val_n_tot))
    T_py.append(T_guess)

# Plotting
# plt.plot(phi_values, n_tots)
# plt.xlabel('Equivalence Ratio (phi)')
# plt.ylabel('No. of moles Total')
# plt.title('N_Total vs Scpies')
# plt.grid(True)
# plt.show()


plt.figure(figsize=(10, 8))
plt.plot(phi_values, X_co2, label='CO2')
plt.plot(phi_values, X_co, label='CO')
plt.plot(phi_values, X_h2o, label='H2O')
plt.plot(phi_values, X_o2, label='O2')
plt.plot(phi_values, X_n2, label='N2')
plt.xlabel('Equivalence Ratio (phi)')
plt.ylabel('Mole Fraction')
plt.title('Species Mole Fractions vs. Equivalence Ratio')
plt.legend()
plt.grid(True)
plt.show()