import cv2
import datetime

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()
#fff
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 20.0
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

now = datetime.datetime.now()
filename = f"recording_{now.strftime('%Y%m%d_%H%M%S')}.mp4"

out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
recording = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    cv2.imshow('Camera Feed', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        recording = not recording
        if recording:
            print("Recording started...")
        else:
            print("Recording stopped.")

    if recording:
        out.write(frame)

    if key == ord('q'):
        print("Exiting and turning off camera.")
        break