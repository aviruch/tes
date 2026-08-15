"""
5-Layer Stratified Water Storage Tank
=====================================

This model represents a 150 m³ water storage tank using five
equal-volume stratified nodes.

Tank configuration
------------------

                12 °C water IN
                       ↓
              ┌─────────────────┐
              │     Node 1      │  Top
              │     30 m³       │
              ├─────────────────┤
              │     Node 2      │
              │     30 m³       │
              ├─────────────────┤
              │     Node 3      │
              │     30 m³       │
              ├─────────────────┤
              │     Node 4      │
              │     30 m³       │
              ├─────────────────┤
              │     Node 5      │  Bottom
              │     30 m³       │
              └─────────────────┘
                       ↓
                  20 kg/s OUT

The formulation follows the stratified tank energy-balance approach
described in the Engineering Reference.

Main assumptions
----------------
1. Five equal-volume nodes.
2. Each node is perfectly mixed within itself.
3. Water flows from Node 1 -> Node 2 -> ... -> Node 5.
4. Water enters Node 1 at 12 °C.
5. Water leaves Node 5 at 20 kg/s.
6. No heat loss to the surroundings.
7. Constant water density and specific heat.
8. No temperature-inversion mixing is included initially.
9. Conduction between nodes can optionally be included.
"""

import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 1. TANK PARAMETERS
# =============================================================================

tank_volume = 150.0              # Total tank volume [m³]

number_of_nodes = 5              # Number of stratified nodes

water_density = 1000.0           # Water density [kg/m³]

specific_heat = 4180.0            # Water specific heat [J/kg-K]

mass_flow_rate = 20.0             # Mass flow rate [kg/s]


# =============================================================================
# 2. TEMPERATURE CONDITIONS
# =============================================================================

initial_temperature = 6.0         # Initial temperature of all nodes [°C]

inlet_temperature = 12.0          # Inlet water temperature [°C]


# =============================================================================
# 3. TIME SETTINGS
# =============================================================================

time_step = 120.0                 # Simulation time step [s]

simulation_time = 6 * 3600        # Total simulation time [s]

number_of_time_steps = int(
    simulation_time / time_step
)


# =============================================================================
# 4. CALCULATE NODE PROPERTIES
# =============================================================================

# All nodes have equal volume.

node_volume = tank_volume / number_of_nodes

# Mass of water contained in each node.

node_mass = water_density * node_volume


print("==============================================")
print("5-Layer Stratified Tank Model")
print("==============================================")

print(f"Tank volume       : {tank_volume:.1f} m³")
print(f"Number of nodes   : {number_of_nodes}")
print(f"Node volume       : {node_volume:.1f} m³")
print(f"Node mass         : {node_mass:.1f} kg")
print(f"Mass flow rate    : {mass_flow_rate:.1f} kg/s")
print(f"Inlet temperature : {inlet_temperature:.1f} °C")
print(f"Initial temperature: {initial_temperature:.1f} °C")
print(f"Time step         : {time_step:.1f} s")

print("==============================================")


# =============================================================================
# 5. INITIAL NODE TEMPERATURES
# =============================================================================

# Node numbering:
#
# Node 1 = Top
# Node 5 = Bottom
#
# Initially the entire tank is at 6 °C.

temperatures = np.full(
    number_of_nodes,
    initial_temperature,
    dtype=float
)


# =============================================================================
# 6. STORAGE FOR RESULTS
# =============================================================================

time_history = []

temperature_history = []

outlet_temperature_history = []


# Store initial condition

time_history.append(0.0)

temperature_history.append(
    temperatures.copy()
)

# Initially, the outlet temperature is the temperature
# of the bottom node.

outlet_temperature_history.append(
    temperatures[-1]
)


# =============================================================================
# 7. TIME-STEPPING SOLUTION
# =============================================================================

for step in range(1, number_of_time_steps + 1):

    # Create a copy so that all new temperatures are calculated
    # using temperatures from the PREVIOUS time step.

    new_temperatures = temperatures.copy()


    # -------------------------------------------------------------------------
    # NODE 1 — TOP NODE
    #
    # Node 1 receives 12 °C water from outside the tank.
    #
    # Energy balance:
    #
    # m cp dT1/dt =
    #       m_dot cp (T_in - T1)
    #
    # -------------------------------------------------------------------------

    new_temperatures[0] = (
        temperatures[0]
        +
        (
            mass_flow_rate
            / node_mass
        )
        *
        (
            inlet_temperature
            - temperatures[0]
        )
        *
        time_step
    )


    # -------------------------------------------------------------------------
    # NODES 2 TO 5
    #
    # Each node receives water from the node immediately above it.
    #
    # For example:
    #
    # Node 2:
    #     m cp dT2/dt =
    #     m_dot cp (T1 - T2)
    #
    # Node 3:
    #     m cp dT3/dt =
    #     m_dot cp (T2 - T3)
    #
    # etc.
    #
    # This represents the internode flow described in the
    # Engineering Reference.
    # -------------------------------------------------------------------------

    for node in range(1, number_of_nodes):

        new_temperatures[node] = (
            temperatures[node]
            +
            (
                mass_flow_rate
                / node_mass
            )
            *
            (
                temperatures[node - 1]
                - temperatures[node]
            )
            *
            time_step
        )


    # -------------------------------------------------------------------------
    # UPDATE TEMPERATURES
    # -------------------------------------------------------------------------

    temperatures = new_temperatures


    # Current simulation time

    current_time = step * time_step


    # -------------------------------------------------------------------------
    # STORE RESULTS
    # -------------------------------------------------------------------------

    time_history.append(current_time)

    temperature_history.append(
        temperatures.copy()
    )

    # Bottom node is the tank outlet temperature

    outlet_temperature_history.append(
        temperatures[-1]
    )


# Convert lists to NumPy arrays

time_history = np.array(time_history)

temperature_history = np.array(
    temperature_history
)

outlet_temperature_history = np.array(
    outlet_temperature_history
)


# =============================================================================
# 8. PRINT FINAL RESULTS
# =============================================================================

print("\n==============================================")
print("Final Temperature Distribution")
print("==============================================")

for node in range(number_of_nodes):

    print(
        f"Node {node + 1}: "
        f"{temperatures[node]:.3f} °C"
    )

print(
    f"\nOutlet temperature: "
    f"{outlet_temperature_history[-1]:.3f} °C"
)


# =============================================================================
# 9. PLOT TEMPERATURE OF EACH NODE
# =============================================================================

plt.figure(figsize=(8, 5))

for node in range(number_of_nodes):

    plt.plot(
        time_history / 3600,
        temperature_history[:, node],
        label=f"Node {node + 1}"
    )

plt.xlabel("Time [hours]")

plt.ylabel("Temperature [°C]")

plt.title(
    "Temperature Evolution of 5-Layer Stratified Tank"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()


# =============================================================================
# 10. PLOT FINAL TEMPERATURE PROFILE
# =============================================================================

node_numbers = np.arange(
    1,
    number_of_nodes + 1
)

plt.figure(figsize=(6, 5))

plt.plot(
    temperatures,
    node_numbers,
    marker="o"
)

plt.xlabel("Temperature [°C]")

plt.ylabel(
    "Node Number "
    "(1 = Top, 5 = Bottom)"
)

plt.title(
    "Final Temperature Profile Through Tank"
)

plt.grid(True)

plt.tight_layout()

plt.show()
