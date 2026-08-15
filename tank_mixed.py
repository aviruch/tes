"""
Transient Temperature of a Water Storage Tank
-----------------------------------------------

This model calculates the temperature of water in a perfectly mixed
150 m³ storage tank.

Physical system
---------------
- Tank volume: 150 m³
- Initial tank temperature: 6 °C
- Water enters the tank from the top at 12 °C
- Water leaves the tank from the bottom
- Inlet and outlet mass flow rates are equal
- Mass flow rate: 20 kg/s
- Tank is assumed to be perfectly mixed

Energy balance
--------------
rho * V * cp * dT/dt = m_dot * cp * (T_in - T)

where:

rho   = water density [kg/m³]
V     = tank volume [m³]
cp    = specific heat capacity [J/kg-K]
m_dot = mass flow rate [kg/s]
T_in  = inlet water temperature [°C]
T     = tank temperature [°C]

Assumptions
-----------
- No heat loss to surroundings
- Constant water properties
- Constant tank volume
- Perfect mixing
- No thermal stratification
"""

import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 1. TANK PARAMETERS
# =============================================================================

tank_volume = 150.0             # Tank volume [m³]

water_density = 1000.0          # Water density [kg/m³]

specific_heat = 4180.0           # Specific heat of water [J/kg-K]

mass_flow_rate = 20.0           # Water mass flow rate [kg/s]


# =============================================================================
# 2. TEMPERATURE CONDITIONS
# =============================================================================

initial_temperature = 6.0        # Initial tank temperature [°C]

inlet_temperature = 12.0         # Inlet water temperature [°C]


# =============================================================================
# 3. TIME SETTINGS
# =============================================================================

time_step = 120.0                # Time step [s]

number_of_time_steps = 100       # Number of time steps


# =============================================================================
# 4. TANK MASS AND CHARACTERISTIC TIME
# =============================================================================

# Total mass of water in the tank
tank_mass = water_density * tank_volume

# Characteristic mixing time:
#
# tau = tank_mass / mass_flow_rate
#
# This represents approximately the time required to replace
# one tank volume of water.

mixing_time = tank_mass / mass_flow_rate

print("Tank mass =", tank_mass, "kg")
print("Characteristic mixing time =", mixing_time, "s")
print(
    "Characteristic mixing time =",
    mixing_time / 3600,
    "hours"
)


# =============================================================================
# 5. INITIAL CONDITION
# =============================================================================

tank_temperature = initial_temperature

temperature_history = []


# =============================================================================
# 6. TIME-STEPPING CALCULATION
# =============================================================================

for step in range(1, number_of_time_steps + 1):

    # Current simulation time
    current_time = step * time_step

    # -------------------------------------------------------------------------
    # Energy balance:
    #
    # Energy entering:
    #     m_dot * cp * T_in
    #
    # Energy leaving:
    #     m_dot * cp * T_tank
    #
    # Therefore:
    #
    # dT/dt = m_dot / (rho * V) * (T_in - T_tank)
    # -------------------------------------------------------------------------

    temperature_change = (
        mass_flow_rate
        / tank_mass
        * (inlet_temperature - tank_temperature)
        * time_step
    )

    # Update tank temperature
    tank_temperature = tank_temperature + temperature_change

    # Store results
    temperature_history.append(
        {
            "time": current_time,
            "temperature": tank_temperature
        }
    )

    # Print result
    print(
        f"Time = {current_time / 60:.1f} min, "
        f"Tank temperature = {tank_temperature:.3f} °C"
    )


# =============================================================================
# 7. EXTRACT RESULTS FOR PLOTTING
# =============================================================================

time_hours = np.array(
    [result["time"] for result in temperature_history]
) / 3600

tank_temperatures = np.array(
    [result["temperature"] for result in temperature_history]
)


# =============================================================================
# 8. PLOT TANK TEMPERATURE
# =============================================================================

plt.figure(figsize=(7, 5))

plt.plot(
    time_hours,
    tank_temperatures,
    marker="o",
    markersize=3
)

plt.xlabel("Time [hours]")
plt.ylabel("Tank temperature [°C]")

plt.title("Transient Temperature of Water Storage Tank")

plt.grid(True)

plt.tight_layout()
plt.show()
