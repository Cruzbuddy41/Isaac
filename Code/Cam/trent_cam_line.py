import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
time.sleep(2)
ret, frame = cap.read()

if ret:
    print("Frame captured successfully. Processing...")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((19, 19), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    edges = cv2.Canny(mask, 100, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=30, maxLineGap=20)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
    save_path = 'lane_output2.jpg'
    cv2.imwrite(save_path, frame)
    print(f"Image successfully saved to {save_path}")
else:
    print("Error: Could not capture an image from the camera.")

cap.release()