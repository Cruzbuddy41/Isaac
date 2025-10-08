import gpiozero as GPIO
import time
from classesTest import HR8825

def forward(steps):
    Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
    try:
        Motor1.SetMicroStep('softward', '1/16step')
        Motor2.SetMicroStep('softward', '1/16step')
        print("Motors running. Press Ctrl+C to stop.")
        print("Sleeping 3")
        time.sleep(3) # hello
        for i in range(steps):
            Motor2.forward()
            Motor1.forward()
            time.sleep(0.05)
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
        print("Sleeping 3")
        time.sleep(3)
        for i in range(steps):
            Motor2.forward()
            print("2")
            time.sleep(1)
            Motor2.forward()
            print("2")
            Motor1.forward()
            print("1")
            print(i)
    except KeyboardInterrupt:
        print("\nStopping motors gracefully...")
    finally:
        Motor1.Stop()
        Motor2.Stop()
        print("Motors stopped.")
#forward(15)
#print("Sleeping 3")
#time.sleep(3)
backward(50)
