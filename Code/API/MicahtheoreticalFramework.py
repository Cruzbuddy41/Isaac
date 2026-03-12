import cv2
import numpy as np
import time

horizlines = 0


def actualcode(threshold): #this is the actual code. I compressed it into a function for recursion
    global horizlines
    global frame
    horizlines = 0
    h, w = frame.shape[:2]

    side_length = 1400
    tri_height = int((np.sqrt(3) / 2) * side_length)

    start_x = (w - side_length) // 2
    end_x = start_x + side_length

    v1 = [start_x, h - 1]
    v2 = [end_x, h - 1]
    v3 = [w // 2, h - 1 - tri_height]

    pts = np.array([v1, v2, v3], np.int32)

    mask = np.zeros((h, w), dtype=np.uint8)

    cv2.fillPoly(mask, [pts], 255)

    result = np.zeros_like(frame)
    result[mask == 255] = frame[mask == 255]

    cv2.polylines(result, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 70, 30])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(blurred, kernel, iterations=1)

    edge = cv2.Canny(dilated, 50, 150)

    houghlines = cv2.HoughLinesP(edge, rho=1, theta=np.pi / 180, threshold=50, minLineLength=50, maxLineGap=100)

    if houghlines is not None:
        for line in houghlines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            x1, y1, x2, y2 = line[0]

            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            if dx > dy and dy < threshold:
                orientation = "Horizontal"
                horizlines+=1
            elif dy > dx and dx < threshold:
                orientation = "Vertical"
            else:
                orientation = "Diagonal/Unknown"
    else:
        print("No lines were detected with the current parameters.")


def check_for_options(): # what im going to do is basically turn left and turn right in order to detect if there's a horizontal line in front of me.
    move_left(10, 1.5) #move left assume this is a 90-degree turn
    actualcode(30) #arbitrary threshold; will change in future
    if horizlines > 0:

        move_right(50, 0.7175) #assume this as a 90-degree turn asw
        move_right(50, 0.7175) #will need two in order for it to be a 180.
        actualcode(30)
        if horizlines > 0:
            move_right(50, 0.7175) #dead end case


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    move_forward(30, 4.88)
    actualcode(30)
    if horizlines > 0:
        check_for_options()
    else:
        continue

    cv2.imshow('frame', img)
    if cv2.waitKey(1) == ord('q'):
        break

# cv2.imshow('frame', img)
    # if cv2.waitKey(1) == ord('q'):
    #     break

cv2.waitKey(0)
