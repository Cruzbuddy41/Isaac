import cv2
import numpy as np

def lanes():

    img = cv2.imread('lane.jpg')
    h, w = img.shape[:2]

    v1 = [int(w * 0), h - 1]  # 5% from left edge
    v2 = [int(w * 1), h - 1]  # 95% from left edge
    v3 = [w // 2, int(h * 0.3)]  # Middle width, 40% down from top

    pts = np.array([v1, v2, v3], np.int32)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50,
                            minLineLength=100, maxLineGap=50)

    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, mask_3ch)

    cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

    cv2.imwrite('lanes.jpg', img)
