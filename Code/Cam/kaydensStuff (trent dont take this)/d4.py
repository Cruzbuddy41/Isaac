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

roi_top = int(h * 0.75)
roi_mask = np.zeros_like(blue_mask)
roi_mask[roi_top:h, :] = 255
masked_blue = cv2.bitwise_and(blue_mask, roi_mask)

edges = cv2.Canny(masked_blue, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40,
                        minLineLength=40, maxLineGap=50)

output_img = img.copy()
center_x = w // 2

cv2.line(output_img, (center_x, 0), (center_x, h), (255, 255, 0), 1)

left_xs, left_ys = [], []
right_xs, right_ys = [], []

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        mid_x = (x1 + x2) // 2
        if mid_x < center_x:
            left_xs.extend([x1, x2])
            left_ys.extend([y1, y2])
        else:
            right_xs.extend([x1, x2])
            right_ys.extend([y1, y2])

y_bottom = h - 1
y_top = roi_top + 10

left_x_top = left_x_bottom = None
right_x_top = right_x_bottom = None

if len(left_xs) > 2 and len(np.unique(left_ys)) > 1:
    poly_left = np.poly1d(np.polyfit(left_ys, left_xs, 1))
    left_x_bottom = int(poly_left(y_bottom))
    left_x_top = int(poly_left(y_top))
    cv2.line(output_img, (left_x_bottom, y_bottom), (left_x_top, y_top), (0, 0, 255), 3)

if len(right_xs) > 2 and len(np.unique(right_ys)) > 1:
    poly_right = np.poly1d(np.polyfit(right_ys, right_xs, 1))
    right_x_bottom = int(poly_right(y_bottom))
    right_x_top = int(poly_right(y_top))
    cv2.line(output_img, (right_x_bottom, y_bottom), (right_x_top, y_top), (0, 0, 255), 3)

path_x_top = center_x
lane_width = int(w * 0.6)

if left_x_top is not None and right_x_top is not None:
    path_x_top = (left_x_top + right_x_top) // 2
    path_x_bottom = (left_x_bottom + right_x_bottom) // 2
elif left_x_top is not None:
    path_x_top = left_x_top + (lane_width // 2)
    path_x_bottom = left_x_bottom + (lane_width // 2)
elif right_x_top is not None:
    path_x_top = right_x_top - (lane_width // 2)
    path_x_bottom = right_x_bottom - (lane_width // 2)
else:
    path_x_bottom = center_x

cv2.line(output_img, (path_x_bottom, y_bottom), (path_x_top, y_top), (0, 255, 0), 4)
cv2.circle(output_img, (path_x_top, y_top), 10, (255, 0, 255), -1)

direction = "SEARCHING"
deadzone = 30

if path_x_top < center_x - deadzone:
    direction = "LEFT"
elif path_x_top > center_x + deadzone:
    direction = "RIGHT"
else:
    direction = "FORWARD"

print(f"Detected Direction: {direction}")

cv2.putText(output_img, f"Direction: {direction}", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imwrite('lanes_result.jpg', output_img)