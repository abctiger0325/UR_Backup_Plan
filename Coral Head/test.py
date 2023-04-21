import cv2
import numpy as np

# Function to calculate the length of a line segment
def length(pt1, pt2):
    return np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)

# Load the image
img = cv2.imread('image.jpg')

# Define the colors for the lines and text
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

# Function to handle mouse events
def draw_line(event, x, y, flags, param):
    global line_points, lines_drawn, ref_pixel

    if event == cv2.EVENT_LBUTTONDOWN and lines_drawn < num_lines:
        # Add the current point to the line_points list
        line_points.append((x, y))

        # Draw a circle at the current point
        cv2.circle(img, (x, y), 2, colors[lines_drawn], -1)



        # If two points have been added to the line_points list, draw a line between them
        if len(line_points) == 2:
            cv2.line(img, line_points[0], line_points[1], colors[lines_drawn-1], 2)
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
                cv2.putText(img, text, text_pos, font, font_scale, text_color, 1, cv2.LINE_AA)
                ref_pixel = line_length
            else:
                # Calculate the length in cm, assuming the first line is 5cm
                cm_length = (line_length / ref_pixel) * ref_length
                text = f"{cm_length:.2f} cm"
                text_size, _ = cv2.getTextSize(text, font, font_scale, 1)
                text_pos = ((line_points[0][0] + line_points[1][0] - text_size[0]) // 2,
                            (line_points[0][1] + line_points[1][1] + text_size[1]) // 2)
                cv2.putText(img, text, text_pos, font, font_scale, text_color, 1, cv2.LINE_AA)

            # Clear the line_points list
            line_points.clear()

# Create a window to display the image
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_line)

# Loop until the user presses the 'q' key
while True:
    # Display the image
    cv2.imshow('image', img)

    # Wait for a key event
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, quit the program
    if key == ord('q'):
        break

# Close all windows
cv2.destroyAllWindows()
