import numpy as np
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 70, 30])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(blurred, kernel, iterations=1)

    edge = cv2.Canny(dilated, 50, 150)

    houghlines = cv2.HoughLinesP(edge, rho=1, theta=np.pi / 180, threshold=50, minLineLength=50, maxLineGap=100)

    # for rtheta in houghlines:
    #     arr = np.array(rtheta[0], dtype=np.float64)
    #     r, theta = arr
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x1 = int(a*r + (10000*(-b)))
    #     y1 = int(b*r + (10000*a))
    #     x2 = int(a*r - 10000*(-b))
    #     y2 = int(b*r - (10000*(a)))
    #
    #
    #
    #     cv2.line(img, (x1,y1), (x2, y2), (0,255,0), 2)
    if houghlines is not None:
        for line in houghlines:
            x1, y1, x2, y2 = line[0] 
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    else:
        print("No lines were detected with the current parameters.")
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
