import numpy as np
import matplotlib.pyplot as plt

nx, ny = 50, 50
omega = 1.0
tolerance = 1e-4
max_iter = 10000  # just in case it doesn't converge

# D2Q9 model
c = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1],
              [1, 1], [-1, 1], [-1, -1], [1, -1]])
w = np.array([4/9] + [1/9]*4 + [1/36]*4)

# Fields
T = np.full((nx, ny), 30.0)
f = np.zeros((9, nx, ny))
feq = np.zeros_like(f)

# Boundary conditions
T[:, 0] = 30     # left
T[:, -1] = 30    # right
T[0, :] = 30     # top
T[-1, :] = 60    # bottom

# Initialization
for k in range(9):
    f[k] = w[k] * T

# LBM loop
for it in range(max_iter):
    T_prev = T.copy()

    # Compute macroscopic temperature
    T = np.sum(f, axis=0)

    # Collision step
    for k in range(9):
        feq[k] = w[k] * T
        f[k] += -omega * (f[k] - feq[k])

    # Streaming step
    for k in range(9):
        dx, dy = c[k]
        f[k] = np.roll(f[k], shift=dx, axis=0)
        f[k] = np.roll(f[k], shift=dy, axis=1)

    # Reapply boundary conditions directly
    T[:, 0] = 30
    T[:, -1] = 30
    T[0, :] = 30
    T[-1, :] = 60

    for k in range(9):
        f[k, :, 0] = w[k] * T[:, 0]     # left
        f[k, :, -1] = w[k] * T[:, -1]   # right
        f[k, 0, :] = w[k] * T[0, :]     # top
        f[k, -1, :] = w[k] * T[-1, :]   # bottom

    # Convergence check
    if np.max(np.abs(T - T_prev)) < tolerance:
        print(f"Converged in {it+1} iterations.")
        break
else:
    print("Did not converge within max_iter.")

# Plot result
plt.pcolormesh(T.T, cmap='jet', shading='auto', vmin=30, vmax=60)
plt.colorbar(label="Temperature")
plt.title("Steady-State Temperature (LBM D2Q9)")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
