from PCA9685 import PCA9685
import time

Dir = [
    'forward',
    'backward'
]
pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

class MotorDriver():
    ''' Motor Driver Class '''
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4

    def MotorRun(self, motor, index, speed):
        '''
        Code that turns the motors and adjusts speed
        motor - 0 or 1 Right side = 0, Left side = 1
        index - forward or backward
        speed - 0-100 
        '''

        # Can't be more than 100%
        #if int(speed) > 100:
            #return

        # Right side motor
        if(motor == 0):

            # Set our motor speed
            pwm.setDutycycle(self.PWMA, speed)

            # Log motor
            print("Right side ", end='')

            # Move this side forward
            if(index == Dir[0]):
                print (Dir[0])
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                print (Dir[1])
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)

        # Left side motor
        elif(motor == 1):

            pwm.setDutycycle(self.PWMB, speed)
            print("Left side ", end='')

            # Move forward
            if(index == Dir[0]):
                print (Dir[0])
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                print (Dir[1])
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

        # You can only move forward or backwards
        else:
            print("Error: index must be forward or backward")
            return

    def MotorStop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)
