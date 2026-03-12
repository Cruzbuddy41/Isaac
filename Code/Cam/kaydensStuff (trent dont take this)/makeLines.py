import cv2
import numpy as np

def lanes():

    img = cv2.imread('lane.jpg')
    if img is None:
        print("Error: Could not load image.")
        exit()

    h, w = img.shape[:2]
    v1 = [int(w * 0.05), h - 1]  # Bottom Left
    v2 = [int(w * 0.95), h - 1]  # Bottom Right
    v3 = [w // 2, int(h * 0.6)]  # (Middle width, 30% down)

    pts = np.array([v1, v2, v3], np.int32)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50,
                            minLineLength=100, maxLineGap=50)
    output_img = img.copy()
    cv2.polylines(output_img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    left_slopes = []
    right_slopes = []
    center_x = w / 2

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 999
            cv2.line(output_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            if slope < -0.5 and x1 < center_x:
                left_slopes.append(slope)
            elif slope > 0.5 and x1 > center_x:
                right_slopes.append(slope)
    direction = "UNKNOWN"

    if len(left_slopes) > 0 and len(right_slopes) > 0:
        direction = "FORWARD"
    elif len(left_slopes) > 0:
        direction = "RIGHT"
    elif len(right_slopes) > 0:
        direction = "LEFT"
    else:
        direction = "SEARCHING"

    print(f"Detected Direction: {direction}")

    cv2.putText(output_img, f"Direction: {direction}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Save result
    cv2.imwrite('lanes_result.jpg', output_img)

