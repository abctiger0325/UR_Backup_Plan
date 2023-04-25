import cv2
import numpy as np
from pygrabber.dshow_graph import FilterGraph

devices = FilterGraph().get_input_devices()

available_cameras = {}

for device_index, device_name in enumerate(devices):
    available_cameras[device_name] = device_index
    print(f"Device {device_index}: {device_name}")

device_id_1 = int(input("Select Camera 1: "))
device_id_2 = int(input("Select Camera 2: "))

capture1 = cv2.VideoCapture(device_id_1)
capture2 = cv2.VideoCapture(device_id_2)

while True:
    ret, img1 = capture1.read()
    cv2.imshow('Image 1', img1)
    if cv2.waitKey(1) == ord('q'):
        ret, img1 = capture1.read()
        break

capture1.release()
cv2.destroyAllWindows()

while True:
    ret, img2 = capture2.read()
    cv2.imshow('Image 2', img2)
    if cv2.waitKey(1) == ord('q'):
        ret, img2 = capture2.read()
        break

capture2.release()
cv2.destroyAllWindows()

def select_roi(event, x, y, flags, param):
    global roi_pts, roi_selected
    
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_pts.append((x, y))
        
        # If we have selected all four points, set roi_selected to True
        if len(roi_pts) == 4:
            roi_selected = True

# Display the images
cv2.imshow('Image 1', img1)
cv2.imshow('Image 2', img2)

# Allow the user to select a rectangular ROI in both images
print("Select the ROI in the first image")
roi1 = cv2.selectROI('Image 1', img1, fromCenter=False, showCrosshair=True)
print("Select the ROI in the second image")
roi2 = cv2.selectROI('Image 2', img2, fromCenter=False, showCrosshair=True)

# Clean up
cv2.destroyAllWindows()
# Extract the ROIs from the images
roi_img1 = img1[int(roi1[1]):int(roi1[1]+roi1[3]), int(roi1[0]):int(roi1[0]+roi1[2])]
roi_img2 = img2[int(roi2[1]):int(roi2[1]+roi2[3]), int(roi2[0]):int(roi2[0]+roi2[2])]

# Resize the second ROI to match the size of the first ROI
if roi_img1.shape != roi_img2.shape:
    roi_img2 = cv2.resize(roi_img2, (roi_img1.shape[1], roi_img1.shape[0]))

cv2.imshow('Image 1', roi_img1)
cv2.imshow('Image 2', roi_img2)
# Calculate the absolute difference between the two ROIs
diff = cv2.absdiff(roi_img1, roi_img2)

# Display the difference image
cv2.imshow('ROI Difference', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()
