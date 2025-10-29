import gpiozero as GPIO
import time
from classes_we_use import HR8825


try:
	Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
	Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

	Motor1.SetMicroStep('hardward','1/16step')
	Motor2.SetMicroStep('hardward' ,'1/16step')
	Motor2.TurnStep(Dir='forward', steps=1600, stepdelay=0.0005)	
	Motor1.TurnStep(Dir='forward', steps=1600, stepdelay = 0.0005)
	time.sleep(0.5)
	Motor1.Stop()
	Motor2.Stop()

	Motor1.Stop()
	Motor2.Stop()
    
except:
    print("\nMotor stop")
    Motor1.Stop()
    Motor2.Stop()
    exit()
