from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import threading
import time
import RobotController

Motor = RobotController.MotorDriver()

app = FastAPI(
    title="Robot API",
    description="An API to perform robot actions of forward, backward, left, right turns.",
    version="1.0.0",
)

favicon_path = "favicon.ico"

@app.get("/favicon.ico")
async def get_favicon():
    try:
        return FileResponse(favicon_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Favicon not found")


# ---------- Motion manager (single active motion at a time) ----------
class MotionManager:
    def __init__(self, motor):
        self.motor = motor
        self._stop_evt = threading.Event()
        self._thread = None
        self._lock = threading.Lock()  # protect motor access

    def _run_motion(self, start_actions, stop_actions, duration_s: float):
        # Start motors under lock
        with self._lock:
            for action in start_actions:
                action()

        try:
            t0 = time.monotonic()
            # Poll stop flag frequently for snappy stops
            while (time.monotonic() - t0) < duration_s and not self._stop_evt.is_set():
                time.sleep(0.02)  # 20 ms polling interval
        finally:
            # Always stop motors, even if an exception occurs
            with self._lock:
                for action in stop_actions:
                    action()

    def start(self, start_actions, stop_actions, duration_s: float):
        # Stop any previous motion (non-blocking join)
        self.stop(wait=False)
        self._stop_evt.clear()
        self._thread = threading.Thread(
            target=self._run_motion,
            args=(start_actions, stop_actions, duration_s),
            daemon=True,
        )
        self._thread.start()

    def stop(self, wait: bool = True):
        self._stop_evt.set()
        t = self._thread
        if wait and t and t.is_alive():
            t.join(timeout=1.0)


motion = MotionManager(Motor)


# ---------- Routes that trigger non-blocking motions ----------
@app.post("/move/forward", status_code=200)
def move_forward(
    speed: int = Query(..., ge=0, le=100),
    ttime: float = Query(..., gt=0),
):
    start = [
        lambda: Motor.MotorRun(0, "forward", speed),
        lambda: Motor.MotorRun(1, "backward", speed),
    ]
    stop = [lambda: Motor.MotorStop(0), lambda: Motor.MotorStop(1)]
    motion.start(start, stop, ttime)
    return {"status": "running", "action": "forward", "speed": speed, "time_s": ttime}


@app.post("/move/backward", status_code=200)
def move_backward(
    speed: int = Query(..., ge=0, le=100),
    ttime: float = Query(..., gt=0),
):
    start = [
        lambda: Motor.MotorRun(0, "backward", speed),
        lambda: Motor.MotorRun(1, "forward", speed),
    ]
    stop = [lambda: Motor.MotorStop(0), lambda: Motor.MotorStop(1)]
    motion.start(start, stop, ttime)
    return {"status": "running", "action": "backward", "speed": speed, "time_s": ttime}


@app.post("/move/right", status_code=200)
def move_right(
    speed: int = Query(..., ge=0, le=100),
    ttime: float = Query(..., gt=0),
):
    start = [lambda: Motor.MotorRun(0, "forward", speed)]
    stop = [lambda: Motor.MotorStop(0)]
    motion.start(start, stop, ttime)
    return {"status": "running", "action": "right", "speed": speed, "time_s": ttime}


@app.post("/move/left", status_code=200)
def move_left(
    speed: int = Query(..., ge=0, le=100),
    ttime: float = Query(..., gt=0),
):
    start = [lambda: Motor.MotorRun(1, "forward", speed)]
    stop = [lambda: Motor.MotorStop(1)]
    motion.start(start, stop, ttime)
    return {"status": "running", "action": "left", "speed": speed, "time_s": ttime}


@app.post("/stop", status_code=200)
def stop():
    # Signal the background motion to stop and wait briefly
    motion.stop(wait=True)
    # Double-ensure motors are stopped (belt & suspenders)
    with motion._lock:
        Motor.MotorStop(0)
        Motor.MotorStop(1)
    return {"status": "stopped"}
