import gpiozero as GPIO
import time
from classes_we_use import HR8825
time.sleep(2)
def forward(steps):
    Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
    try:
        Motor1.SetMicroStep('hardward', '1/16step')
        Motor2.SetMicroStep('hardward', '1/16step')
        print("Motors running. Press Ctrl+C to stop.")
        time.sleep(5)
        for i in range(steps):
            Motor2.Turn(Dir='forward')
            Motor1.Turn(Dir='backward')
            time.sleep(0.1)
            Motor2.Stop()
            Motor1.Stop()
    except KeyboardInterrupt:
        print("\nStopping motors gracefully...")
    finally:
        Motor1.Stop()
        Motor2.Stop()
        print("Motors stopped.")
def backward(steps):
    Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
    try:
        Motor1.SetMicroStep('hardward', '1/16step')
        Motor2.SetMicroStep('hardward', '1/16step')
        print("Motors running. Press Ctrl+C to stop.")
        time.sleep(5)
        for i in range(0, steps):
            Motor2.Turn(Dir='backward')
            Motor1.Turn(Dir='forward')
            Motor2.Stop()
            Motor1.Stop()
    except KeyboardInterrupt:
        print("\nStopping motors gracefully...")
    finally:
        Motor1.Stop()
        Motor2.Stop()
        print("Motors stopped.")
forward(40)
backward(40) #bugger
