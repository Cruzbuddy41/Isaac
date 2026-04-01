import cv2
import numpy as np
import movement

print("wsp brodie")

print("reading the image")
img = cv2.imread('lane.jpg')

if img is None:
    print("something bad just happened")
    exit()

print(f"Image found! Dimensions: {img.shape}")
h, w = img.shape[:2]

print("Converting colors to HSV")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

print("Creating blue mask")
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

print("Drawing the triangle boundaries")
v1 = [int(w * 0.05), h - 1]
v2 = [int(w * 0.95), h - 1]
v3 = [w // 2, int(h * 0.3)]
pts = np.array([v1, v2, v3], np.int32)
roi_mask = np.zeros((h, w), dtype=np.uint8)

print("Filling the polygon")
cv2.fillPoly(roi_mask, [pts], 255)

print("Cropping mask to triangle")
masked_blue = cv2.bitwise_and(blue_mask, roi_mask)

print("Preparing the output image drawing")
output_img = img.copy()
output_img[masked_blue > 0] = [0, 0, 255]
cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

print("Doing the pixel math")
center_x = w // 2
turn_y_boundary = int(h * 0.5)

turn_zone = masked_blue[:turn_y_boundary, :]
top_pixels = cv2.countNonZero(turn_zone)

correction_zone = masked_blue[turn_y_boundary:, :]
left_correction = correction_zone[:, :center_x]
right_correction = correction_zone[:, center_x:]

left_pixels = cv2.countNonZero(left_correction)
right_pixels = cv2.countNonZero(right_correction)
pixel_diff = right_pixels - left_pixels

print("Drawing lines and text")
cv2.line(output_img, (center_x, turn_y_boundary), (center_x, h), (255, 255, 0), 2)
cv2.line(output_img, (0, turn_y_boundary), (w, turn_y_boundary), (255, 165, 0), 2)

turn_threshold = 12000
correction_threshold = 2000
direction = "FORWARD"
if top_pixels > turn_threshold:
    if right_pixels > left_pixels:
        direction = "HARD LEFT"
        movement.move_left(50, 1)
    else:
        direction = "HARD RIGHT"
        movement.move_right(50, 1)

elif abs(pixel_diff) > correction_threshold:
    if pixel_diff > 0:
        direction = "SLIGHT LEFT"
        movement.move_left(25, 0.5)
    else:
        direction = "SLIGHT RIGHT"
        movement.move_right(25, 0.5)

elif (left_pixels + right_pixels) > 500:
    direction = "FORWARD"
    movement.move_forward(40, 1)

cv2.putText(output_img, f"Dir: {direction}", (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

print("Saving image gng")
cv2.imwrite('lanes_result.jpg', output_img)

print(f"Did it thank me with a special gift wink* wink* I went: {direction}")
