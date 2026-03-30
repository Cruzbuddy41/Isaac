import cv2
import numpy as np

img = cv2.imread('lane.jpg')
if img is None:
    exit()

h, w = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

v1 = [int(w * 0.05), h - 1]
v2 = [int(w * 0.95), h - 1]
v3 = [w // 2, int(h * 0.3)]
pts = np.array([v1, v2, v3], np.int32)
roi_mask = np.zeros((h, w), dtype=np.uint8)
cv2.fillPoly(roi_mask, [pts], 255)

masked_blue = cv2.bitwise_and(blue_mask, roi_mask)

output_img = img.copy()
output_img[masked_blue > 0] = [0, 0, 255]
cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

center_x = w // 2
left_half = masked_blue[:, :center_x]
right_half = masked_blue[:, center_x:]

left_pixels = cv2.countNonZero(left_half)
right_pixels = cv2.countNonZero(right_half)

top_boundary = int(h * 0.4)
top_portion = masked_blue[:top_boundary, :]
top_pixels = cv2.countNonZero(top_portion)

cv2.line(output_img, (center_x, 0), (center_x, h), (255, 255, 0), 1)
cv2.line(output_img, (0, top_boundary), (w, top_boundary), (255, 0, 255), 1)

diff = right_pixels - left_pixels
correction_threshold = 1000
turn_threshold = 3000

direction = "FORWARD"

if top_pixels > turn_threshold:
    if right_pixels > left_pixels:
        direction = "HARD LEFT"
    else:
        direction = "HARD RIGHT"
elif abs(diff) > correction_threshold:
    if right_pixels > left_pixels:
        direction = "SLIGHT LEFT"
    else:
        direction = "SLIGHT RIGHT"

cv2.putText(output_img, f"Dir: {direction}", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(output_img, f"L: {left_pixels} R: {right_pixels}", (50, 90),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
cv2.putText(output_img, f"Top: {top_pixels}", (50, 130),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

cv2.imwrite('lanes_result.jpg', output_img)