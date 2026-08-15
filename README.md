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


## Example Calculation — First 120 Sec

Consider a 150 m³ water storage tank divided into 10 equal-volume layers.

### 1. Tank and Layer Properties

The total tank volume is:

$$
V_{tank}=150\;m^3
$$

The tank is divided into 10 layers:

$$
N=10
$$

Therefore, the volume of each layer is:

$$
V_{layer}
=
\frac{V_{tank}}{N}
=
\frac{150}{10}
=
15\;m^3
$$

Assuming a water density of:

$$
\rho=1000\;kg/m^3
$$

the mass of water in each layer is:

$$
m_{layer}
=
\rho V_{layer}
$$

$$
m_{layer}
=
1000\times15
=
15,000\;kg
$$

Therefore, each layer contains approximately **15,000 kg of water**.

---

### 2. Initial and Boundary Conditions

Initially, the entire tank is at:

$$
T_{initial}=6^\circ C
$$

Therefore, the initial temperature of the top layer is:

$$
T_1^0=6^\circ C
$$

Water enters the tank from the top at:

$$
T_{in}=12^\circ C
$$

The mass flow rate is:

$$
\dot{m}=20\;kg/s
$$

We calculate the temperature after 2 minutes:

$$
\Delta t=2\times60=120\;s
$$

---

### 3. Water Flow During the 2-Minute Time Step

The mass of water entering during the time step is:

$$
m_{in}=\dot{m}\Delta t
$$

Using:

$$
\begin{aligned}
m_{in}
&=
20\times120 \\
&=
2,400\;kg
\end{aligned}
$$

Therefore:

$$
\boxed{m_{in}=2,400\;kg}
$$

Because the tank has a constant volume, the same mass of water moves out of Layer 1 into Layer 2.

Therefore, the mass of Layer 1 remains:

$$
m_1=15,000\;kg
$$

---

### 4. Energy Balance for Layer 1

The top layer receives water at $T_{in}$ and transfers the same mass flow rate to Layer 2.

The energy balance is:

$$
m_1c_p\frac{dT_1}{dt}
=
\dot{m}c_p(T_{in}-T_1)
$$

Since $c_p$ appears on both sides, it cancels:

$$
m_1\frac{dT_1}{dt}
=
\dot{m}(T_{in}-T_1)
$$

Therefore:

$$
\frac{dT_1}{dt}
=
\frac{\dot{m}}{m_1}
(T_{in}-T_1)
$$

---

### 5. Discrete Time-Step Equation

Using a time step $\Delta t$, the temperature of Layer 1 at the next time step is:

$$
T_1^{n+1}
=
T_1^n+
\frac{\dot{m}\Delta t}{m_1}
\left(T_{in}-T_1^n\right)
$$

For the first time step:

$$
T_1^n=6^\circ C
$$

$$
T_{in}=12^\circ C
$$

$$
\dot{m}=20\;kg/s
$$

$$
\Delta t=120\;s
$$

$$
m_1=15,000\;kg
$$

Substituting these values:

$$
\begin{aligned}
T_1^{n+1}
&=
6+
\frac{20\times120}{15,000}(12-6) \\[6pt]
&=
6+
\frac{2,400}{15,000}(6) \\[6pt]
&=
6+0.16(6) \\[6pt]
&=
6+0.96 \\[6pt]
&=
\boxed{6.96^\circ C}
\end{aligned}
$$

Therefore, the temperature of the top layer after **2 minutes is 6.96 °C**.

---

### 6. Energy Balance for Layer 2

Layer 2 receives water from Layer 1.

The energy balance is:

$$
m_2c_p\frac{dT_2}{dt}
=
\dot{m}c_p(T_1-T_2)
$$

Again, $c_p$ cancels:

$$
\frac{dT_2}{dt}
=
\frac{\dot{m}}{m_2}
(T_1-T_2)
$$

The discrete equation is:

$$
T_2^{n+1}
=
T_2^n+
\frac{\dot{m}\Delta t}{m_2}
\left(T_1^n-T_2^n\right)
$$

Initially:

$$
T_2^n=6^\circ C
$$

and:

$$
T_1^n=6^\circ C
$$

Therefore, during the **first 2-minute time step**:

$$
\begin{aligned}
T_2^{n+1}
&=
6+
\frac{20\times120}{15,000}(6-6) \\[6pt]
&=
6+0 \\[6pt]
&=
\boxed{6.00^\circ C}
\end{aligned}
$$

This is an important point: in an explicit time-stepping scheme, **Layer 2 uses the Layer 1 temperature from the beginning of the time step**, not the newly calculated 6.96 °C.

Therefore, after the first 2-minute time step:

| Layer | Temperature |
|---|---:|
| Layer 1 — Top | 6.960 °C |
| Layer 2 | 6.000 °C |
| Layer 3 | 6.000 °C |
| Layer 4 | 6.000 °C |
| Layer 5 | 6.000 °C |
| Layer 6 | 6.000 °C |
| Layer 7 | 6.000 °C |
| Layer 8 | 6.000 °C |
| Layer 9 | 6.000 °C |
| Layer 10 — Bottom | 6.000 °C |

---

### 7. General Equation for the 10-Layer Model

For the top layer:

$$
\boxed{
T_1^{n+1}
=
T_1^n+
\frac{\dot{m}\Delta t}{m_1}
\left(T_{in}-T_1^n\right)
}
$$

For all other layers:

$$
\boxed{
T_i^{n+1}
=
T_i^n+
\frac{\dot{m}\Delta t}{m_i}
\left(T_{i-1}^n-T_i^n\right)
}
$$

where:

- $T_i^n$ = temperature of layer $i$ at the previous time step
- $T_i^{n+1}$ = temperature of layer $i$ at the new time step
- $\dot{m}$ = water mass flow rate [kg/s]
- $\Delta t$ = time step [s]
- $m_i$ = mass of water in layer $i$ [kg]
- $T_{in}$ = inlet water temperature [°C]

For the bottom layer:

$$
T_{out}=T_{10}
$$

Therefore, the temperature of Layer 10 represents the **tank outlet temperature**.

---

### 8. Important Numerical Point

The calculation above uses an **explicit time-stepping approach**.

At each time step:

1. Temperatures from the previous time step are used.
2. The new temperature of Layer 1 is calculated.
3. The new temperature of Layer 2 is calculated using the **old** temperature of Layer 1.
4. The same procedure is repeated down to Layer 10.
5. All calculated temperatures become the starting temperatures for the next time step.

This can be represented as:

$$
\left[
T_1^n,T_2^n,\ldots,T_{10}^n
\right]
\longrightarrow
\left[
T_1^{n+1},T_2^{n+1},\ldots,T_{10}^{n+1}
\right]
$$

The process is then repeated for every time step until the desired simulation period is reached.

The model can subsequently be expanded to represent the actual operating conditions of a thermal energy storage (TES) system more closely.
