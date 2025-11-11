import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)
time.sleep(1.5)  # Wait for exposure

ret, frame = cap.read()

if ret:
    # Print max and mean pixel values
    max_val = np.max(frame)
    mean_val = np.mean(frame)
    print(f"Frame captured. Max pixel value: {max_val}, Mean pixel value: {mean_val}")

    cv2.imwrite('diagnostics_image.jpg', frame)
    print("Image saved as diagnostics_image.jpg")
else:
    print("Failed to read frame.")

cap.release()
