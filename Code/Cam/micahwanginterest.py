import cv2
import numpy as np

img = cv2.imread('/Users/bd6010870/Downloads/line_998x1331.png')
h, w = img.shape[:2]


side_length = 1400
tri_height = int((np.sqrt(3) / 2) * side_length) 

start_x = (w - side_length) // 2 
end_x = start_x + side_length

v1 = [start_x, h - 1]
v2 = [end_x, h - 1]
v3 = [w // 2, h - 1 - tri_height]

pts = np.array([v1, v2, v3], np.int32)


mask = np.zeros((h, w), dtype=np.uint8)

cv2.fillPoly(mask, [pts], 255)


result = np.zeros_like(img)
result[mask == 255] = img[mask == 255]

cv2.polylines(result, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

cv2.imshow('hola sadiq', result)
cv2.waitKey(0)
