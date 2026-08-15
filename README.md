# 5-Layer Stratified Water Storage Tank Model

This repository contains a Python model for simulating the transient temperature distribution in a **150 m³ stratified water storage tank**.

The tank is represented by **five vertically stratified, equal-volume nodes**. Water enters the tank at the top at 12 °C and leaves from the bottom at a mass flow rate of 20 kg/s.

## 1. Physical Configuration

The tank is represented as five layers:

```text
                    12 °C water inlet
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
                     20 kg/s outlet
```

Initially, all five layers are at **6 °C**.

## 2. Model Parameters

| Parameter | Value | Unit |
|---|---:|---|
| Total tank volume | 150 | m³ |
| Number of layers | 5 | - |
| Volume per layer | 30 | m³ |
| Initial tank temperature | 6 | °C |
| Inlet water temperature | 12 | °C |
| Mass flow rate | 20 | kg/s |
| Water density | 1000 | kg/m³ |
| Specific heat capacity | 4180 | J/kg·K |
| Time step | 120 | s |
| Simulation duration | 6 | h |

Each layer therefore contains approximately:

\[
m_{layer} = 
ho V_{layer}
= 1000 	imes 30
= 30,000\;kg
\]

## 3. Energy Balance

The model uses a nodal energy balance.

For the top node:

\[
m_1c_prac{dT_1}{dt}
=
\dot m c_p(T_{in}-T_1)
\]

For the remaining nodes:

\[
m_ic_prac{dT_i}{dt}
=
\dot m c_p(T_{i-1}-T_i)
\]

where:

- \(m_i\) = water mass in node \(i\)
- \(c_p\) = specific heat capacity of water
- \(\dot m\) = mass flow rate
- \(T_i\) = temperature of node \(i\)
- \(T_{in}\) = inlet temperature

The outlet temperature is the temperature of **Node 5**, the bottom node.

## 4. Assumptions

The current model assumes:

1. The tank has five equal-volume nodes.
2. Each node is perfectly mixed within itself.
3. Water flows sequentially from Node 1 to Node 5.
4. Water enters Node 1 at 12 °C.
5. Water exits from Node 5 at 20 kg/s.
6. The inlet and outlet mass flow rates are equal, so tank volume remains constant.
7. Water density and specific heat are constant.
8. There is no heat loss from the tank to the surroundings.
9. There is no direct mixing between non-adjacent nodes.
10. The current implementation does not include explicit conduction between nodes or temperature-inversion mixing.

The underlying stratified-tank reference formulation includes additional effects such as inter-node flow, conduction, and temperature-inversion mixing. These can be added in future versions if required.

## 5. Numerical Method

The model advances the temperature of each node at every time step.

For example, Node 2 is updated using:

\[
T_2^{n+1}
=
T_2^n+
rac{\dot m}{m_2}
(T_1^n-T_2^n)\Delta t
\]

Similarly, each downstream node uses the temperature of the node immediately above it.

The implementation uses a fixed time step of **120 seconds**.

## 6. Python Code

The main script should contain the 5-layer stratified tank model.

A typical project structure is:

```text
5-layer-stratified-tank/
│
├── tank_5_layer.py
├── README.md
└── requirements.txt
```

## 7. Requirements

The model requires:

- Python 3
- NumPy
- Matplotlib

Install the required packages with:

```bash
pip install numpy matplotlib
```

Or, if a `requirements.txt` file is included:

```bash
pip install -r requirements.txt
```

## 8. Running the Model

Run the Python script from a terminal:

```bash
python tank_5_layer.py
```

The script prints the temperature of each layer during the simulation and generates plots showing:

1. Temperature of each layer versus time.
2. Final temperature profile through the tank.

## 9. Interpretation of the Results

The expected physical behaviour is:

- Node 1 (top) responds first because it receives the 12 °C inlet water.
- Node 2 responds after Node 1 begins warming.
- Nodes 3–5 respond progressively later.
- The bottom node (Node 5) represents the outlet temperature.
- The stratification causes the upper part of the tank to warm before the lower part.
- The tank approaches the inlet temperature over time if the system continues operating without heat loss.

This behaviour is different from a perfectly mixed tank, where the entire tank would have one uniform temperature at every instant.

## 10. Relation to the Stratified Tank Reference

The model is based on the nodal energy-balance concept used for stratified storage tanks. In a more detailed implementation, the model can be extended to include:

- Conduction between adjacent nodes
- Temperature-inversion mixing
- Variable flow rates
- Variable inlet temperature
- Tank heat losses
- More than five nodes
- Charging and discharging modes
- Adaptive time stepping
- Analytical nodal solutions

These additions should be implemented only when the corresponding physical behaviour is required by the application.

## 11. Intended Application

The model is intended as a simple, transparent representation of a stratified thermal storage tank. It can be used to study how an initially cold tank responds when warmer water is introduced at the top while water is simultaneously discharged from the bottom.

For the current case:

**Tank volume:** 150 m³  
**Initial temperature:** 6 °C  
**Inlet temperature:** 12 °C  


## Example Hand Calculation — First 2 Minutes

Consider a 150 m³ water storage tank divided into 10 equal-volume layers.

### 1. Tank and Layer Properties

Total tank volume:

\[
V_{tank}=150\;m^3
\]

Number of layers:

\[
N=10
\]

Therefore, the volume of each layer is:

\[
V_{layer}=\frac{V_{tank}}{N}
=\frac{150}{10}
=15\;m^3
\]

Assuming a water density of:

\[
\rho=1000\;kg/m^3
\]

the mass of water in each layer is:

\[
m_{layer}=\rho V_{layer}
\]

\[
m_{layer}=1000\times15
\]

\[
\boxed{m_{layer}=15,000\;kg}
\]

