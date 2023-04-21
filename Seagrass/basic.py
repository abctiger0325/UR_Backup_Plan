import cv2
import numpy as np

# Load the two images
img1 = cv2.imread('real_image1.jpg')
img2 = cv2.imread('real_image2.jpg')

# Display the images
cv2.imshow('Image 1', img1)
cv2.imshow('Image 2', img2)

# Allow the user to select a rectangular ROI in both images
print("Select the ROI in the first image")
roi1 = cv2.selectROI('Image 1', img1, fromCenter=False, showCrosshair=True)
print("Select the ROI in the second image")
roi2 = cv2.selectROI('Image 2', img2, fromCenter=False, showCrosshair=True)

# Extract the ROIs from the images
roi_img1 = img1[int(roi1[1]):int(roi1[1]+roi1[3]), int(roi1[0]):int(roi1[0]+roi1[2])]
roi_img2 = img2[int(roi2[1]):int(roi2[1]+roi2[3]), int(roi2[0]):int(roi2[0]+roi2[2])]

# Resize the second ROI to match the size of the first ROI
if roi_img1.shape != roi_img2.shape:
    roi_img2 = cv2.resize(roi_img2, (roi_img1.shape[1], roi_img1.shape[0]))

# Calculate the absolute difference between the two ROIs
diff = cv2.absdiff(roi_img1, roi_img2)

# Display the difference image
cv2.imshow('ROI Difference', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()
