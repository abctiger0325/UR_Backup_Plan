from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import itertools
import math


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = [10, 10, 10, 10,15,15,15,15]
y = [10, 15, 15, 10,10, 15, 15, 10]
z = [10, 10, 15, 15,10, 10, 15, 15]

nums = [0, 1, 2, 3, 4,5,6,7]
combinations = list(itertools.combinations(nums, 4))
# print(combinations)
vertices =  [list(combinations[i]) for i in range(len(combinations))]
# vertices = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]

tupleList = list(zip(x, y, z))
tupleList = [list(tupleList[i]) for i in range(len(tupleList))]

centroid = np.mean(tupleList, axis=0)
print(tupleList)

poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]

ax.scatter(x,y,z)
ax.add_collection3d(Poly3DCollection(poly3d, facecolors='w', linewidths=1, alpha=1))

angle = math.radians(45)

R = np.array([
    [np.cos(angle), -np.sin(angle), 0],
    [np.sin(angle), np.cos(angle), 0],
    [0, 0, 1]
])

new_vertices = []
for v in tupleList:
    # Translate the vertex to the origin
    v -= centroid
    # Apply the rotation matrix
    v = np.matmul(R, v)
    # Translate the vertex back to the centroid
    v += centroid
    new_vertices.append(v)

# tupleList = np.dot(tupleList, R)
new_vertices = [list(new_vertices[i]) for i in range(len(new_vertices))]
# new_vertices = np.dot(new_vertices, R)
# print(new_vertices)


poly3d = [[new_vertices[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
ax.add_collection3d(Poly3DCollection(poly3d, facecolors='b', linewidths=1, alpha=1))

plt.show()