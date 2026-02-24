import cv2
import numpy as np
import time

# 1. Initialize camera for Raspberry Pi
cap = cv2.VideoCapture(0)
time.sleep(2)  # Camera warm-up
ret, frame = cap.read()

if ret:
    print("Frame captured. Processing...")

    # 2. Grayscale and Blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Otsu's Thresholding (Isolates the tape/grout from the tiles)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 4. Morphological Opening (Erases the thin grout lines, keeps the thick tape)
    kernel = np.ones((7, 7), np.uint8)
    clean_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # 5. Canny Edge Detection
    edges = cv2.Canny(clean_mask, 50, 150)

    # 6. STANDARD Hough Line Transform (cv2.HoughLines instead of HoughLinesP)
    # This returns polar coordinates (rho, theta) for infinite lines
    # The threshold '100' means a line needs at least 100 edge points to be recognized
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=100)

    # 7. Math to draw the standard Hough Lines
    if lines is not None:
        for line in lines:
            rho, theta = line[0]

            # Convert polar coordinates to Cartesian to draw on the image
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            # Create two points far off the screen to draw a continuous line
            x1 = int(x0 + 2000 * (-b))
            y1 = int(y0 + 2000 * (a))
            x2 = int(x0 - 2000 * (-b))
            y2 = int(y0 - 2000 * (a))

            # Draw the continuous border line in green
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # 8. Save the final image to the Raspberry Pi
    cv2.imwrite('standard_hough_borders.jpg', frame)
    print("Image successfully saved.")

else:
    print("Error: Could not capture an image from the camera.")

cap.release()