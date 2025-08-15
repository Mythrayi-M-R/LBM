# Deriving Navier–Stokes from Lattice Boltzmann

## Boltzmann Equation with External Force

$$
\frac{\partial f}{\partial t} + \mathbf{v} \cdot \nabla f + \mathbf{F} \cdot \nabla_{\mathbf{v}} f = \left( \frac{\partial f}{\partial t} \right)_{\text{coll}}
$$

This equation describes how the probability distribution function $f$ (higher probability → higher number of particles → higher density) changes with time.

---

## Macroscopic Variables

From $f$ we obtain:

**Density**

$$
\rho = \int f \, d\mathbf{v}
$$

**Momentum**

$$
\rho \mathbf{u} = \int \mathbf{v} f \, d\mathbf{v}
$$

**Energy**

$$
\rho e = \int \frac{1}{2} |\mathbf{v}|^2 f \, d\mathbf{v}
$$

---

## Chapman–Enskog Expansion

We assume the gas is near equilibrium:

$$
f = f^{(0)} + \epsilon f^{(1)} + \epsilon^2 f^{(2)} + \dots
$$

Here, $\epsilon$ is the mean free path / characteristic length.

Similarly:

$$
\partial_t = \epsilon \partial_t^{(1)} + \epsilon^2 \partial_t^{(2)} + \dots
$$

$$
\nabla = \epsilon \nabla^{(1)} + \dots
$$

---

## BGK Approximation

$$
\left( \frac{\partial f}{\partial t} \right)_{\text{coll}} = -\frac{1}{\tau} \left( f - f^{\text{eq}} \right)
$$

---

## Zeroth Order Case

If $f = f^{\text{eq}}$, the collision term becomes zero and $f$ does not evolve with time — representing **no viscosity flows**.

---

## First Order Case

$$
f^{(1)} = -\tau \left( \partial_t^{(1)} f^{(0)} + \mathbf{v} \cdot \nabla^{(1)} f^{(0)} \right)
$$

---

## Macroscopic Equations

**1. Continuity Equation**

Multiply by 1 and integrate over $\mathbf{v}$:

$$
\int \left( \partial_t f + \mathbf{v} \cdot \nabla f \right) d\mathbf{v} = 0
$$

$$
\Rightarrow \partial_t \rho + \nabla \cdot (\rho \mathbf{u}) = 0
$$

**2. Momentum Equation**

Multiply by $\mathbf{v}$ and integrate over $\mathbf{v}$:

$$
\frac{\partial}{\partial t} (\rho \mathbf{u}) + \nabla \cdot \mathbf{P} = 0
$$

where the **pressure tensor** is:

$$
\mathbf{P} = \int \mathbf{v} \mathbf{v} f \, d\mathbf{v}
$$

---

## Applying Chapman–Enskog

Using the expansion for $f^{(1)}$:

$$
\mathbf{P} = \int \mathbf{v} \mathbf{v} f^{(0)} \, d\mathbf{v} + \epsilon f^{(1)} + \dots
$$

The zeroth-order term corresponds to **ideal gas pressure**.

---

## Stress Tensor and Viscosity

From the first-order term:

$$
\mathbf{P}^{(1)} = -\mu \left[ \nabla \mathbf{u} + (\nabla \mathbf{u})^T - \frac{2}{3} (\nabla \cdot \mathbf{u}) \mathbf{I} \right]
$$

where:

$$
\mu = \rho c_s^2 \tau
$$

is the **dynamic viscosity**.

---

## Navier–Stokes Equations from LBM

$$
\rho \left( \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} \right) = -\nabla p + \nabla \cdot \boldsymbol{\sigma}
$$

with:

$$
\sigma_{\alpha \beta} = \rho c_s^2 \tau \left( \frac{\partial u_\alpha}{\partial x_\beta} + \frac{\partial u_\beta}{\partial x_\alpha} - \frac{2}{3} \delta_{\alpha \beta} \nabla \cdot \mathbf{u} \right)
$$

---

## Final Viscosity Relation

Including second-order terms:

$$
\mu = \rho c_s^2 \left( \tau - \frac{1}{2} \right) \Delta t
$$
