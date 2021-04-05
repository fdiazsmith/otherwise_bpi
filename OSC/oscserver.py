"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/pi/otherwise_bpi/test_and_examples')
from LED_brightness import * 


def print_brightness_handler(unused_addr, args, brightness):
    print("[{0}] ~ {1}".format(args[0], brightness))
    set_brightness(brightness)

def print_compute_handler(unused_addr, args, brightness):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](brightness)))
    except ValueError: pass


dispatcher = dispatcher.Dispatcher()
def listen_for_osc(ip="192.168.1.16", port=5005):
    # global dispatcher

    dispatcher.map("/filter", print)
    dispatcher.map("/brightness", print_brightness_handler, "brightness")
    dispatcher.map("/logbrightness", print_compute_handler, "Log brightness", math.log)

    server = osc_server.ThreadingOSCUDPServer(
        (ip, port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

def osc_server_close():
    LED_brightness_close()