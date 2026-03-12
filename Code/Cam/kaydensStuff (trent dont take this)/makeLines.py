import cv2
import numpy as np


def lanes():
    # Load the image captured by kaydensVer
    img = cv2.imread('lane.jpg')
    if img is None:
        return None

    h, w = img.shape[:2]

    # Define a triangular Region of Interest (ROI)
    v1, v2 = [int(w * 0.05), h - 1], [int(w * 0.95), h - 1]
    v3 = [w // 2, int(h * 0.6)]
    pts = np.array([v1, v2, v3], np.int32)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50,
                            minLineLength=100, maxLineGap=50)

    all_x = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999
            if abs(slope) > 0.5:
                all_x.extend([x1, x2])
    return sum(all_x) / len(all_x) if all_x else None
