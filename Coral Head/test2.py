from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import itertools
import math


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# x = r, y = 0,z = level
center = [12,0,10]
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

# ax.scatter(vertices)
ax.add_collection3d(Poly3DCollection(poly3d, facecolors='w', linewidths=1, alpha=1))


plt.show()