from time import sleep  
import math
import random

from Oxygen_sensor import *

from OSC.server import Server
from OSC.client import Client

    

if __name__ == "__main__":

    oxygen = DFRobot_Oxygen_IIC()
    osc_server = Server()
    osc_client = Client()
    # setup stuff that should happen once
    try:
        while True:
            # loopforever
            oxygen_data = oxygen.get_oxygen_data()
            osc_client.send_message("/filter", random.random())
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        osc_server.close()
    finally:
        print('Program finished')

        
