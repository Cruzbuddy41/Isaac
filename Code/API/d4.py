import cv2
import numpy as np
def ts(input_path, output_path):
    frame = cv2.imread(input_path)
    if frame is None:
        print(f"Error: Could not open or find {input_path}")
        return

    height, width = frame.shape[:2]
    frame_center = width // 2
    apex_x = int(width * 0.5)
    roi_vertices = np.array([[
        (int(width * 0.1), height),
        (apex_x, int(height * 0.4)),
        (int(width * 0.9), height)
    ]], dtype=np.int32)
    error = apex_x - frame_center
    threshold = width * 0.05

    if error > threshold:
        command = "TURN RIGHT"
        color = (0, 0, 255)
    elif error < -threshold:
        command = "TURN LEFT"
        color = (255, 0, 0)
    else:
        command = "FORWARD"
        color = (0, 255, 0)
    cv2.polylines(frame, roi_vertices, isClosed=True, color=color, thickness=5)
    cv2.putText(frame, f"ACTION: {command}", (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
    cv2.imwrite(output_path, frame)
    print(f"Successfully processed {input_path}. Command: {command}")
    print(f"Result saved as {output_path}")
ts('lane.jpg', 'lane_results.jpg')
