#!/usr/bin/env python
'''
BREADCRUMS
-[More on osc4py3 here](https://osc4py3.readthedocs.io/en/latest/userdoc.html#complicated-to-use)
'''
#  Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
#general utils
import time
import math
# groove gas
from smbus2 import SMBus
from grooveGas import Gas

print("OTHERWISE sensing")
#OSC: Start the OSC system.
osc_startup()
#OSC: Make client channels to send packets.
osc_udp_client("192.168.1.133", 10000, "touchdesigner")

i2c = SMBus(1)

g = Gas(i2c)

def main():
    '''
    Main program function
    '''
    #get gas readigns
    gm1 = g.getGM102B()
    gm1v= g.calcVol(gm1) 
    gm3 = g.getGM302B()
    gm3v= g.calcVol(gm3) 
    gm5 = g.getGM502B()
    gm5v= g.calcVol(gm5) 
    gm7 = g.getGM702B()
    gm7v= g.calcVol(gm7)
    # send them to Tochdesinger
    osc_process()
    msg1 = oscbuildparse.OSCMessage("/gas/NO2", None, [gm1v])
    msg2 = oscbuildparse.OSCMessage("/gas/C2H5OH", None, [gm3v])
    msg3 = oscbuildparse.OSCMessage("/gas/VOC", None, [gm5v])
    msg4 = oscbuildparse.OSCMessage("/gas/CO", None, [gm7v])
    bun = oscbuildparse.OSCBundle(oscbuildparse.OSC_IMMEDIATELY ,
                        [msg1, msg2, msg3, msg4])
    osc_send(bun, "touchdesigner")

if __name__ == "__main__":
    try:
        while True:
            main()
            
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        print('Program finished')
        g.close()
        osc_terminate()