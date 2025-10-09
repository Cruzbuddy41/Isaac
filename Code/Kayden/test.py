import time
from classesTest import HR8825

def move_forward(steps, delay=0.005):
    """Moves the robot forward by a specified number of steps."""
    motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
    
    try:
        motor1.SetMicroStep('softward', '1/16step')
        motor2.SetMicroStep('softward', '1/16step')
        print(f"Moving forward for {steps} steps.")
        
        motor1.forward(steps, delay)
        motor2.forward(steps, delay)

    except KeyboardInterrupt:
        print("\nStopping forward movement gracefully...")
    finally:
        motor1.Stop()
        motor2.Stop()
        print("Motors stopped.")

def move_backward(steps, delay=0.005):
    """Moves the robot backward by a specified number of steps."""
    motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
    
    try:
        motor1.SetMicroStep('softward', '1/16step')
        motor2.SetMicroStep('softward', '1/16step')
        print(f"Moving backward for {steps} steps.")

        motor1.backward(steps, delay)
        motor2.backward(steps, delay)

    except KeyboardInterrupt:
        print("\nStopping backward movement gracefully...")
    finally:
        motor1.Stop()
        motor2.Stop()
        print("Motors stopped.")

if __name__ == '__main__':
    move_forward(100)

    time.sleep(3)

    move_backward(100)
