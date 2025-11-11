import cv2
import time
import subprocess  # We might use this later if manual settings are needed

# Open the *correct* camera index 0
cap = cv2.VideoCapture(0)

# Add a significantly longer warm-up delay
# (1 to 2 seconds is often needed for sluggish auto-exposure)
print("Waiting for camera auto-exposure to adjust...")
time.sleep(1.5)

if not cap.isOpened():
    print("Error: Camera 0 could not be opened.")
else:
    print("Camera 0 opened successfully. Attempting capture.")
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('final_image_fixed_exposure.jpg', frame)
        print("Success: Image saved as final_image_fixed_exposure.jpg")
    else:
        print("Error: Failed to read frame from camera.")

cap.release()
