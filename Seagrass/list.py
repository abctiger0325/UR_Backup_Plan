import cv2

img1 = cv2.imread('image1.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
cv2.imshow('Image 1', gray1)

print("Select the ROI in the first image")
roi1 = cv2.selectROI('Image 1', gray1, fromCenter=False, showCrosshair=True)

roi_img1 = img1[int(roi1[1]):int(roi1[1]+roi1[3]), int(roi1[0]):int(roi1[0]+roi1[2])]

_, thresh_black1 = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
contours_black1, _ = cv2.findContours(thresh_black1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt1 in contours_black1:
    perimeter1 = cv2.arcLength(cnt1, True)
    approx1 = cv2.approxPolyDP(cnt1, 0.02*perimeter1, True)
    area1 = cv2.contourArea(cnt1)
    if len(approx1) == 4 and area1 > 1000 and area1 < 10000:
        x, y, w, h = cv2.boundingRect(cnt1)
        square_roi = gray1[y:y+h, x:x+w]
        if cv2.mean(square_roi)[0] < 128:
            num_green_squares1 += 1
        else:
            num_white_squares1 += 1
            
print(f"Number of green squares in previous frame: {num_green_squares1}")
print(f"Number of white squares in previous frame: {num_white_squares1}")

if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()