Therefore, each of the 10 layers contains approximately **15,000 kg of water**.

---

### 2. Initial Conditions

Initially, the entire tank is at:

\[
T_{initial}=6^\circ C
\]

Therefore, for the first layer:

\[
T_1^0=6^\circ C
\]

Water enters the tank from the top at:

\[
T_{in}=12^\circ C
\]

The mass flow rate is:

\[
\dot{m}=20\;kg/s
\]

We want to calculate the temperature after:

\[
\Delta t=2\;minutes=120\;s
\]

---

### 3. Water Entering During the 2-Minute Time Step

The mass of water entering during the 120-second time step is:

\[
m_{in}=\dot{m}\Delta t
\]

\[
m_{in}=20\times120
\]

\[
\boxed{m_{in}=2,400\;kg}
\]

Because the tank has a constant volume, the same 2,400 kg of water leaves Layer 1 and moves into Layer 2 during this time step.

Therefore, the mass of Layer 1 remains:

\[
m_1=15,000\;kg
\]

---

### 4. Energy Balance for Layer 1

Layer 1 receives 12 °C water and sends water to Layer 2.

The energy balance is:

\[
m_1c_p\frac{dT_1}{dt}
=
\dot{m}c_p(T_{in}-T_1)
\]

Since the specific heat \(c_p\) appears on both sides, it cancels:

\[
m_1\frac{dT_1}{dt}
=
\dot{m}(T_{in}-T_1)
\]

For a time-step calculation:

\[
T_1^{n+1}
=
T_1^n+
\frac{\dot{m}\Delta t}{m_1}
(T_{in}-T_1^n)
\]

---

### 5. Calculate Temperature of Layer 1 After 2 Minutes

Known values:

\[
T_1^n=6^\circ C
\]

\[
T_{in}=12^\circ C
\]

\[
\dot{m}=20\;kg/s
\]

\[
\Delta t=120\;s
\]

\[
m_1=15,000\;kg
\]

Substituting:

\[
T_1^{n+1}
=
6+
\frac{20\times120}{15,000}(12-6)
\]

First calculate the mass-flow fraction:

\[
\frac{20\times120}{15,000}
=
\frac{2,400}{15,000}
=
0.16
\]

Therefore:

\[
T_1^{n+1}
=
6+0.16(12-6)
\]

\[
T_1^{n+1}
=
6+0.16(6)
\]

\[
T_1^{n+1}=6+0.96
\]

Therefore:

\[
\boxed{T_1^{2min}=6.96^\circ C}
\]

So, after two minutes, the temperature of the top layer increases from **6.00 °C to approximately 6.96 °C**.

---

### 6. Calculation for Layer 2

Initially:

\[
T_2^0=6^\circ C
\]

Layer 2 receives water from Layer 1. At the end of the first time step:

\[
T_1=6.96^\circ C
\]

The energy balance for Layer 2 is:

\[
m_2c_p\frac{dT_2}{dt}
=
\dot{m}c_p(T_1-T_2)
\]

Therefore:

\[
T_2^{n+1}
=
T_2^n+
\frac{\dot{m}\Delta t}{m_2}
(T_1^n-T_2^n)
\]

Substituting:

\[
T_2^{n+1}
=
6+
\frac{20\times120}{15,000}(6.96-6)
\]

\[
=
6+0.16(0.96)
\]

\[
=
6+0.1536
\]

Therefore:

\[
\boxed{T_2^{2min}=6.154^\circ C}
\]

---

### 7. Temperature Distribution After 2 Minutes

Using the same approach for all 10 layers gives the temperature distribution after each time step.

After the first 2-minute time step:

| Layer | Initial Temperature (°C) | Temperature after 2 min (°C) |
|---|---:|---:|
| 1 — Top | 6.000 | 6.960 |
| 2 | 6.000 | 6.154 |
| 3 | 6.000 | 6.025 |
| 4 | 6.000 | 6.004 |
| 5 | 6.000 | 6.001 |
| 6 | 6.000 | 6.000 |
| 7 | 6.000 | 6.000 |
| 8 | 6.000 | 6.000 |
| 9 | 6.000 | 6.000 |
| 10 — Bottom | 6.000 | 6.000 |

The warmer water therefore propagates gradually downward through the tank.

---

## 8. General Equation Used by the Model

For the **top layer**:

\[
\boxed{
T_1^{n+1}
=
T_1^n+
\frac{\dot{m}\Delta t}{m_1}
(T_{in}-T_1^n)
}
\]

For all other layers:

\[
\boxed{
T_i^{n+1}
=
T_i^n+
\frac{\dot{m}\Delta t}{m_i}
(T_{i-1}^n-T_i^n)
}
\]

where:

- \(T_i^n\) = temperature of layer \(i\) at the previous time step
- \(T_i^{n+1}\) = temperature of layer \(i\) at the new time step
- \(\dot{m}\) = mass flow rate [kg/s]
- \(\Delta t\) = time step [s]
- \(m_i\) = water mass in layer \(i\) [kg]
- \(T_{in}\) = inlet water temperature [°C]

For the bottom layer (Layer 10), the calculated temperature is also the **tank outlet temperature**.

---

## 9. Important Note

This hand calculation represents a simplified stratified-tank model in which each layer is assumed to be perfectly mixed within itself and water flows sequentially from the top layer to the bottom layer.

The model does not currently include:

- Heat loss through the tank wall
- Thermal conduction between adjacent layers
- Temperature-inversion mixing
- Inlet diffuser effects
- Non-uniform layer volumes
- Variable water properties

These effects can be added later if a more detailed representation of the actual TES tank is required.

The model can subsequently be expanded to represent the actual operating conditions of a thermal energy storage (TES) system more closely.
