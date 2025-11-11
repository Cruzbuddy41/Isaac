import cv2
from datetime import datetime
from pathlib import Path

DEVICE_INDEX = 1          # 0 -> /dev/video0, change if needed
WIDTH, HEIGHT = 1920, 1080  # pick a supported resolution

out_dir = Path("images") #hi kayden
out_dir.mkdir(exist_ok=True)

cap = cv2.VideoCapture(DEVICE_INDEX, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

if not cap.isOpened():
    raise RuntimeError("Could not open camera. Check device index and permissions.")

# Warm-up: grab a couple frames so auto-exposure can settle
for _ in range(5):
    cap.read()

ret, frame = cap.read()
if not ret:
    cap.release()
    raise RuntimeError("Failed to capture frame.")

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
outfile = out_dir / f"photo_{ts}.jpg"
cv2.imwrite(str(outfile), frame)

cap.release()
print(f"Saved {outfile}")
