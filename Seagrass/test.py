import cv2
import numpy as np

# Load the two images
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')

# Convert the images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Find the key points and descriptors in the two images using ORB feature detector
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)

# Match the descriptors between the two images using a brute-force matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Sort the matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# Create an empty mask to mark the matched points
mask = np.zeros_like(img1)

# Draw the matched points on the mask
for match in matches:
    img1_idx = match.queryIdx
    img2_idx = match.trainIdx
    x1, y1 = kp1[img1_idx].pt
    x2, y2 = kp2[img2_idx].pt
    cv2.circle(mask, (int(x1), int(y1)), 5, (255, 255, 255), -1)
    cv2.circle(mask, (int(x2), int(y2)), 5, (255, 255, 255), -1)
    cv2.line(mask, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 2)

# Find the homography matrix between the two images using the matched points
src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Apply the homography matrix to the first image to align it with the second image
img1_aligned = cv2.warpPerspective(img1, H, (img2.shape[1], img2.shape[0]))

# Calculate the absolute difference between the aligned first image and the second image
diff = cv2.absdiff(img1_aligned, img2)

# Convert the difference image to grayscale and apply a binary threshold to it
gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw rectangles around the changed squares
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img1_aligned, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Display the output image
cv2.imshow("Res",img1_aligned)
cv2.waitKey(0)
