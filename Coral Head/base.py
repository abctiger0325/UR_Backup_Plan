import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import itertools
import math

# User inputs
diameter_x = 24.0
diameter_y = 24.0
diameter_z = 32.0
remain_z = 14.0
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
plane_origin = np.array([0, 0, remain_z])  # origin of the slicing plane
cut = cut.slice_plane(plane_normal=plane_normal, plane_origin=plane_origin)


# Create a new trimesh object with the sliced mesh and add a plane to it
# sliced_mesh = trimesh.Trimesh(vertices=cut.vertices, faces=cut.faces)
# plane_mesh = trimesh.creation.plane(plane_origin, plane_normal)
# sliced_mesh = sliced_mesh + plane_mesh

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=20, azim=-135)  # set view angle
ax.set_box_aspect([1, 1, 1])  # set equal aspect ratio for all axes
# print(trimesh.visual.color.ColorVisuals(sliced_mesh))

verts = cut.vertices
faces = cut.faces
mesh = Poly3DCollection([verts[face] for face in faces], alpha=0.25, edgecolor='k', facecolor='blue')
ax.add_collection3d(mesh)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add annotations for dimensions
ax.text(0, 0, diameter_z/2 + 1, f"Height = {remain_z:.2f}")
ax.text(diameter_x + 1, 0, 0, f"Radius = {diameter_x:.2f}")

# Add area
# x = cal, y = 0,z = level
# x^2 / a^2 + y^2 / b^2 = 1
#0.765 : 14^2 / 16^2
# area_height = (remain_z/4) * 3
# oval_x = (1 - math.sqrt(area_height**2/(diameter_z/2)**2)) * 12**2
oval_x = (1 - 0.765) * 12**2
oval_x = math.sqrt(oval_x)
center = [oval_x,0,(remain_z/4) * 3]
print(center)
length = 2

square_vertices = np.array([
        [center[0] - length /2 , center[1] - length /2 , center[2] - length /2 ],
        [center[0] + length /2 , center[1] - length /2 , center[2] - length /2 ],
        [center[0] + length /2 , center[1] + length /2 , center[2] - length /2 ],
        [center[0] - length /2 , center[1] + length /2 , center[2] - length /2 ],
        [center[0] - length /2 , center[1] - length /2 , center[2] + length /2 ],
        [center[0] + length /2 , center[1] - length /2 , center[2] + length /2 ],
        [center[0] + length /2 , center[1] + length /2 , center[2] + length /2 ],
        [center[0] - length /2 , center[1] + length /2 , center[2] + length /2 ]
    ])

nums = [0, 1, 2, 3, 4,5,6,7]
combinations = list(itertools.combinations(nums, 4))
# print(combinations)
vertices =  [list(combinations[i]) for i in range(len(combinations))]
poly3d = [[square_vertices[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
ax.add_collection3d(Poly3DCollection(poly3d, facecolors='b', linewidths=1, alpha=1))

plt.show()

# print(ellipsoid,cut)
# Visualize the cut ellipsoid
# cut.show()
# # Visualize the ellipsoid
# scene = trimesh.Scene([cut])
# scene.show()
