# To capture from a webcam, use 0
# To open a video file, use the path: 'my_video.mp4'
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()#

while True:
    # Read one frame at a time
    ret, frame = cap.read()

    # 'ret' is a boolean: True if frame was read successfully
    if not ret:
        print("End of video or error.")
        break

    # --- PROCESS YOUR FRAME HERE ---
    # Example: Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ---

    # Display the processed frame
    cv2.imshow('Webcam Feed', gray_frame)

    # Quit when 'q' is pressed
    # We use a 1ms waitKey. This also controls the video playback speed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()


