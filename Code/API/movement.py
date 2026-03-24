import threading
import time
import RobotController
Motor = RobotController.MotorDriver()
class MotionManager:
    def __init__(self, motor):
        self.motor = motor
        self._stop_evt = threading.Event()
        self._thread = None
        self._lock = threading.Lock()

    def _run_motion(self, start_actions, stop_actions, duration_s: float):
        self._stop_evt.clear()
        with self._lock:
            for action in start_actions:
                action()

        t0 = time.monotonic()
        while (time.monotonic() - t0) < duration_s and not self._stop_evt.is_set():
            time.sleep(0.02)

        with self._lock:
            for action in stop_actions:
                action()

    def start(self, start_actions, stop_actions, duration_s: float):
        self.stop(wait=False)
        self._thread = threading.Thread(
            target=self._run_motion,
            args=(start_actions, stop_actions, duration_s),
            daemon=True,
        )
        self._thread.start()

    def stop(self, wait: bool = True):
        self._stop_evt.set()
        if wait and self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

motion = MotionManager(Motor)
def move_forward(speed: int = 50, ttime: float = 2.0):
    start = [
        lambda: Motor.MotorRun(0, "backward", speed),
        lambda: Motor.MotorRun(1, "forward", speed),
    ]
    stop_actions = [lambda: Motor.MotorStop(0), lambda: Motor.MotorStop(1)]
    motion.start(start, stop_actions, ttime)
    print(f"Moving forward: speed {speed} for {ttime}s")


def move_backward(speed: int = 50, ttime: float = 2.0):
    start = [
        lambda: Motor.MotorRun(0, "forward", speed),
        lambda: Motor.MotorRun(1, "backward", speed),
    ]
    stop_actions = [lambda: Motor.MotorStop(0), lambda: Motor.MotorStop(1)]
    motion.start(start, stop_actions, ttime)
    print(f"Moving backward: speed {speed} for {ttime}s")


def move_right(speed: int = 50, ttime: float = 1.0):
    start = [
        lambda: Motor.MotorRun(0, "forward", speed),
        lambda: Motor.MotorRun(1, "forward", speed),
    ]
    stop_actions = [lambda: Motor.MotorStop(0), lambda: Motor.MotorStop(1)]
    motion.start(start, stop_actions, ttime)
    print(f"Turning right: speed {speed} for {ttime}s")


def move_left(speed: int = 50, ttime: float = 1.0):
    start = [
        lambda: Motor.MotorRun(0, "backward", speed),
        lambda: Motor.MotorRun(1, "backward", speed),
    ]
    stop_actions = [lambda: Motor.MotorStop(0), lambda: Motor.MotorStop(1)]
    motion.start(start, stop_actions, ttime)
    print(f"Turning left: speed {speed} for {ttime}s")


def stop_all():
    motion.stop(wait=True)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    print("Motors stopped.")