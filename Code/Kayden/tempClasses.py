import gpiozero as GPIO
import time

MotorDir = [
    'forward',
    'backward',
]

ControlMode = [
    'hardward',
    'softward',
]

class HR8825():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.dir_pin = dir_pin
        self.step_pin = step_pin        
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins
        
        self.dir = GPIO.LED(self.dir_pin)
        self.step = GPIO.LED(self.step_pin)        
        self.enable = GPIO.LED(self.enable_pin)
        self.mode_1 = GPIO.LED(self.mode_pins[0])
        self.mode_2 = GPIO.LED(self.mode_pins[1])
        self.mode_3 = GPIO.LED(self.mode_pins[2])

        self.control_pin = {
          dir_pin: self.dir,
          enable_pin: self.enable,
          step_pin: self.step,
          mode_pins[0]: self.mode_1,
          mode_pins[1]: self.mode_2,
          mode_pins[2]: self.mode_3
        }
        
    def digital_write(self, pin, value):
        if value:
          self.control_pin[pin].on()
        else:
          self.control_pin[pin].off()
        
    def Stop(self):
        self.digital_write(self.enable_pin, 0)

    def Configure_mode(self, microstep):
        j = 0
        for i in microstep:
          self.digital_write(self.mode_pins[j], i)
          j = j+1
    
    def SetMicroStep(self, mode, stepformat):
        microstep = {'fullstep': (0, 0, 0),
                     'halfstep': (1, 0, 0),
                     '1/4step': (0, 1, 0),
                     '1/8step': (1, 1, 0),
                     '1/16step': (0, 0, 1),
                     '1/32step': (1, 0, 1)}

        print("Control mode:",mode)
        if (mode == ControlMode[1]):
            print("set pins")
            self.Configure_mode(microstep[stepformat])
            
    # New method to set direction without a loop
    def SetDirection(self, Dir):
        if Dir == 'forward':
            self.digital_write(self.dir_pin, 0)
        elif Dir == 'backward':
            self.digital_write(self.dir_pin, 1)

    # New non-blocking method to pulse the motor once
    def StepPulse(self):
        self.digital_write(self.step_pin, True)
        time.sleep(0.000001) # Short pulse to trigger the step
        self.digital_write(self.step_pin, False)
    
    # The original blocking TurnStep method is no longer used for simultaneous motion
    def TurnStep(self, Dir, steps, stepdelay=0.005):
        # This function is now superseded by the new forward function
        # It is still valid for single motor operation
        if (Dir == MotorDir[0]):
            print("forward")
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 0)
        elif (Dir == MotorDir[1]):
            print("backward")
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 1)
        else:
            print("the dir must be : 'forward' or 'backward'")
            self.digital_write(self.enable_pin, 0)
            return

        if (steps == 0):
            return
            
        print("turn step:",steps)
        for i in range(steps):
            self.digital_write(self.step_pin, True)
            time.sleep(stepdelay)
            self.digital_write(self.step_pin, False)
            time.sleep(stepdelay)

