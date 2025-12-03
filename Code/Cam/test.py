import cv2
import numpy as np

image = cv2.imread('my_image.jpg')

print(f"Shape: {image.shape}")
print(f"Data type: {image.dtype}")

# Convert our BGR image to Grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(f"Grayscale shape: {gray_image.shape}")
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, binary_mask = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
edges = cv2.Canny(image, 100, 200)
cv2.imshow('Edges', edges)


cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('new_image.png', edges)
