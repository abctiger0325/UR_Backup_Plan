import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import itertools
import math
from pygrabber.dshow_graph import FilterGraph
import cv2

devices = FilterGraph().get_input_devices()

available_cameras = {}

for device_index, device_name in enumerate(devices):
    available_cameras[device_name] = device_index
    print(f"Device {device_index}: {device_name}")

device_id_1 = int(input("Select Camera : "))

capture1 = cv2.VideoCapture(device_id_1)

colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]
text_color = (255, 255, 255)

# Define the font for the text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5

# Define the length of the first line in cm
ref_length = 5
ref_pixel = 1

# Define the number of lines to draw
num_lines = 4

# Define a list to store the line endpoints
line_points = []

# Define a variable to keep track of how many lines have been drawn
lines_drawn = 0

# Create a window to display the image
cv2.namedWindow('image')

while True:
    ret, img1 = capture1.read()
    cv2.imshow('Image 1', img1)
    if cv2.waitKey(1) == ord('q'):
        ret, img1 = capture1.read()
        break
capture1.release()
cv2.destroyAllWindows()
# Function to calculate the length of a line segment
def length(pt1, pt2):
    return np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)

# Function to handle mouse events
def draw_line(event, x, y, flags, param):
    global line_points, lines_drawn, ref_pixel

    if event == cv2.EVENT_LBUTTONDOWN and lines_drawn < num_lines:
        # Add the current point to the line_points list
        line_points.append((x, y))

        # Draw a circle at the current point
        cv2.circle(img1, (x, y), 2, colors[lines_drawn], -1)



        # If two points have been added to the line_points list, draw a line between them
        if len(line_points) == 2:
            cv2.line(img1, line_points[0], line_points[1], colors[lines_drawn-1], 2)
            # Increment the number of lines drawn
            lines_drawn += 1
            # Calculate the length of the line
            line_length = length(line_points[0], line_points[1])
            
            
            # Display the length on the image
            if (lines_drawn == 1):
                text = f"{ref_length:.2f} cm"
                text_size, _ = cv2.getTextSize(text, font, font_scale, 1)
                text_pos = ((line_points[0][0] + line_points[1][0] - text_size[0]) // 2,
                            (line_points[0][1] + line_points[1][1] + text_size[1]) // 2)
                cv2.putText(img1, text, text_pos, font, font_scale, text_color, 1, cv2.LINE_AA)
                ref_pixel = line_length
            else:
                # Calculate the length in cm, assuming the first line is 5cm
                cm_length = (line_length / ref_pixel) * ref_length
                text = f"{cm_length:.2f} cm"
                text_size, _ = cv2.getTextSize(text, font, font_scale, 1)
                text_pos = ((line_points[0][0] + line_points[1][0] - text_size[0]) // 2,
                            (line_points[0][1] + line_points[1][1] + text_size[1]) // 2)
                cv2.putText(img1, text, text_pos, font, font_scale, text_color, 1, cv2.LINE_AA)
                print(f"Line {lines_drawn-1} length: {cm_length:.2f}")

            # Clear the line_points list
            line_points.clear()

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_line)
while True:
    # Display the image
    cv2.imshow('image', img1)

    # Wait for a key event
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, quit the program
    if key == ord('q'):
        break


# User inputs
diameter_x = int(input("Diameter: "))
diameter_y = diameter_x

remain_z = int(input("Height: "))
Dome = int(input("Dome or Flat on Top (1:Dome, 0:Flat): "))
diameter_z = remain_z + (remain_z * 1.2 * Dome)
# remain_z = 10.5

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
ax.set_box_aspect([10, 10, 10])  # set equal aspect ratio for all axes
# print(trimesh.visual.color.ColorVisuals(sliced_mesh))

verts = cut.vertices
faces = cut.faces
mesh = Poly3DCollection([verts[face] for face in faces], alpha=1, edgecolor='k', facecolor='blue')
ax.add_collection3d(mesh)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add annotations for dimensions
ax.text(0, 0, diameter_z/2 + 1, f"Height = {remain_z:.2f}")
ax.text(diameter_x + 1, 0, 0, f"Radius = {diameter_x:.2f}")

for i in range(3):
    # Add area
    # x = cal, y = 0,z = level
    # x^2 / a^2 + y^2 / b^2 = 1
    #0.765 : 14^2 / 16^2
    length = int(input(f"Square {i} length(2,4,6):"))
    latitude = int(input(f"Square {i} latitude(1[Low] - 4[High]):"))
    area_height = (remain_z/4) * latitude

    longitude = int(input(f"Square {i} longitude(1 - 12):"))
    angle = math.radians(-30 * (longitude % 12))
    # color = input(f"Square {i} Color:")

    R = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])

    oval_x = (1 - (area_height**2/(diameter_z/2)**2)) * 12**2
    # oval_x = (1 - 0.765) * 12**2
    oval_x = math.sqrt(oval_x)
    center = [oval_x,0,area_height]

    center[0] = oval_x * np.cos(angle)
    center[1] = oval_x * np.sin(angle)
    print(center)

    ax.text(center[0] + 1, center[1] + 1, center[2] + 1, f"Size = {length} x {length}")
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

    rotated_vertices = np.dot(square_vertices, R)

    nums = [0, 1, 2, 3, 4,5,6,7]
    combinations = list(itertools.combinations(nums, 4))
    # print(combinations)
    vertices =  [list(combinations[i]) for i in range(len(combinations))]
    poly3d = [[square_vertices[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='red', linewidths=1, alpha=1))

plt.show()

# print(ellipsoid,cut)
# Visualize the cut ellipsoid
# cut.show()
# # Visualize the ellipsoid
# scene = trimesh.Scene([cut])
# scene.show()
