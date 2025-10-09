import time
from classesTest import HR8825

# Initialize motors once
Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

try:
    Motor1.SetMicroStep('softward', '1/16step')
    Motor2.SetMicroStep('softward', '1/16step')
    print("Motors running. Press Ctrl+C to stop.")

    print("Forward motion...")
    time.sleep(3)
    Motor1.forward(15)
    Motor2.forward(15)

    print("Stopping for 3 seconds...")
    time.sleep(3)

    print("Backward motion...")
    Motor1.backward(15)
    Motor2.backward(15)
    
except KeyboardInterrupt:
    print("\nStopping motors gracefully...")
finally:
    Motor1.Stop()
    Motor2.Stop()
    print("Motors stopped.")
