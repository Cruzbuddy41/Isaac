import gpiozero as GPIO
import time
from classes_we_use import HR8825

def forward(steps):
	try:
		Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
		Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

		Motor1.SetMicroStep('hardward','1/16step')
		Motor2.SetMicroStep('hardward' ,'1/16step')
		
  		for i in range(steps):
			Motor2.TurnStep(Dir='backward', steps=1, stepdelay=0.001)
			Motor1.TurnStep(Dir='forward', steps=1, stepdelay = 0.001)
			
		Motor1.Stop()
		Motor2.Stop()
    
	except:
		print("\nMotor stop")
		Motor1.Stop()
		Motor2.Stop()
		exit()

forward(400)
