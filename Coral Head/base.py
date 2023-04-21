import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# User inputs
diameter_x = 24.0
diameter_y = 24.0
diameter_z = 32.0

# Create a sphere
sphere = trimesh.creation.uv_sphere(radius=1.0, count=[32, 32])

# Scale the sphere to an ellipsoid
scale = [diameter_x / 2.0, diameter_y / 2.0, diameter_z / 2.0]
ellipsoid = sphere.apply_scale(scale)

# Slice off the top half of the ellipsoid
plane_normal = np.array([0, 0, 1])  # normal vector of the slicing plane
plane_origin = np.array([0, 0, 0])  # origin of the slicing plane
cut = ellipsoid.slice_plane(plane_normal=plane_normal, plane_origin=plane_origin)

plane_normal = np.array([0, 0, -1])  # normal vector of the slicing plane
plane_origin = np.array([0, 0, 14])  # origin of the slicing plane
cut = cut.slice_plane(plane_normal=plane_normal, plane_origin=plane_origin)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=20, azim=-135)  # set view angle
ax.set_box_aspect([1, 1, 1])  # set equal aspect ratio for all axes
print(trimesh.visual.color.ColorVisuals(cut))

verts = cut.vertices
faces = cut.faces
mesh = Poly3DCollection([verts[face] for face in faces], alpha=0.25, edgecolor='k', facecolor='blue')
ax.add_collection3d(mesh)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add annotations for dimensions
ax.text(0, 0, diameter_z/2 + 1, f"Height = {14:.2f}")
ax.text(diameter_x + 1, 0, 0, f"Radius = {diameter_x:.2f}")

plt.show()

# print(ellipsoid,cut)
# Visualize the cut ellipsoid
# cut.show()
# # Visualize the ellipsoid
# scene = trimesh.Scene([cut])
# scene.show()
