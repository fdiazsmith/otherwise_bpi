#!/usr/bin/env python
from smbus2 import SMBus
from grooveGas import Gas
import time
import argparse
import random
import logging
import threading

from pythonosc import udp_client
from oscserver import *

print("OTHERWISE sensing")
# Open i2c bus 1 and read one byte from address 80, offset 0
# bus = SMBus(1)
# b = bus.read_byte_data(0x08, 0x01)
# print(b)
# bus.close()

i2c = SMBus(1)

g = Gas(i2c)
# OSC Arguments for client
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="192.168.1.133",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=10000,
    help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

# listen_for_osc()

def main():
    '''
    Main program function
    '''
    


    client.send_message("/filter", random.random())
    print("some message")
    time.sleep(1)



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : Setting up  everything")
    osc_server_thread = threading.Thread(target=listen_for_osc,kwargs={"ip":"192.168.1.16","port":5005})
    osc_server_thread.start()
    # main()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        osc_server_thread.join()
        osc_server_close()
        g.close()
    finally:
        osc_server_thread.join()
        osc_server_close()
        g.close()
        print('Program finished')
        

