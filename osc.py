#!/usr/bin/env python
'''
BREADCRUMS
-[More on osc4py3 here](https://osc4py3.readthedocs.io/en/latest/userdoc.html#complicated-to-use)
-[Might need to know more about this](https://learn.adafruit.com/porting-an-arduino-library-to-circuitpython-vl6180x-distance-sensor?view=all)
'''
#  Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
#general utils
import time
import math
import sys
sys.path.append("../..")
# DFROBOT oxygen
from DFRobot_Oxygen import *
# groove gas
from smbus2 import SMBus
from grooveGas import Gas
#light spectrometer
from as7262 import AS7262
print("OTHERWISE sensing")
#OSC: Start the OSC system.

osc_startup()
#OSC: Make client channels to send packets.
osc_udp_client("192.168.1.133", 10000, "touchdesigner")

COLLECT_NUMBER   = 10              # collect number, the collection range is 1-100
IIC_MODE         = 0x01            # default use IIC1
'''
   # The first  parameter is to select iic0 or iic1
   # The second parameter is the iic device address
   # The default address for iic is ADDRESS_3
   # ADDRESS_0                 = 0x70
   # ADDRESS_1                 = 0x71
   # ADDRESS_2                 = 0x72
   # ADDRESS_3                 = 0x73
'''
oxygen = DFRobot_Oxygen_IIC(IIC_MODE ,ADDRESS_3)


i2c = SMBus(1)

g = Gas(i2c)

as7262 = AS7262(i2c)
# as7262.set_integration_time(17.857)
as7262.set_measurement_mode(2)
as7262.set_illumination_led(1)
as7262.set_gain(64)
frame_timestamp = 0
'''
Main program function
'''
def main():
    global frame_timestamp
    #get gas readigns
    gm1 = g.getGM102B()
    gm1v= g.calcVol(gm1) 
    gm3 = g.getGM302B()
    gm3v= g.calcVol(gm3) 
    gm5 = g.getGM502B()
    gm5v= g.calcVol(gm5) 
    gm7 = g.getGM702B()
    gm7v= g.calcVol(gm7)
  

    red, orange, yellow, green, blue, violet = as7262.get_calibrated_values()

    oxygen_data = oxygen.get_oxygen_data(COLLECT_NUMBER);
#     print("""
# Red:    {}
# Orange: {}
# Yellow: {}
# Green:  {}
# Blue:   {}
# Violet: {}""".format(red, orange,yellow,green,blue,violet))
    # send them to Tochdesinger
    osc_process()

    gas1 = oscbuildparse.OSCMessage("/gas/NO2", None, [gm1v])
    gas2 = oscbuildparse.OSCMessage("/gas/C2H5OH", None, [gm3v])
    gas3 = oscbuildparse.OSCMessage("/gas/VOC", None, [gm5v])
    gas4 = oscbuildparse.OSCMessage("/gas/CO", None, [gm7v])
    # gases = oscbuildparse.OSCBundle(oscbuildparse.OSC_IMMEDIATELY ,
    #                     [gas1, gas2, gas3, gas4])
    # osc_send(gases, "touchdesigner")

    light1 = oscbuildparse.OSCMessage("/light/red", None, [red])
    light2 = oscbuildparse.OSCMessage("/light/orange", None, [orange])
    light3 = oscbuildparse.OSCMessage("/light/yellow", None, [yellow])
    light4 = oscbuildparse.OSCMessage("/light/green", None, [green])
    light5 = oscbuildparse.OSCMessage("/light/blue", None, [blue])
    light6 = oscbuildparse.OSCMessage("/light/violet", None, [violet])
    
    light = oscbuildparse.OSCBundle(oscbuildparse.OSC_IMMEDIATELY ,
                        [gas1, gas2, gas3, gas4,light1, light2, light3, light4, light5, light6])
                    
    osc_send(light, "touchdesigner")
    print('fps {}, oxygen {}%'.format( 1/(time.time() - frame_timestamp), oxygen_data ))
    frame_timestamp = time.time()






if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        as7262.set_measurement_mode(3)
        as7262.set_illumination_led(0)
        print("Keyboard interrupt")
    finally:
        g.close()
        osc_terminate()
        print('Program finished')