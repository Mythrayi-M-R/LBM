import numpy as np
import matplotlib.pyplot as plt

plate_length = 50 # square plate
alpha = 0.25 # alpha declared as 0.25 to avoid overflow
delta_x = 1
tolerance = 1e-4  # Convergence criterion

# temperature is represented using the function u
u = np.zeros((plate_length, plate_length))
u_initial = 0.0

# Boundary conditions
u_top = 60 # heat transfers from this edge throughout the plate
u_left = 30
u_bottom = 30
u_right = 30

# Initialize
u.fill(u_initial)
u[(plate_length-1):, :] = u_top # one subtracted from plate length to match numpy and matlab naming conventions
u[:, :1] = u_left
u[:1, 1:] = u_bottom
u[:, (plate_length-1):] = u_right

def calculate(u):
    u_new = u.copy()
    while True:
        u_old = u_new.copy()
        for i in range(1, plate_length - 1):
            for j in range(1, plate_length - 1):
                u_new[i, j] = alpha * (u_old[i+1, j] + u_old[i-1, j] 
                                       + u_old[i, j+1] + u_old[i, j-1]) #FDM
        # Check max difference for convergence
        diff = np.max(np.abs(u_new - u_old))
        if diff < tolerance:
            break
    return u_new

def plotheatmap(u):
    plt.xlabel("x")
    plt.ylabel("y")
    plt.pcolormesh(u, cmap=plt.cm.jet, shading='auto', vmin=30, vmax=60)
    plt.colorbar(label="Temperature")
    plt.title("Steady-State Temperature (LBM D2Q9)")
    plt.show()


u = calculate(u)
plotheatmap(u)
