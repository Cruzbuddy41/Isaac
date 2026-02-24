import cv2
import numpy as np

def lanes():
    img = cv2.imread('lane.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 100, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50,
                        minLineLength=50, maxLineGap=50)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

    cv2.imwrite('lanes.jpg', img)
