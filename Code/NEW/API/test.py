print("Motor driver test code")
Motor = MotorDriver()

print("Forward 5 seconds, half speed")
Motor.MotorRun(0, 'forward', 50)
Motor.MotorRun(1, 'forward', 50)
time.sleep(2)

print("Backward 5 seconds, half speed")
Motor.MotorRun(0, 'backward', 50)
Motor.MotorRun(1, 'backward', 50)
time.sleep(2)


print("Turn left, half speed")
Motor.MotorRun(0, 'forward', 50)
Motor.MotorRun(1, 'backward', 50)
time.sleep(2.75)


print("Turn right, half speed")
Motor.MotorRun(0, 'backward', 50)
Motor.MotorRun(1, 'forward', 50)
time.sleep(3.25)

print("Stop")
Motor.MotorStop(0)
Motor.MotorStop(1)
