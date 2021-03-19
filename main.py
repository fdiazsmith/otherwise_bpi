#!/usr/bin/env python
from smbus2 import SMBus
from grooveGas import Gas
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import time
print("OTHERWISE sensing")
# Open i2c bus 1 and read one byte from address 80, offset 0
# bus = SMBus(1)
# b = bus.read_byte_data(0x08, 0x01)
# print(b)
# bus.close()

i2c = SMBus(1)

g = Gas(i2c)
def main():
    '''
    Main program function
    '''

    gm1 = g.getGM102B()
    gm1v= g.calcVol(gm1) 
    gm3 = g.getGM302B()
    gm3v= g.calcVol(gm3) 
    gm5 = g.getGM502B()
    gm5v= g.calcVol(gm5) 
    gm7 = g.getGM702B()
    gm7v= g.calcVol(gm7) 

        # Import needed modules from osc4py3

    # Start the system.
    osc_startup()

    # Make client channels to send packets.
    osc_udp_client("192.168.1.133", 10000, "someother123")

    # Build a simple message and send it.
    # msg = oscbuildparse.OSCMessage("/test/me", None, [ gm1v])
    # osc_send(msg, "someother123")

    # # Build a message with autodetection of data types, and send it.
    # msg = oscbuildparse.OSCMessage("/test/me", None, [gm3v])
    # osc_send(msg, "someother123")

    # Buils a complete bundle, and postpone its executions by 10 sec.
    exectime = time.time() + 30   # execute in 10 seconds
    msg1 = oscbuildparse.OSCMessage("/gas/NO2", None, [ gm1v])
    msg2 = oscbuildparse.OSCMessage("/gas/C2H5OH", None, [gm3v])
    msg3 = oscbuildparse.OSCMessage("/gas/VOC", None, [gm5v])
    msg4 = oscbuildparse.OSCMessage("/gas/CO", None, [gm7v])
    bun = oscbuildparse.OSCBundle(oscbuildparse.OSC_IMMEDIATELY ,
                        [msg1, msg2, msg3, msg4])
    osc_send(bun, "someother123")
    # print("NO2:{: <20}    C2H5OH:{: <20}   VOC:{: <20}   CO:{: <20}".format(gm1v,gm3v,gm5v,gm7v))
    osc_process()

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

