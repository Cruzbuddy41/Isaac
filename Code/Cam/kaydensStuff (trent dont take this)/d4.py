import cv2
import numpy as np
<<<<<<< HEAD
import the_robot_photo
the_robot_photo.capture_photo_linux()
=======

>>>>>>> ece195a (new3)
img = cv2.imread('lane.jpg')
if img is None:
    print("Error: Could not load image.")
    exit()

h, w = img.shape[:2]
<<<<<<< HEAD
v1 = [int(w * 0.4), int(h * 0.6)]  # Bottom Left
v2 = [int(w * 0.6), int(h * 0.6)]  # Bottom Right
v3 = [w // 2, int(h * 0.1)]  # Top Peak

pts = np.array([v1, v2, v3], np.int32)
output_img = img.copy()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([100, 100, 50])
upper_blue = np.array([130, 255, 255])
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
roi_mask = np.zeros((h, w), dtype=np.uint8)
cv2.fillPoly(roi_mask, [pts], 255)
masked_blue = cv2.bitwise_and(blue_mask, roi_mask)
lines = cv2.HoughLinesP(masked_blue, 1, np.pi / 180, threshold=30,
                        minLineLength=40, maxLineGap=100)

cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
=======

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
>>>>>>> ece195a (new3)

cv2.line(output_img, (center_x, 0), (center_x, h), (255, 255, 0), 1)

left_x_points = []
right_x_points = []

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
<<<<<<< HEAD
        if slope < -0.3 and x1 < center_x:
            left_slopes.append(slope)
        elif slope > 0.3 and x1 > center_x:
            right_slopes.append(slope)

direction = "UNKNOWN"
=======
>>>>>>> ece195a (new3)

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

# 7. ADD TEXT AND SAVE
cv2.putText(output_img, f"Direction: {direction}", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

<<<<<<< HEAD
cv2.imwrite('lanes_result.jpg', output_img)
=======
cv2.imwrite('lanes_result.jpg', output_img)
>>>>>>> ece195a (new3)
