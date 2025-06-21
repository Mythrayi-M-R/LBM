import numpy as np
import matplotlib.pyplot as plt

# Parameters
Lx = 2.0  # Domain length in x-direction
Ly = 1.0  # Domain length in y-direction
nx = 41  # Number of grid points in x-direction
ny = 21  # Number of grid points in y-direction
dx = Lx / (nx - 1)  # Grid spacing in x-direction
dy = Ly / (ny - 1)  # Grid spacing in y-direction

# Velocity (only in x-direction)
u = 1.0  # Constant x-velocity
v = 0.0  # No y-velocity

# Thermal diffusivity
alpha = 0.01

# Time parameters
dt = 0.001  # Time step
max_iter = 10000  # Maximum iterations
convergence_threshold = 1e-4  # Convergence criterion

# Initialize temperature field
T = np.ones((ny, nx)) * 30.0  # Initial temperature 30°C everywhere

# Boundary conditions
T[0, :] = 60.0   # Top wall at 60°C
T[-1, :] = 60.0  # Bottom wall at 60°C
T[:, 0] = 30.0   # Inlet at 30°C

# Create grid
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Function to update temperature field
def update_temp(T, dt, dx, dy, u, v, alpha):
    Tn = T.copy()
    
    # Apply boundary conditions
    Tn[0, :] = 60.0   # Top wall
    Tn[-1, :] = 60.0  # Bottom wall
    Tn[:, 0] = 30.0   # Inlet
    
    # Calculate new temperature using finite differences
    for i in range(1, ny-1):
        for j in range(1, nx-1):
            # Advection terms (upwind scheme)
            if u > 0:
                adv_x = u * (T[i, j] - T[i, j-1]) / dx
            else:
                adv_x = u * (T[i, j+1] - T[i, j]) / dx
                
            if v > 0:
                adv_y = v * (T[i, j] - T[i-1, j]) / dy
            else:
                adv_y = v * (T[i+1, j] - T[i, j]) / dy
                
            # Diffusion terms (central difference)
            diff_x = alpha * (T[i, j+1] - 2*T[i, j] + T[i, j-1]) / dx**2
            diff_y = alpha * (T[i+1, j] - 2*T[i, j] + T[i-1, j]) / dy**2
            
            # Update temperature
            Tn[i, j] = T[i, j] - dt * (adv_x + adv_y) + dt * (diff_x + diff_y)
    
    # Neumann boundary condition at outlet (zero gradient)
    Tn[:, -1] = Tn[:, -2]
    
    return Tn

# Solve until convergence
for n in range(max_iter):
    T_old = T.copy()
    T = update_temp(T, dt, dx, dy, u, v, alpha)
    
    # Calculate L2 norm of the change
    change = np.sqrt(np.sum((T - T_old)**2) / (nx * ny))
    
    # Optional: Plot intermediate state every 500 iterations
    if n % 500 == 0 and n > 0:
        plt.figure(figsize=(10, 5))
        plt.contourf(X, Y, T, levels=20, cmap='jet')
        plt.colorbar(label='Temperature (°C)')
        plt.title(f'Intermediate Temperature Distribution (Iteration {n})')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
    
    # Check for convergence
    if change < convergence_threshold:
        print(f"Converged after {n} iterations with change {change:.2e}")
        break

# Final temperature distribution
plt.figure(figsize=(10, 5))
plt.contourf(X, Y, T, levels=20, cmap='jet')
plt.colorbar(label='Temperature (°C)')
plt.title('Final Temperature Distribution (Steady State)')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

