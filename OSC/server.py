"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""

import argparse
import math
import threading

from pythonosc import dispatcher
from pythonosc import osc_server

import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '/home/pi/otherwise_bpi/test_and_examples')
# from LED_brightness import * 
from LED_Light.LED_Light import LED_Light

dispatcher = dispatcher.Dispatcher()
light = LED_Light()

class Server:
    def __init__(self, ip = "192.168.1.16", port = 5005):
        self.ip = ip
        self.port = port
        self.server_thread = threading.Thread(target=listen_for_osc,kwargs={"ip":ip,"port":port})
        self.server_thread.start()
        pass

    def close(self):
        light.close()
        self.server_thread.join()
        pass

def print_brightness_handler(unused_addr, args, brightness):
    print("[{0}] ~ {1}".format(args[0], brightness))
    light.set_brightness(brightness)

def print_compute_handler(unused_addr, args, brightness):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](brightness)))
    except ValueError: pass




def listen_for_osc(ip="192.168.1.16", port=5005):
    # global dispatcher
    dispatcher.map("/brightness", print_brightness_handler, "brightness")

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

