import cv2
import numpy as np

# Load an image from disk
image = cv2.imread('my_image.jpg')

# Check its properties (This confirms it's a NumPy array!)
print(f"Shape: {image.shape}") # (height, width, 3) for a color image
print(f"Data type: {image.dtype}") # uint8 (0-255)

# Display the image in a window
cv2.imshow('My Image', image)

# Wait indefinitely for a key press
cv2.waitKey(0)

# Clean up all windows
cv2.destroyAllWindows()

# Write an image back to disk
cv2.imwrite('new_image.png', image)