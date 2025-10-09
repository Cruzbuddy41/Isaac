import gpiozero as GPIO
import time

MotorDir = ['forward', 'backward']
ControlMode = ['hardward', 'softward']

class HR8825():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins

        # gpiozero.LED is a simplified way to control digital outputs
        self.dir = GPIO.LED(self.dir_pin)
        self.step = GPIO.LED(self.step_pin)
        self.enable = GPIO.LED(self.enable_pin)

        # Assuming mode_pins is a list of pins
        self.mode_1 = GPIO.LED(self.mode_pins[0])
        self.mode_2 = GPIO.LED(self.mode_pins[1])
        self.mode_3 = GPIO.LED(self.mode_pins[2])
        
        self.control_pin = {
            dir_pin: self.dir,
            enable_pin: self.enable,
            step_pin: self.step,
            self.mode_pins[0]: self.mode_1,
            self.mode_pins[1]: self.mode_2,
            self.mode_pins[2]: self.mode_3
        }

    def digital_write(self, pin, value):
        if value:
            self.control_pin[pin].on()
        else:
            self.control_pin[pin].off()

    def Stop(self):
        self.digital_write(self.enable_pin, 0)

    def Configure_mode(self, microstep):
        for i, pin in enumerate(self.mode_pins):
            self.digital_write(pin, microstep[i])

    def SetMicroStep(self, mode, stepformat):
        microstep = {'fullstep': (0, 0, 0), 'halfstep': (1, 0, 0), '1/4step': (0, 1, 0), '1/8step': (1, 1, 0), '1/16step': (0, 0, 1), '1/32step': (1, 0, 1)}
        print("Control mode:", mode)
        if mode == 'softward':  # Check if the mode is 'softward'
            print("set pins")
            self.Configure_mode(microstep[stepformat])

    def step_once(self):
        """Generates a single step pulse."""
        self.digital_write(self.step_pin, True)
        time.sleep(0.000001)  # Short delay for pulse width
        self.digital_write(self.step_pin, False)
        time.sleep(0.000001)  # Short delay for pulse width

    def forward(self, steps, delay=0.005):
        print("forward")
        self.digital_write(self.enable_pin, 1)
        self.digital_write(self.dir_pin, 1)
        for _ in range(steps):
            self.step_once()
            time.sleep(delay)

    def backward(self, steps, delay=0.005):
        print("backward")
        self.digital_write(self.enable_pin, 1)
        self.digital_write(self.dir_pin, 0)
        for _ in range(steps):
            self.step_once()
            time.sleep(delay)
