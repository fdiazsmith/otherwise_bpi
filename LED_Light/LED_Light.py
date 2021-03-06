'''
* [correct wiring](http://adam-meyer.com/arduino/TIP120)
* [code example](https://electronicshobbyists.com/raspberry-pi-pwm-tutorial-control-brightness-of-led-and-servo-motor/)
'''
import RPi.GPIO as GPIO     # Importing RPi library to use the GPIO pins
import LED_Light.variables as v

class LED_Light:
    def __init__(self, pin = v.led_pin, freq=v.freq):
        GPIO.setmode(GPIO.BCM)          # We are using the BCM pin numbering
        GPIO.setup(pin, GPIO.OUT)   # Declaring pin 21 as output pin
        self.pwm = GPIO.PWM(pin, freq)    # Created a PWM object
        self.pwm.start(0)                    # Started PWM at 0% duty cycle
    
    def set_brightness(self, value):
        self.pwm.ChangeDutyCycle(value*100) # Change duty cycle

    def close(self):
        self.pwm.stop()      # Stop the PWM
        GPIO.cleanup()  # Make all the output pins LOW
        print("LED_brightness_close closed")