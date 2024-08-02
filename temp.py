import matplotlib.pyplot as plt
import numpy as np

# Constants
R = 8.314  # J/(mol·K)

# Initial conditions
P_total = 101325  # Total pressure in Pa (1 atm)

# Reaction: CH4 + 2 O2 -> CO2 + 2 H2O
# Stoichiometric coefficients
nu_CH4 = -1
nu_O2 = -2
nu_CO2 = 1
nu_H2O = 2

# Initial moles assuming excess air and varying equivalence ratio
phi = 1.5  # Equivalence ratio
moles_CH4_initial = 1  # Arbitrary choice, 1 mole of CH4
moles_O2_initial = 2 * phi * moles_CH4_initial  # Based on stoichiometry and excess
moles_N2_initial = 3.76 * moles_O2_initial  # Air is about 79% N2 and 21% O2

# Temperature range
temperature_range = np.linspace(800, 3000, 100)  # From 800 K to 3000 K

# Prepare lists to store results for plotting
temperatures = []
p_CO2_list = []
p_H2O_list = []
p_CH4_list = []
p_O2_list = []

def reaction_extent(T, Kp):
    # Use the stoichiometric coefficients and initial amounts to calculate the equilibrium state
    xi = 0.5 * moles_CH4_initial  # Assume half of the CH4 reacts initially
    xi_min = 0
    xi_max = moles_CH4_initial

    # Iterative approach to find xi that satisfies the equilibrium condition
    for _ in range(100):
        n_CH4 = moles_CH4_initial + nu_CH4 * xi
        n_O2 = moles_O2_initial + nu_O2 * xi
        n_CO2 = 0 + nu_CO2 * xi
        n_H2O = 0 + nu_H2O * xi
        n_total = n_CH4 + n_O2 + n_CO2 + n_H2O + moles_N2_initial

        # Calculate partial pressures
        p_CH4 = (n_CH4 / n_total) * P_total
        p_O2 = (n_O2 / n_total) * P_total
        p_CO2 = (n_CO2 / n_total) * P_total
        p_H2O = (n_H2O / n_total) * P_total

        Kp_calc = (p_CO2 * p_H2O**2) / (p_CH4 * p_O2**2)
        
        # Adjust xi to satisfy Kp
        if Kp_calc < Kp:
            xi_min = xi
            xi = (xi + xi_max) / 2
        else:
            xi_max = xi
            xi = (xi + xi_min) / 2

    return p_CH4, p_O2, p_CO2, p_H2O

# Calculate Gibbs free energy changes for each temperature and the corresponding Kp
for T in temperature_range:
    delta_H_CH4 = -74.85e3  # ΔH in J/mol for CH4 combustion, example value
    delta_S_CH4 = -0.224  # ΔS in J/(mol·K) for CH4 combustion, example value
    delta_G = delta_H_CH4 - T * delta_S_CH4
    Kp = np.exp(-delta_G / (R * T))

    p_CH4, p_O2, p_CO2, p_H2O = reaction_extent(T, Kp)
    
    # Store results
    temperatures.append(T)
    p_CH4_list.append(p_CH4 / 101325)  # Convert Pa to atm
    p_O2_list.append(p_O2 / 101325)
    p_CO2_list.append(p_CO2 / 101325)
    p_H2O_list.append(p_H2O / 101325)

# Plotting the results
plt.figure(figsize=(10, 8))
plt.plot(temperatures, p_CO2_list, label='CO2')
plt.plot(temperatures, p_H2O_list, label='H2O')
plt.plot(temperatures, p_CH4_list, label='CH4')
plt.plot(temperatures, p_O2_list, label='O2')
plt.xlabel('Temperature (K)')
plt.ylabel('Partial Pressure (atm)')
plt.title('Equilibrium Partial Pressures vs. Temperature')
plt.legend()
plt.grid(True)
plt.show()
