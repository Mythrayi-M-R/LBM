# Numerical Methods for Heat Transfer and Fluid Flow

This repository documents three problems solved using different numerical methods — **Finite Difference Method (FDM)** and **Lattice Boltzmann Method (LBM)**, including the **Two-Relaxation-Time (TRT)** collision operator for improved stability.

---

## Problem 1 — Heat Conduction in a Square Plate

### Finite Difference Method (FDM)
- Solves the 2D steady-state heat transfer equation.
- Assumes uniform grid spacing in both directions.
- The temperature at a grid point is computed as the average of its four immediate neighbours.
- Iterative updates are performed until convergence.

### Lattice Boltzmann Method (LBM)
- A mesoscopic numerical method based on kinetic theory.
- Uses the **Boltzmann equation** with the **BGK approximation** for the collision term.
- The discrete velocity model **D2Q9** is used for 2D problems.
- Collision and streaming steps are applied iteratively until steady state is reached.
- Relaxation time `τ` is related to diffusion constant; stability requires `τ > 0.5`.

---

## Problem 2 — Unsteady Advection–Diffusion Equation

### FDM Approach
- Advection terms discretised using **upwind scheme**:
  - Backward difference for positive flow.
  - Forward difference for negative flow.
- Diffusion terms discretised using **central difference**.
- Numerical stability ensured via:
  1. **CFL number**
  2. **Fourier number**
- Small time step used to satisfy stability conditions.

### LBM with D2Q5 Model
- In pure diffusion, equilibrium function is isotropic.
- With advection, directional bias is introduced.
- LBM captures both advection and diffusion within a single equation.
- Relaxation time determined from diffusion coefficient.

### Using the TRT Collision Operator
- BGK uses a single relaxation time `τ` for both physical diffusion and stability, which can lead to instability in anisotropic lattices.
- TRT splits the distribution function into:
  - **Even part** (controls bulk diffusion).
  - **Odd part** (controls numerical dissipation).
- Two separate relaxation rates:
  - `ω+` from diffusion coefficient/viscosity.
  - `ω−` from stability condition using magic number `Λ ≈ 0.25`.
- Improves stability over BGK and allows faster convergence.

---

## Problem 3 — Thermal and Velocity Boundary Layers

- Two coupled equations solved in the same lattice:
  1. **X-Momentum Equation** → velocity field.
  2. **Advection–Diffusion Equation** → temperature field.
- Taylor series expansion of the LBM equation used to derive equilibrium distributions (`feq` for momentum, `geq` for temperature).
- Different relaxation times used for velocity (`τu` from viscosity) and temperature (`τT` from thermal diffusivity).
- TRT operator applied to both velocity and temperature fields for enhanced stability.
- Boundary conditions:
  - Inlet: **Zou/He velocity boundary condition**.
  - Bottom wall: **no-slip**, constant temperature.
  - Top wall: **free-slip**, adiabatic.
  - Outlet: **zero-gradient**.
- Simulations performed for different **Prandtl numbers** (0.5, 1, 2) to study boundary layer behaviour.

---

## Key Insights
- FDM provides a straightforward macroscopic solution but requires careful stability checks for unsteady problems.
- LBM offers a unified framework for modelling advection–diffusion and flow problems at the mesoscopic scale.
- TRT significantly enhances numerical stability compared to BGK, especially in anisotropic or advective cases.
- Coupled LBM simulations can handle thermal–fluid interactions efficiently within the same lattice framework.

---

## References
- Succi, S. *The Lattice Boltzmann Equation for Fluid Dynamics and Beyond.*
- He, X., Luo, L.-S. *Theory of the Lattice Boltzmann Method.*
