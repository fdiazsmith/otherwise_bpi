'''
* [correct wiring](http://adam-meyer.com/arduino/TIP120)
* [code example](https://electronicshobbyists.com/raspberry-pi-pwm-tutorial-control-brightness-of-led-and-servo-motor/)
'''
import RPi.GPIO as GPIO     # Importing RPi library to use the GPIO pins
from time import sleep  # Importing sleep from time library
led_pin = 21            # Initializing the GPIO pin 21 for LED
GPIO.setmode(GPIO.BCM)          # We are using the BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)   # Declaring pin 21 as output pin

FREQUENCY = 1000
pwm = GPIO.PWM(led_pin, 100)    # Created a PWM object
pwm.start(0)                    # Started PWM at 0% duty cycle

# try:
#     while 1:                    # Loop will run forever
#         pwm.ChangeDutyCycle(100) # Change duty cycle
#         for x in range(100):    # This Loop will run 100 times
#             pwm.ChangeDutyCycle(x) # Change duty cycle
#             sleep(0.01)         # Delay of 10mS
            
#         for x in range(100,0,-1): # Loop will run 100 times; 100 to 0
#             pwm.ChangeDutyCycle(x)
#             sleep(0.01)
#         # sleep(1)
#         # print("cyclign")
# # If keyboard Interrupt (CTRL-C) is pressed
# except KeyboardInterrupt:

#     pwm.stop()      # Stop the PWM
#     GPIO.cleanup()  # Make all the output pins LOW
#     print("keyboard interrupt")
#     pass        # Go to next line

def set_brightness(value):
    pwm.ChangeDutyCycle(value*100) # Change duty cycle

def LED_brightness_close():
    pwm.stop()      # Stop the PWM
    GPIO.cleanup()  # Make all the output pins LOW
    print("LED_brightness_close closed")