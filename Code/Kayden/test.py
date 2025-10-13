# Controls two DC motors using two HR8825 stepper motor drivers.
#
# Wiring setup (assuming BCM pin numbering):
#
# DRIVER 1 (Motor 1):
# - RPi GPIO 17 (PWM Speed) -> HR8825 ENABLE pin (Must be active LOW, LOW=enabled, HIGH=disabled)
# - RPi GPIO 27 (Direction) -> HR8825 DIR pin
# - HR8825 AOUT1 & AOUT2 -> DC Motor 1 Wires
#
# DRIVER 2 (Motor 2):
# - RPi GPIO 22 (PWM Speed) -> HR8825 ENABLE pin
# - RPi GPIO 23 (Direction) -> HR8825 DIR pin
# - HR8825 BOUT1 & BOUT2 -> DC Motor 2 Wires
#
# NOTE: The STEP pin should be connected to GND (LOW) or simply left disconnected for this direct-drive method.
 

from gpiozero import OutputDevice, PWMOutputDevice
from time import sleep
 

# --- Pin Definitions (BCM numbering) ---
 

# Motor 1 Pins (Driver 1)
# ENABLE is connected to PWM, DIR is connected to a standard output.
M1_ENABLE_PIN = 12 # Connects to HR8825 ENABLE (Controls Speed/Power, PWM)
M1_DIR_PIN = 13 # Connects to HR8825 DIR (Controls Direction)
 

# Motor 2 Pins (Driver 2)
M2_ENABLE_PIN = 4 # Connects to HR8825 ENABLE (Controls Speed/Power, PWM)
M2_DIR_PIN = 24 # Connects to HR8825 DIR (Controls Direction)
 

# --- Initialise gpiozero devices ---
 

# M1_Speed controls the HR8825 ENABLE pin via inverted PWM.
# The HR8825 ENABLE pin is active LOW, so we invert the output logic.
# value=1.0 (100% duty cycle) on M1_Speed should mean the HR8825 is fully DISABLED.
# value=0.0 (0% duty cycle) on M1_Speed should mean the HR8825 is fully ENABLED.
# We will manually invert the speed value in the control functions.
M1_Speed = PWMOutputDevice(M1_ENABLE_PIN, active_high=False, initial_value=0) # active_high=False means 0.0=GND (Enabled)
M1_Direction = OutputDevice(M1_DIR_PIN, initial_value=False)
 

# M2_Speed control
M2_Speed = PWMOutputDevice(M2_ENABLE_PIN, active_high=False, initial_value=0)
M2_Direction = OutputDevice(M2_DIR_PIN, initial_value=False)
 

print("HR8825 DC Motor Control Initialized.")
 

# --- Control Functions ---
 

def set_motor_speed(motor_pwm_device, speed_ratio):
    """
    Sets the speed of the motor. Speed ratio is a float between 0.0 (stop) and 1.0 (full speed).
    Since HR8825 ENABLE is active LOW, the PWM duty cycle must be INVERTED.
    A speed of 1.0 (full power) requires the ENABLE pin to be LOW (duty cycle 0%).
    A speed of 0.0 (off) requires the ENABLE pin to be HIGH (duty cycle 100%).
    """
    if 0.0 <= speed_ratio <= 1.0:
        # Invert the speed: 1.0 - speed_ratio
        # speed_ratio=1.0 (full speed) -> Inverted PWM value=0.0 (LOW)
        # speed_ratio=0.5 (half speed) -> Inverted PWM value=0.5
        # speed_ratio=0.0 (stop) -> Inverted PWM value=1.0 (HIGH/Disabled)
        inverted_value = 1.0 - speed_ratio
        motor_pwm_device.value = inverted_value
        print(f"Setting motor PWM to inverted value: {inverted_value:.2f}")
    else:
        print("Error: Speed ratio must be between 0.0 and 1.0.")
 

def motor_forward(motor_num, speed):
    """Run the specified motor forward."""
 
    if motor_num == 1:
        # Set DIR pin LOW for forward
        M1_Direction.off()
        set_motor_speed(M1_Speed, speed)
        print(f"Motor 1: FORWARD at {speed*100:.0f}%")
 
    elif motor_num == 2:
        # Set DIR pin LOW for forward
        M2_Direction.off()
        set_motor_speed(M2_Speed, speed)
        print(f"Motor 2: FORWARD at {speed*100:.0f}%")
 

def motor_backward(motor_num, speed):
    """Run the specified motor backward."""
    if motor_num == 1:
        # Set DIR pin HIGH for backward
        M1_Direction.on()
        set_motor_speed(M1_Speed, speed)
        print(f"Motor 1: BACKWARD at {speed*100:.0f}%")
    elif motor_num == 2:
        # Set DIR pin HIGH for backward
        M2_Direction.on()
        set_motor_speed(M2_Speed, speed)
        print(f"Motor 2: BACKWARD at {speed*100:.0f}%")
 

def motor_stop(motor_num):
    """Stop the specified motor by setting PWM to 0 (ENABLE=HIGH, which disables the bridge)."""
    if motor_num == 1:
        set_motor_speed(M1_Speed, 0)
        print("Motor 1: STOPPED")
    elif motor_num == 2:
        set_motor_speed(M2_Speed, 0)
        print("Motor 2: STOPPED")
    elif motor_num == 'all':
        set_motor_speed(M1_Speed, 0)
        set_motor_speed(M2_Speed, 0)
        print("All Motors: STOPPED")
 

# --- Demo Sequence ---
try:
    print("\n--- Starting Motor Demo ---")
 
    # 1. Motor 1 Forward (Medium Speed)
    #motor_forward(1, 0.6) # 60% speed
    #sleep(2)
 
    # 2. Motor 2 Backward (Fast Speed)
    motor_backward(2, 0.9) # 90% speed
    sleep(2)
 
    # 3. Stop Motor 1 and change Motor 2 direction
    #motor_stop(1)
    #motor_forward(2, 0.4) # 40% speed
    #sleep(2)
 
    # 4. Motor 1 Backward (Slow Speed)
    #motor_backward(1, 0.3) # 30% speed
    #sleep(2)
 
    # 5. Stop Both
    motor_stop('all')
    sleep(1)
 
except KeyboardInterrupt:
    print("\nExiting program.")
 
finally:
    # Cleanup all pins
    motor_stop('all')
    M1_Speed.close()
    M1_Direction.close()
    M2_Speed.close()
    M2_Direction.close()
    print("GPIO cleanup complete.")
