import numpy as np
import matplotlib.pyplot as plt

# User inputs
diameter_x1 = 24
diameter_x2 = 10

ratio_c = (diameter_x1 / diameter_x2) - 1
remind_height = 14
height_c = remind_height/ratio_c
diameter_y = height_c + remind_height
print(diameter_y)

# reminding_height = 12

# Create a meshgrid of points
n_points = 100
theta = np.linspace(0, 2 * np.pi, n_points)
phi = np.linspace(0, np.pi, n_points)
theta, phi = np.meshgrid(theta, phi)

# Calculate the x, y, z coordinates of each point
x = (diameter_x1 / 2) * np.sin(phi) * np.cos(theta)
y = (diameter_y / 2) * np.sin(phi) * np.sin(theta)
z = (diameter_x1 / 2) * np.cos(phi)

# x,y,z = x,z,y
# Remove the top half of the model
z[z < 0] = 0
z[z > remind_height] = 0

# Plot the oval sphere with the top half removed
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z)
plt.show()
