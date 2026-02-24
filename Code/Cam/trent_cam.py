import cv2
import numpy as np
import time


def region_of_interest(img, vertices):
    """Applies an image mask. Only keeps the region of the image defined by the polygon."""
    mask = np.zeros_like(img)
    # Fill the polygon with white (255)
    cv2.fillPoly(mask, vertices, 255)
    # Bitwise AND to only keep edges inside the mask
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


# 1. Initialize camera
cap = cv2.VideoCapture(0)
time.sleep(2)  # Camera warm-up
ret, frame = cap.read()

if ret:
    print("Frame captured. Processing...")

    # 2. Get image dimensions for the Region of Interest
    height = frame.shape[0]
    width = frame.shape[1]

    # 3. Grayscale and Blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduced blur kernel to keep sharp lines

    # 4. Canny Edge Detection (Removed the fixed threshold for better lighting adaptability)
    edges = cv2.Canny(blur, 50, 150)

    # 5. Define Region of Interest (A triangle covering the bottom half of the frame)
    # Adjust these points based on how your camera is mounted!
    roi_vertices = np.array([
        [(0, height),  # Bottom left
         (int(width / 2), int(height / 2)),  # Middle center (vanishing point)
         (width, height)]  # Bottom right
    ], dtype=np.int32)

    # Apply the mask to the edges
    masked_edges = region_of_interest(edges, roi_vertices)

    # 6. Hough Line Transform on the masked edges
    lines = cv2.HoughLinesP(
        masked_edges,
        rho=1,
        theta=np.pi / 180,
        threshold=50,  # Minimum number of intersections to detect a line
        minLineLength=40,  # Minimum length of a line (pixels)
        maxLineGap=20  # Max gap allowed between line segments to connect them
    )

    # 7. Draw the lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)

    # 8. Save the result
    save_path = 'accurate_lane_output.jpg'
    cv2.imwrite(save_path, frame)

    # Tip: Also save the 'masked_edges' image to see exactly what the computer is seeing!
    # cv2.imwrite('debug_edges.jpg', masked_edges)

    print(f"Image successfully saved to {save_path}")

else:
    print("Error: Could not capture an image.")

cap.release()