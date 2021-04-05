from time import sleep  
from LED_Light.LED_Light import LED_Light

try:
    while 1:  
        light = LED_Light()
        
        for x in range(100):    # This Loop will run 100 times
            light.set_brightness(x/100) # Change duty cycle
            sleep(0.01)         # Delay of 10mS
            
        for x in range(100,0,-1): # Loop will run 100 times; 100 to 0
            light.set_brightness(x/100)
            sleep(0.01)
        # sleep(1)
        # print("cyclign")
# If keyboard Interrupt (CTRL-C) is pressed
except KeyboardInterrupt:
    light.close()      # Stop the PWM
    print("keyboard interrupt")
    pass       # Go to next line