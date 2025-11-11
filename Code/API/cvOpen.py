import cv2
import time

# Try index 0
cap0 = cv2.VideoCapture(0)
# Try index 1
cap1 = cv2.VideoCapture(1)

# Add delays
time.sleep(0.5)

ret0, frame0 = cap0.read()
ret1, frame1 = cap1.read()

if ret0:
    cv2.imwrite('image_0.jpg', frame0)
    print("Image 0 captured successfully.")
if ret1:
    cv2.imwrite('image_1.jpg', frame1)
    print("Image 1 captured successfully.")
if not ret0 and not ret1:
    print("Neither camera captured an image.")

cap0.release()
cap1.release()
