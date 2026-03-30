import cv2
import numpy as np

img = cv2.imread('lane.jpg')
if img is None:
    print("Error: Could not load image.")
    exit()

h, w = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

roi_top = int(h * 0.2)
roi_mask = np.zeros_like(blue_mask)
roi_mask[roi_top:h, :] = 255
masked_blue = cv2.bitwise_and(blue_mask, roi_mask)

edges = cv2.Canny(masked_blue, 50, 150)

lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40,
                        minLineLength=40, maxLineGap=50)

output_img = img.copy()
center_x = w // 2

cv2.line(output_img, (center_x, 0), (center_x, h), (255, 255, 0), 1)

left_x_points = []
right_x_points = []

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        mid_x = (x1 + x2) // 2
        if mid_x < center_x:
            left_x_points.append(mid_x)
        else:
            right_x_points.append(mid_x)

direction = "SEARCHING"
deadzone = 40

if len(left_x_points) > 0 and len(right_x_points) > 0:
    avg_left = int(np.mean(left_x_points))
    avg_right = int(np.mean(right_x_points))

    path_center = (avg_left + avg_right) // 2

    cv2.circle(output_img, (path_center, h // 2), 10, (0, 255, 0), -1)

    if path_center < center_x - deadzone:
        direction = "LEFT"
    elif path_center > center_x + deadzone:
        direction = "RIGHT"
    else:
        direction = "FORWARD"

elif len(left_x_points) > 0:
    direction = "RIGHT"

elif len(right_x_points) > 0:
    direction = "LEFT"

print(f"Detected Direction: {direction}")

cv2.putText(output_img, f"Direction: {direction}", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imwrite('lanes_result.jpg', output_img)
#