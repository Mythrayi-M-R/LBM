import numpy as np
import matplotlib.pyplot as plt

# Domain parameters
Lx, Ly = 2.0, 1.0
nx, ny = 41, 21
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Flow properties
u, v = 0.05, 0.0
alpha = 0.01

# LBM parameters
tau = 3 * alpha + 0.5
omega = 1.0 / tau

# Time loop parameters
max_iter = 10000
convergence_threshold = 1e-5

# D2Q5 model
w = np.array([1/3, 1/6, 1/6, 1/6, 1/6])
e = np.array([[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]])

# Initialize distribution functions
f = np.zeros((ny, nx, 5))
feq = np.zeros_like(f)
T = np.ones((ny, nx)) * 30.0

# Apply initial boundary conditions
T[0, :] = 60.0
T[-1, :] = 60.0
T[:, 0] = 30.0

# Initialize f with equilibrium
for i in range(5):
    f[:, :, i] = w[i] * T

# Main LBM loop
for iteration in range(max_iter):
    T_old = T.copy()

    # Equilibrium calculation
    for i in range(5):
        eu = e[i, 0] * u + e[i, 1] * v
        feq[:, :, i] = w[i] * T * (1 + 3 * eu)

    # Collision step
    f = (1 - omega) * f + omega * feq

    # Streaming step (manual shift per direction)
    f_streamed = np.zeros_like(f)
    for i in range(5):
        ex, ey = e[i]
        f_streamed[:, :, i] = np.roll(np.roll(f[:, :, i], shift=ey, axis=0), shift=ex, axis=1)
    f = f_streamed

    # Boundary conditions
    # Inlet (Dirichlet T=30)
    T_inlet = 30.0
    f[:, 0, 1] = w[1] * T_inlet * (1 + 3 * u)
    f[:, 0, 2] = w[2] * T_inlet * (1 - 3 * u)
    f[:, 0, 3] = w[3] * T_inlet
    f[:, 0, 4] = w[4] * T_inlet

    # Outlet (zero gradient)
    f[:, -1, :] = f[:, -2, :]

    # Top wall (Dirichlet T=60)
    f[0, :, 3] = w[3] * 60.0
    f[0, :, 4] = w[4] * 60.0

    # Bottom wall (Dirichlet T=60)
    f[-1, :, 3] = w[3] * 60.0
    f[-1, :, 4] = w[4] * 60.0

    # Recalculate temperature
    T = np.sum(f, axis=2)

    # Apply macroscopic boundary conditions again (to fix small drift)
    T[0, :] = 60.0
    T[-1, :] = 60.0
    T[:, 0] = 30.0

    # Convergence check
    change = np.sqrt(np.mean((T - T_old)**2))
    if iteration % 100 == 0:
        print(f"Iter {iteration}, ΔT = {change:.2e}, T: {T.min():.1f}–{T.max():.1f}")
    if change < convergence_threshold:
        print(f"Converged in {iteration} iterations with ΔT = {change:.2e}")
        break

# Final temperature plot
plt.figure(figsize=(10, 5))
plt.contourf(X, Y, T, levels=20, cmap='jet')
plt.colorbar(label='Temperature (°C)')
plt.title('Final Temperature Distribution (LBM)')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# Temperature profiles
plt.figure(figsize=(8, 5))
for y_idx in [0, ny//4, ny//2, 3*ny//4, ny-1]:
    plt.plot(x, T[y_idx, :], label=f'y = {y[y_idx]:.2f}')
plt.xlabel('x')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Profiles at Various y')
plt.legend()
plt.grid(True)
plt.show()
