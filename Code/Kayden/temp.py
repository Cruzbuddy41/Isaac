Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))

Motor1.SetMicroStep('softward','1/16step') # Changed from hardward to softward
Motor2.SetMicroStep('softward','1/16step') # Changed from hardward to softward

def forward(steps):
    try:
        # Set the direction for each motor once outside the loop
        Motor1.SetDirection('forward')
        Motor2.SetDirection('backward') # Or 'forward' if both wheels are on opposite sides
        
        # Enable the motors
        Motor1.digital_write(Motor1.enable_pin, 1)
        Motor2.digital_write(Motor2.enable_pin, 1)
        
        step_delay = 0.001
        
        for i in range(steps):
            # Pulse both step pins at the same time
            Motor1.digital_write(Motor1.step_pin, True)
            Motor2.digital_write(Motor2.step_pin, True)
            time.sleep(step_delay)
            
            Motor1.digital_write(Motor1.step_pin, False)
            Motor2.digital_write(Motor2.step_pin, False)
            time.sleep(step_delay)
			
        Motor1.Stop()
        Motor2.Stop()
    
    except Exception as e:
        print(f"\nMotor stop due to an error: {e}")
        Motor1.Stop()
        Motor2.Stop()
        exit()

# Set microstepping to 'softward' to allow software control
Motor1.SetMicroStep('softward', '1/16step')
Motor2.SetMicroStep('softward', '1/16step')

# Call the new forward function
forward(400)
