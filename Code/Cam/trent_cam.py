import cv2
import numpy as np
import time

# 1. Initialize camera
cap = cv2.VideoCapture(0)
time.sleep(2)  # Camera warm-up
ret, frame = cap.read()

if ret:
    print("Frame captured. Processing...")

    # --- Image Processing Pipeline ---

    # 2. Grayscale and Blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Otsu's Thresholding
    # Automatically calculates the best threshold value to separate the
    # light tiles from the darker tape and grout. Inverts it so darks become white.
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 4. Morphological Opening (The Grout Eraser)
    # A 7x7 kernel will erase any white lines thinner than 7 pixels (the grout),
    # while keeping the thicker white blobs (the tape).
    kernel = np.ones((7, 7), np.uint8)
    clean_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # 5. Canny Edge Detection on the cleaned mask
    edges = cv2.Canny(clean_mask, 50, 150)

    # 6. Hough Line Transform
    # We increase maxLineGap heavily to jump over the torn/missing pieces of tape
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=40,
        minLineLength=50,  # Ignore tiny random edges
        maxLineGap=100  # High gap to connect the patchy/torn tape segments
    )

    # 7. Draw the lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Drawing green lines so they contrast well with the blue tape
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)

    # 8. Save the results (including debug images!)
    cv2.imwrite('lane_final_output.jpg', frame)

    # Saving these debug images is highly recommended so you can see how
    # the Pi is "thinking" step-by-step
    cv2.imwrite('debug_1_thresh.jpg', thresh)
    cv2.imwrite('debug_2_clean_mask.jpg', clean_mask)
    cv2.imwrite('debug_3_edges.jpg', edges)

    print("Images successfully saved.")

else:
    print("Error: Could not capture an image from the camera.")

cap.release()